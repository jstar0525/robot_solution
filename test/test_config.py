import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest

import config

class TestConfig(unittest.TestCase):
    
    # yaml 설정 파일 경로가 잘못되었을 경우, 에러 로그 출력 & default logger 실행
    def test_invalid_path(self) -> None:
        with self.assertLogs() as captured:
            test_cfg = config.Config(config_path="./invalid.yaml", 
                                     logger_name="invalid_path")
        self.assertIn("yaml config file can not load", captured.output[2])
        
    # config['logger'] key값이 없을 경우, 에로 로그 출력 & default logger 실행
    def test_none_log(self) -> None:
        with self.assertLogs() as captured:
            test_cfg = config.Config(config_path="./none_config.yaml",
                                     logger_name="none_log")
        self.assertIn("yaml config['logger'] have a problem", captured.output[2])
    
    # config['logger'] key값이 없을 경우, .get_log()는 {} 반환
    def test_none_logger(self) -> None:
        test_cfg = config.Config(config_path="./none_config.yaml",
                                 logger_name="none_logger").get_log()
        self.assertEqual(test_cfg, {})
        
    # config['data_manager'] key값이 없을 경우, .get_manager()는 {} 반환
    def test_none_manager(self) -> None:
        test_cfg = config.Config(config_path="./none_config.yaml",
                                 logger_name="none_manage").get_manager()
        self.assertEqual(test_cfg, {})
        
    # config['data_processor'] key값이 없을 경우, .get_processor()는 {} 반환
    def test_none_processor(self) -> None:
        test_cfg = config.Config(config_path="./none_config.yaml",
                                 logger_name="none_processor").get_processor()
        self.assertEqual(test_cfg, {})
    
    # 정상 작동시 각 키의 값 확인
    def test_config(self) -> None:
        test_cfg = config.Config(config_path="./test_config.yaml",
                                 logger_name="test_config")
        self.assertEqual(list(test_cfg.config.keys()), 
                         ['data_manager', 'logger', 'data_processor'])

if __name__ == '__main__':
    unittest.main()