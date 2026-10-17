import json
import logging
from datetime import UTC, datetime

from src.env import DAEMON_LOGGER_LEVEL, ENVIRONMENT, LOG_LEVEL

_logger = logging.getLogger(__name__)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "line_number": record.lineno,
            "message": record.getMessage(),
            "environment": ENVIRONMENT,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(DAEMON_LOGGER_LEVEL or LOG_LEVEL)
    root_logger.addHandler(handler)
    if DAEMON_LOGGER_LEVEL:
        _logger.warning(
            "DAEMON_LOGGER_LEVEL is deprecated and will be removed in the next major version. Use LOG_LEVEL instead"
        )
