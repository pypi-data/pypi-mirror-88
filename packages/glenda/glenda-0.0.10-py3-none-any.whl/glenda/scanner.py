from confluent_kafka import Consumer, Producer
import os
import logging
import json

module_logger = logging.getLogger("glendaWrapper.Scanner")


class Scanner:
    KAFKA_URL = None
    PROGRESS_TOPIC = "progress"
    REPORT_TOPIC = "master"

    SCANNER_NAME = ""

    consumer = None
    producer = None

    def __init__(self, scanner_name: str) -> None:
        self.KAFKA_URL = os.getenv("KAFKA_URL", "localhost:9093")
        logging.debug(f"KAFKA_URL {self.KAFKA_URL}")

        self.SCANNER_NAME = scanner_name

        consumer_args = {
            "bootstrap.servers": self.KAFKA_URL,
            "group.id": self.SCANNER_NAME,
            "auto.offset.reset": "earliest",
            "max.poll.interval.ms": 15000000,
            "message.max.bytes": 20000000,
        }
        self.consumer = Consumer(consumer_args)

        self.producer = Producer(
            {"bootstrap.servers": self.KAFKA_URL, "message.max.bytes": 20000000}
        )

    def __validate(self, data) -> bool:
        scanner = data.get("scanner_only", self.SCANNER_NAME)
        not_use_scanners = data.get("not_use_scanners", [])

        if self.SCANNER_NAME in not_use_scanners or scanner != self.SCANNER_NAME:
            logging.info("Scanner not use. Skip.")
            return False

        return True

    def __kafka_callback(self, err, msg) -> None:
        """Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush()."""
        if err is not None:
            logging.error("Message delivery failed: {}".format(err))
        else:
            logging.info(
                "Message delivered to {} [{}]".format(msg.topic(), msg.offset())
            )

    def start(self, component: dict, level="component") -> None:
        """
        Отправляем в kafka сообщение о начале сканирования
        data нужна временно. Потом от нее избавимся
        """
        logging.info("Scanner -> Glenda: progress is starting")
        logging.debug(component)

        levelId = component.get("id", -1)

        message = json.dumps(
            {
                "level": level,  # TODO: change
                "levelId": levelId,
                "status": "progress",
                "scanner": self.SCANNER_NAME,
            }
        )

        self.producer.produce(
            self.PROGRESS_TOPIC, message.encode("utf-8"), callback=self.__kafka_callback
        )
        self.producer.flush()

    def queue(self, queue_name: str, handler):
        """
        Ждем из очереди задачи на скан
        """
        self.consumer.subscribe([queue_name])
        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                if "Broker: No more messages" not in str(message.error()):
                    logging.warning("Consumer error: {}".format(message.error()))

                continue

            data = json.loads(message.value())

            logging.info(
                f"Glenda -> Scanner: get new task for {data.get('project_name', 'undefined')}"
            )
            logging.debug(
                f"MSG: offset: {message.offset()}, value: {message.value().decode()}"
            )

            # Если по каким-то причинам мы пропускаем таску,
            # то нам все равно необходимо отослать результаты сканирования
            if not self.__validate(data):
                self.skip("scanner not used", data.get("component", {}))
                continue

            handler(data)

    def result(
        self, data: list, component: dict, type="default", level="component"
    ) -> None:
        """
        Отправляем результаты сканирования обратно в мастер
        type - тип отправляемого отчета о сканировании (по умолчанию default)
        """
        levelId = component.get("id", -1)

        logging.info(f"Scanner -> Glenda: send result for component {levelId}")
        logging.debug(data)

        report = {
            "success": True,
            "level": level,  # TODO: change
            "levelId": levelId,
            "result": {"type": type, "count": len(data), "data": data},  # TODO: change
            "scanner": self.SCANNER_NAME,
        }

        report = json.dumps(report)

        self.producer.produce(
            self.REPORT_TOPIC, report.encode("utf-8"), callback=self.__kafka_callback
        )
        self.producer.flush()

        message = json.dumps(
            {
                "level": level,  # TODO: change
                "levelId": levelId,
                "status": "done",
                "scanner": self.SCANNER_NAME,
            }
        )

        self.producer.produce(
            self.PROGRESS_TOPIC, message.encode("utf-8"), callback=self.__kafka_callback
        )
        self.producer.flush()

    def error(self, message: str, component: dict, level="component") -> None:
        """
        Отправляем сообщение об ошибке в мастер
        message - сообщение об ошибке
        component - ...
        """
        levelId = component.get("id", -1)

        logging.info(f"Scanner -> Glenda: send error message for component {levelId}")
        logging.debug(message)

        message = json.dumps(
            {
                "level": level,  # TODO: change
                "levelId": levelId,
                "status": "error",
                "scanner": self.SCANNER_NAME,
                "message": message,
            }
        )

        self.producer.produce(
            self.PROGRESS_TOPIC, message.encode("utf-8"), callback=self.__kafka_callback
        )
        self.producer.flush()

    def skip(self, reason: str, component: dict, level="component") -> None:
        """
        Отправляем сообщение о том, что пропускаем сканер
        reason - причина пропуска сканера
        component - ...
        """
        levelId = component.get("id", -1)

        logging.info(f"Scanner -> Glenda: send error message for component {levelId}")
        logging.debug(reason)

        message = json.dumps(
            {
                "level": level,  # TODO: change
                "levelId": levelId,
                "status": "skip",
                "scanner": self.SCANNER_NAME,
                "message": reason,
            }
        )

        self.producer.produce(
            self.PROGRESS_TOPIC, message.encode("utf-8"), callback=self.__kafka_callback
        )
        self.producer.flush()
