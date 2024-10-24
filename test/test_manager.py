import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import unittest

import config
import data_manager

class TestManager(unittest.TestCase):
    
    def test_manager_cfg(self) -> None:
        cfg = config.Config(config_path="./test_manager_cfg.yaml")
        print(cfg)
        
if __name__ == '__main__':
    unittest.main()