import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import shutil
import unittest

import logger


class TestLogger(unittest.TestCase):
    
    # config의 값이 잘못된 경우 에러 로그 출력, default config 사용
    def test_wrong_cfg(self) -> None:
        cfg = {}
        
        with self.assertLogs() as captured:
            test_logger = logger.CustomLogger("wrong_cfg", cfg)
        self.assertIn("invaild config : use default config", captured.output[0])
    
    # 저장 디렉토리가 없을 경우 디렉토리 생성
    def test_none_dir(self) -> None:
        cfg = {"path": "./logs/log.log",
               "save_log": True,
               "print_log" : True}
        
        # remove dir 
        log_dir = os.path.dirname(cfg['path'])
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)
            
        test_logger = logger.CustomLogger("none_dir", cfg)
        
        self.assertTrue(os.path.exists(log_dir))
        
    # save_log, print_log 
    def test_all_log(self) -> None:
        cfg = {"path": "./logs/log.log",
               "save_log": True,
               "print_log" : True}
        
        with self.assertLogs() as captured:
            test_logger = logger.CustomLogger("oo", cfg).logger
        self.assertIn("enable save log", captured.output[0])
        self.assertIn("enable print log", captured.output[1])
    
    # not_save, print_log
    def test_not_save(self) -> None:
        cfg = {"path": "./logs/log.log",
               "save_log": False,
               "print_log" : True}
        
        with self.assertLogs() as captured:
            test_logger = logger.CustomLogger("xo", cfg).logger
        self.assertIn("disable save log", captured.output[0])
        self.assertIn("enable print log", captured.output[1])
        
    # save_log, not_print
    def test_not_print(self) -> None:
        cfg = {"path": "./logs/log.log",
               "save_log": True,
               "print_log" : False}
        
        with self.assertLogs() as captured:
            test_logger = logger.CustomLogger("ox", cfg).logger
        self.assertIn("enable save log", captured.output[0])
        self.assertIn("disable print log", captured.output[1])
        
    # not_save, not_print
    def test_not_log(self) -> None:
        cfg = {"path": "./logs/log.log",
               "save_log": False,
               "print_log" : False}
        
        with self.assertLogs() as captured:
            test_logger = logger.CustomLogger("xx", cfg).logger
            test_logger.info("test")
        self.assertIn("disable save log", captured.output[0])
        self.assertIn("disable print log", captured.output[1])
        # 3번째 log가 생성되지 않음
        self.assertEqual(2, len(captured.output))
    #     # for i in range(len(captured.output)):
    #     #     print(captured.output[i])

if __name__ == '__main__':
    unittest.main()