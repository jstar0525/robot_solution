import yaml
import logger


class Config:
    """
    설정 파일로부터 설정 값을 읽음
    
    Args:
        config_path (str): 설정 파일 경로
        logger_name (str) : logger 이름
        
    Attributes:
        config_path (str): 설정 파일 경로
        config (dict): 설정 값
        
        cfg_logger (logging.Logger): 설정 파일 관리 로거
    """
    
    def __init__(self, config_path: str = "./config.yaml", logger_name: str = "config") -> None:
        self.config_path = config_path
        self.logger_name = logger_name
        self.config = self.load_config()
        

    def load_config(self) -> dict:
        """ 설정 파일 경로로부터 설정 값을 읽음
        
        Raises:
            파일 입력 오류

        Returns:
            dict: 설정 값
        """
        
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            # make config logger
            self.cfg_logger = logger.CustomLogger(self.logger_name, config['logger']).logger
            self.cfg_logger.info("load yaml config file : "+self.config_path)
            return config
        except KeyError as e:
            # make default config logger
            self.cfg_logger = logger.CustomLogger(self.logger_name).logger
            self.cfg_logger.error("yaml config['logger'] have a problem : "+str(config))
            self.cfg_logger.info("use default logger : "+self.logger_name)
            self.cfg_logger.exception(e)
        except Exception as e:
            # make default config logger
            self.cfg_logger = logger.CustomLogger(self.logger_name).logger
            self.cfg_logger.error("yaml config file can not load : "+self.config_path)
            self.cfg_logger.info("use default logger : "+self.logger_name)
            self.cfg_logger.exception(e)
    
    # check config key        
    def check_cfg(self, key) -> dict:
        try:
            cfg = self.config[key]
        except Exception as e:
            self.cfg_logger.error("invaild config")
            self.cfg_logger.exception(e)
            cfg = {}
        return cfg
    
    def get_log(self) -> dict:
        return self.check_cfg('logger')
    
    def get_manager(self) -> dict:
        return self.check_cfg('data_manager')
    
    def get_processor(self) -> dict:
        return self.check_cfg('data_processor')
