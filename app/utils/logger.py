import logging
import os
from typing import Optional


class Logger:
    """
    Simple logger wrapper for INFO, WARNING and ERROR messages.

    Usage:
        from app.utils.logger import AppLogger
        logger = AppLogger(name="chatbot").get()     # returns a logging.Logger
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

    Or use the wrapper methods:
        wrapper = AppLogger(name="chatbot")
        wrapper.info("Info message")
    """

    def __init__(self, name: str = "chatbot", level: Optional[str] = None, log_file: Optional[str] = None):
        self.name = name
        self._logger = logging.getLogger(name)

        # Avoid adding duplicate handlers if logger already configured
        if self._logger.handlers:
            return

        env_level = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
        numeric_level = getattr(logging, env_level, logging.INFO)
        self._logger.setLevel(numeric_level)

        fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        formatter = logging.Formatter(fmt)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self._logger.addHandler(sh)

        if log_file:
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

        # Prevent double logging if root logger is configured
        self._logger.propagate = False

    def get(self) -> logging.Logger:
        """Return the underlying logging.Logger instance."""
        return self._logger

    # Convenience wrapper methods
    def info(self, msg: str, *args, **kwargs) -> None:
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self._logger.error(msg, *args, **kwargs)

logger = Logger("chatbot")