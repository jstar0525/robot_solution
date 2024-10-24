import os
import numpy as np
from PIL import Image
import open3d as o3d
import matplotlib.pyplot as plt

import logger


class DataManager:
    """
    3D point cloud 데이터를 읽어오고 시각화 및 저장하여 관리
    
    설정 파일의 파일 입출력 경로 설정에 따라
    3D point cloud 데이터를 읽어오고 시각화 및 저장하여 관리
    
    Args:
        config (dict): 설정 파일로부터의 설정 값
        
    Atrributes:
        manage_logger (logging.Logger): 3D 데이터 관리 로거
        
        input_data (str): 3D 데이터 입력 경로
        output_depth (str): depth map 출력 경로
        output_heat (str): heat map 출력 경로
        output_pcd (str): (노이즈 처리된) 3D 데이터 출력 경로
        
        flag_save_depth (bool): depth map 출력 경로 지정 여부에 따른 저장 여부 
        flag_save_heat (bool): heat map 출력 경로 지정 여부에 따른 저장 여부 
        flag_save_pcd (bool): (노이즈 처리된) 3D 데이터 출력 경로 지정 여부에 따른 저장 여부 
    """
    def __init__(self, config: dict) -> None:

        # manage_logger
        self.manage_logger = logger.CustomLogger("manager", config.get_log()).logger
        
        # config
        cfg_manage = config.get_manager()
        self.set_manager_cfg(cfg_manage)
        
    def set_manager_cfg(self, cfg_manage: dict) -> None:
        """ 설정 값으로부터 파일 입출력 경로를 설정
        
        설정 값으로부터 파일 입출력 경로를 설정하고
        출력 경로 미지정시 해당 파일은 저장하지 않도록 flag를 설정

        Args:
            cfg_manage (dict): 3D 데이터 관리 설정 값
        """
        
        self.input_data = cfg_manage['input_path']['3d_data']
        
        self.flag_save_depth = False
        self.flag_save_heat = False
        self.flag_save_pcd = False
        
        if 'output_path' in cfg_manage and cfg_manage['output_path'] != None:
            if '2d_depth_map' in cfg_manage['output_path']:
                self.flag_save_depth = True
                self.output_depth = cfg_manage['output_path']['2d_depth_map']
            if '2d_heat_map' in cfg_manage['output_path']:
                self.flag_save_heat = True
                self.output_heat = cfg_manage['output_path']['2d_heat_map']
                # self.depth_csv = cfg_manage['output_path']['2d_depth_csv']
            if '3d_filtered_data' in cfg_manage['output_path']:
                self.flag_save_pcd = True
                self.output_pcd = cfg_manage['output_path']['3d_filtered_data']
                
    def read_pcd(self) -> o3d.cpu.pybind.geometry.PointCloud:
        """ 3D Point Cloud 파일(.ply or .pcd)의 경로로부터 데이터를 읽는다. 
        
        Raises:
            파일 입력 오류

        Returns:
            o3d.cpu.pybind.geometry.PointCloud: 3D Point Cloud 데이터
        """
        try:
            pcd = o3d.io.read_point_cloud(self.input_data)
            self.manage_logger.info("read point cloud")
            return pcd
        except Exception as e:
            self.manage_logger.error("point cloud can not read")
            self.manage_logger.exception(e)

    def draw_pcd(self, pcd: o3d.cpu.pybind.geometry.PointCloud) -> None:
        o3d.visualization.draw_geometries([pcd])
        
    def save_pcd(self, pcd: o3d.cpu.pybind.geometry.PointCloud) -> None:
        """경로가 지정되었을 때 3D point cloud를 저장하고
        경로가 지정되지 않았을 경우 3D point cloud를 저장하지 않음

        Args:
            pcd (o3d.cpu.pybind.geometry.PointCloud) : 3D Point Cloud 데이터
            
        Raises:
            파일 출력 오류
        """
        
        if self.flag_save_pcd:
            # make output dir
            output_dir = os.path.dirname(self.output_pcd)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            try:
                o3d.io.write_point_cloud(self.output_pcd, pcd)
                self.manage_logger.info("saved (filtered) pcd")
            except Exception as e:
                self.manage_logger.error("(filtered) pcd can not save")
                self.manage_logger.exception(e)
        else:
            self.manage_logger.warning("No path specified : do not save (filterd) pcd")
            
    def show_img(self, img: np.array) -> None:
        plt.imshow(img)
        plt.show()

    def save_depth(self, depth_map: np.array) -> None:
        """경로가 지정되었을 때 depth map을 저장하고
        경로가 지정되지 않았을 경우 depth map을 저장하지 않음

        Args:
            depth_map (np.array) : depth map 데이터
            
        Raises:
            파일 출력 오류
        """
        
        if self.flag_save_depth:
            # make output dir
            output_dir = os.path.dirname(self.output_depth)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            pil_depth = Image.fromarray(depth_map, 'F')
            try:
                pil_depth.save(self.output_depth, "TIFF")
                # np.savetxt(self.depth_csv, depth_map, delimiter=",")
                self.manage_logger.info("saved depth map")
            except Exception as e:
                self.manage_logger.error("depth map can not save")
                self.manage_logger.exception(e)
        else:
            self.manage_logger.warning("No path specified : do not save depth map")

    def save_heat(self, heat_map: np.array) -> None:
        """경로가 지정되었을 때 heat map을 저장하고
        경로가 지정되지 않았을 경우 heat map을 저장하지 않음

        Args:
            heat_map (np.array) : heat map 데이터
            
        Raises:
            파일 출력 오류
        """
        
        if self.flag_save_heat:
            # make output dir
            output_dir = os.path.dirname(self.output_heat)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            pil_heat = Image.fromarray(heat_map, "RGB")
            try:
                pil_heat.save(self.output_heat, "PNG")
                self.manage_logger.info("saved heat map")
            except Exception as e:
                self.manage_logger.error("heat map can not save")
                self.manage_logger.exception(e)
        else:
            self.manage_logger.warning("No path specified : do not save heat map")