import yaml
import logger


class Config:
    """
    설정 파일로부터 설정 값을 읽음
    
    Args:
        config_path (str): 설정 파일 경로
        
    Attributes:
        config_path (str): 설정 파일 경로
        config (dict): 설정 값
        
        cfg_logger (logging.Logger): 설정 파일 관리 로거
    """
    
    def __init__(self, config_path: str = "./config.yaml") -> None:
        self.config_path = config_path
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
            self.cfg_logger = logger.CustomLogger("config", config['logger']).logger
            self.cfg_logger.info("load yaml config file")
            return config
        except Exception as e:
            # make default config logger
            self.cfg_logger = logger.CustomLogger("config").logger
            self.cfg_logger.error("yaml config file can not load")
            self.cfg_logger.exception(e)
    
    def get_log(self) -> dict:
        return self.config['logger']
    
    def get_manager(self) -> dict:
        return self.config['data_manager']
    
    def get_processor(self) -> dict:
        return self.config['data_processor']
