import os
import logging


class CustomLogger:
    """
    로그 호출시 프린트 로그와 파일 로그를 남김
    
    설정 파일의 파일 로그 저장 경로, 파일 로그 사용 여부, 프린트 로그 사용 여부 설정에 따라
    로그 호출 시 프린트 로그와 파일 로그를 남김
    
    Args:
        name (str): logger의 이름
        log_config (dict): 로그의 설정 값 (파일 로그 저장 경로 / 파일 로그 사용 여부 / 프린트 로그 사용 여부)
        
    Attributes:
        log_level (int): logger의 레벨을 설정
        formatter (logging.Formatter): logger의 포멧을 설정
        log_path (str): 파일 로그를 저장할 경로
        save_log (bool): 파일 로그 사용 여부
        print_log (bool): 프린트 로그의 사용 여부
        logger (logging.Logger): logger
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
        self.logger.info("enable save log")

    def enable_print(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(stream_handler)
        self.logger.info("enable print log")

    def disable_log(self):
        self.logger.info("disable save and print log")
        self.logger.disabled = True
        
