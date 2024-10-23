import os
import numpy as np
from PIL import Image
import open3d as o3d
import matplotlib.pyplot as plt

import logger
from config import Config as cfg


class DataManager:
    """
    """
    def __init__(self, config: cfg) -> None:

        # manage_logger
        self.manage_logger = logger.CustomLogger("manager", config.get_log()).logger
        
        # config
        cfg_manage = config.get_manager()
        self.input_data = cfg_manage['input_path']['3d_data']
        self.output_depth = cfg_manage['output_path']['2d_depth_map']
        self.output_heat = cfg_manage['output_path']['2d_heat_map']

    def read_pcd(self):
        try:
            pcd = o3d.io.read_point_cloud(self.input_data)
            self.manage_logger.info("read point cloud")
            return pcd
        except Exception as e:
            self.manage_logger.critical("point cloud can not read")
            self.manage_logger.exception(e)


    def draw_pcd(self, pcd):
        o3d.visualization.draw_geometries([pcd])
        
    def show_img(self, img: np.array) -> None:
        plt.imshow(img)
        plt.show()

    def save_depth(self, depth_map: np.array) -> None:
        
        # make output dir
        output_dir = os.path.dirname(self.output_depth)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        pil_depth = Image.fromarray(depth_map, 'F')
        try:
            pil_depth.save(self.output_depth, "TIFF")
            self.manage_logger.info("saved depth map")
        except Exception as e:
            self.manage_logger.critical("depth map can not save")
            self.manage_logger.exception(e)
        np.savetxt("./output/depth_map.csv", depth_map, delimiter=",")

    def save_heat(self, heat_map: np.array) -> None:
        
        # make output dir
        output_dir = os.path.dirname(self.output_heat)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        pil_heat = Image.fromarray(heat_map, "RGB")
        try:
            pil_heat.save(self.output_heat, "PNG")
            self.manage_logger.info("saved heat map")
        except Exception as e:
            self.manage_logger.critical("heat map can not save")
            self.manage_logger.exception(e)
        # plt.imshow(heat_map)
        # plt.show()
        









