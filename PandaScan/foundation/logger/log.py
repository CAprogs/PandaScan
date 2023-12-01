import logging


class CustomLogger:
    def __init__(self, level, format="[%(levelname)s] %(message)s"):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)

        # Add a logging handler to the console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(format))
        self.logger.addHandler(stream_handler)

    def debug(self, message):
        """display a debug message

        Args:
            message (str): message to display
        """
        self.logger.debug(f"{message}\n")

    def info(self, message):
        """display an info message

        Args:
            message (str): message to display
        """
        self.logger.info(f"{message}\n")


LOG_LEVELS = [logging.DEBUG,
              logging.INFO]

LOG_FORMATS = ["%(message)s",
               "%(levelname)s - %(message)s"]
