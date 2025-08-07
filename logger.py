import os
import json

from datetime import datetime, timedelta


class Logger:
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
