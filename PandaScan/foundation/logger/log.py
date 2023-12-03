import logging


LOG_LEVELS = [logging.DEBUG,
              logging.INFO]

LOG_FORMATS = ["%(message)s",
               "%(levelname)s - %(message)s"]


class CustomLogger:
    def __init__(self, level="INFO", format="[%(levelname)s] %(message)s", state=True):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        self.state = state

        # Add a logging handler to the console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(format))
        self.logger.addHandler(stream_handler)

    def debug(self, message):
        """display a debug message

        Args:
            message (str): message to display
        """
        if self.state is True:
            self.logger.debug(f"{message}\n")

    def info(self, message):
        """display an info message

        Args:
            message (str): message to display
        """
        if self.state is True:
            self.logger.info(f"{message}\n")
