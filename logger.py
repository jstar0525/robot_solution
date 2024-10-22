import os
import logging

class CustomLogger:
    """
    """
    def __init__(self, name: str, 
                 log_config: dict = {"path": "./logs/log.log",
                                     "save_log": True,
                                     "print_log" : True}) -> None:
        
        # handler settings
        self.log_level = logging.DEBUG
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.formatter = logging.Formatter(log_format)

        # log seetings
        self.log_path = log_config["path"]
        self.save_log = log_config["save_log"]
        self.print_log = log_config["print_log"]

        # make log dir
        log_dir = os.path.dirname(self.log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)

        if self.save_log:
            self.enable_save()

        if self.print_log:
            self.enable_print()

        if not self.save_log and not self.print_log:
            self.disable_log()

    def enable_save(self):
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def enable_print(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)

    def disable_log(self):
        self.logger.disabled = True

        
