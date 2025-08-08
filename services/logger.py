import os
import json
import logging

from pathlib import Path
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, name: str = "app", log_dir: str = "logs"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        Path(log_dir).mkdir(parents=True, exist_ok=True)
        log_file = os.path.join(log_dir, f"{name}.log")

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if os.getenv("DEBUG_LOG") else logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = TimedRotatingFileHandler(
            log_file, when="midnight", backupCount=7, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def info(self, message: str, data: dict | None = None):
        if data:
            message = f"{message} | data={data}"
        self.logger.info(message)

    def error(self, message: str, data: dict | None = None):
        if data:
            message = f"{message} | data={data}"
        self.logger.error(message)

    def debug(self, message: str, data: dict | None = None):
        if data:
            message = f"{message} | data={data}"
        self.logger.debug(message)

    @staticmethod
    def get_utc_timestamp():
        local_time = datetime.now()
        utc_offset = local_time.utcoffset() or timedelta()
        utc_time = local_time - utc_offset
        return int(utc_time.timestamp() * 1e9)

    def log(self, message: str, data: dict | None = None):
        log_message = {"message": message}

        if data:
            log_message["data"] = json.dumps(data)

        timestamp = self.get_utc_timestamp()

        if os.getenv("DEBUG_LOG"):
            console_message = f"\n\n{datetime.fromtimestamp(timestamp / 1e9)} - {message}"
            if data:
                console_message += f"\n{json.dumps(data, ensure_ascii=False, indent=2)}"

            print(console_message)
