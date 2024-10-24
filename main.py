import config
import data_manager
import data_processor


def main():

    cfg = config.Config(config_path="./config.yaml")

    manager = data_manager.DataManager(cfg)
    pcd = manager.read_pcd()
    # manager.draw_pcd(pcd)

    processor = data_processor.DataProcessor(cfg)
    filtered = processor.filter(pcd)
    manager.save_pcd(filtered)
    # manager.draw_pcd(filtered)

    depth_map, heat_map = processor.project_pcd(pcd)
    manager.save_depth(depth_map)
    manager.save_heat(heat_map)
    manager.show_img(heat_map)
    
if __name__ == "__main__":
    main()