import numpy as np
import matplotlib.pyplot as plt

import logger
from config import Config as cfg

class InvalidMap(Exception):
    def __init__(self):
        super().__init__("Unabel to create image")

class DataProcessor:
    """
    """
    def __init__(self, config: cfg) -> None:

        # processor_logger
        self.processor_logger = logger.CustomLogger("processor", config.get_log()).logger
        
        cfg_processor = config.get_processor()
        self.cfg_filter = cfg_processor['filter']
        self.cfg_projector = cfg_processor['projector']
        
        self.get_intrinsic(self.cfg_projector['intrinsic'])
        self.get_extrinsic(self.cfg_projector['extrinsic'])
        
    def debug_matrix(self, name: str, matrix: np.array):
        self.processor_logger.debug(name+" : "+str(matrix.shape)+"\n"+str(matrix))


    def filter(self, pcd, mean_k=50, std_dev_mul_thresh=1.0):

        filtered, outlier = pcd.remove_statistical_outlier(mean_k, std_dev_mul_thresh)
        
        return filtered
    
    def get_intrinsic(self, cfg_int: dict) -> np.array:
        # [[fx 0, cx],
        #  [0, fy, cy],
        #  [0, 0, 1]]
        self.intrinsic = np.reshape(cfg_int['data'], [cfg_int['rows'], cfg_int['cols']])
        self.debug_matrix("camera intrinsic", self.intrinsic)
        
        return self.intrinsic
        
    def get_extrinsic(self, cfg_ext):
        # [[r11, r12, r13, t1],
        #  [r21, r22, r23, t2],
        #  [r31, r32, r33, t3]]
        self.extrinsic = np.reshape(cfg_ext['data'], [cfg_ext['rows'], cfg_ext['cols']])
        self.debug_matrix("camera extrinsic", self.extrinsic)
        
        return self.extrinsic
        
    def project_pcd_to_pixel(self, o3d_pcd):
        """
        input : 3D points in 3D sensor frame (N x 3)
        output : 2D pixels in image frame (N x 2)
        """
        
        # convert open3d points to numpy array
        pcd = np.asarray(o3d_pcd.points)
        self.debug_matrix("pcd", pcd)
        
        # camera matrix
        # (3 x 4) = (3 x 3) * (3 x 4)
        self.camera_matrix = np.dot(self.intrinsic, self.extrinsic)
        self.debug_matrix("camera matrix", self.camera_matrix)
        
        # homogeneous transpose points
        # (N x 4) <- (N x 3)
        homo_pcd = np.column_stack([pcd, np.ones((pcd.shape[0], 1))])
        # (4 x N)
        homo_trans_pcd = np.transpose(homo_pcd)
        # transform using extrinsic
        # (3 x N) = (3 x 4) * (4 x N)
        self.tf_pcd = np.dot(self.extrinsic, homo_trans_pcd)
        self.debug_matrix("tf homogeneous transpose points", self.tf_pcd)
        
        # normalized pixel coordinate (u, v)
        # (3 x N) = (3 x 3) * (3 x N)
        trans_uv = np.dot(self.intrinsic, self.tf_pcd)
        norm_trans_uv = trans_uv/trans_uv[2,:]
        # (N x 3)
        self.norm_uv = np.transpose(norm_trans_uv)
        self.debug_matrix("normalized pixel coordinate", self.norm_uv)
        
        # projected_points (pixel u, v and depth d)
        self.uvd = self.norm_uv.copy()
        self.uvd[:,2] = np.transpose(self.tf_pcd[2,:])
        self.debug_matrix("projected_points", self.uvd)
        
        return self.uvd
    
    def create_map(self, uvd: np.array):
        
        u_idx, v_idx = uvd[:,0].astype(np.int64), uvd[:,1].astype(np.int64)
        
        max_uvd = np.max(uvd, axis=0)
        min_uvd = np.min(uvd, axis=0)
        self.processor_logger.info("projected image info : "
                                   +"\n max uvd : "+str(max_uvd)
                                   +"\n min uvd : "+str(min_uvd))
        
        # if the maximum width, height, depth of the map < 0
        try:
            if np.any(max_uvd < 0):
                raise InvalidMap
        except Exception as e:
            self.processor_logger.critical("invalid value of map width or height or depth")
            self.processor_logger.exception(e)
            
        
        # round up image width, heigth to the nearest cfg
        self.width = int(np.max(np.ceil(uvd[:,0] / self.cfg_projector['round_up']) * self.cfg_projector['round_up']))
        self.height = int(np.max(np.ceil(uvd[:,1] / self.cfg_projector['round_up']) * self.cfg_projector['round_up']))
        
        # prepare depth map
        self.depth_map = np.zeros((self.height, self.width), dtype=np.float64)
        # create depth map
        for i in range(len(u_idx)):
            if u_idx[i]>=0 and v_idx[i]>=0 and uvd[i,2]>=0: 
                self.depth_map[v_idx[i], u_idx[i]] = max(uvd[i, 2], self.depth_map[v_idx[i], u_idx[i]])
        self.processor_logger.info("created depth map : "+str(self.depth_map.shape))
        
        # prepare heat map
        cmap = plt.cm.get_cmap("jet", 256)
        cmap = np.array(np.array([cmap(i) for i in range(256)])[:,:3]*255, dtype=np.uint8)
        self.heat_map = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # create heat map (method 1)
        """cmap[0] = np.zeros((1,3), dtype=np.uint8) # covert color black in detph 0
        heat_map_mask = self.depth_map.copy()
        cmap_idx_mask = np.array(255*(heat_map_mask) / (max_uvd[2]), dtype=np.uint8)
        self.heat_map = cmap[cmap_idx_mask]"""
        # create heat map (method 2)
        cv, cu = np.where(self.depth_map > 0)
        for v, u in zip(cv, cu):
            depth = self.depth_map[v, u]
            c_idx = int(255 * (depth - min_uvd[2]) / (max_uvd[2]- min_uvd[2]))
            self.heat_map[v, u] = cmap[c_idx]
        self.processor_logger.info("created heat map : "+str(self.heat_map.shape))
            
        return self.depth_map, self.heat_map
        
        
    def projected_depth(self, pcd):

        projected_points = self.project_pcd_to_pixel(pcd)
        depth_map, heat_map = self.create_map(projected_points)
        
        return depth_map, heat_map
        
        
        
        
        