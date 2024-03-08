from shutil import copyfile
import os
from pathlib import Path
import argparse

def main(args):

    exp_name = args.exp_name
    case = args.case
    conf_path = args.conf_path

    exps_dir = Path(args.exp_path) / exp_name / case / Path(conf_path).stem
    prev_exps = sorted(exps_dir.iterdir())
    cur_dir = prev_exps[-1].name      

    path_to_mesh = os.path.join(exps_dir, cur_dir, 'meshes')
    path_to_ckpt = os.path.join(exps_dir, cur_dir, 'checkpoints')
    path_to_fitted_camera = os.path.join(exps_dir, cur_dir, 'cameras')

    meshes = sorted(os.listdir(path_to_mesh))

    last_ckpt = sorted(os.listdir(path_to_ckpt))[-1]

    last_hair = [i for i in meshes if i.split('_')[-1].split('.')[0]=='hair'][-1]
    last_head = [i for i in meshes if i.split('_')[-1].split('.')[0]=='head'][-1]

    path_to_data = args.path_to_data
    scene_type = args.scene_type
    
    
    print(f'Copy obtained from the first stage checkpoint, hair and head geometry to folder {path_to_data}/{scene_type}/{case}')
    

    print(path_to_data, os.path.join(path_to_mesh, last_hair), f'{path_to_data}/{scene_type}/{case}/final_hair.ply')

    
    copyfile(os.path.join(path_to_mesh, last_hair), f'{path_to_data}/{scene_type}/{case}/final_hair.ply')
    copyfile(os.path.join(path_to_mesh, last_head), f'{path_to_data}/{scene_type}/{case}/final_head.ply')
    copyfile(os.path.join(path_to_ckpt, last_ckpt), f'{path_to_data}/{scene_type}/{case}/ckpt_final.pth')

    if os.path.exists(path_to_fitted_camera):
        print(f'Copy obtained from the first stage camera fitting checkpoint to folder {path_to_data}/{scene_type}/{case}')
        last_camera = sorted(os.listdir(path_to_fitted_camera))[-1]
        copyfile(os.path.join(path_to_fitted_camera, last_camera), f'{path_to_data}/{scene_type}/{case}/fitted_cameras.pth')


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(conflict_handler='resolve')

    parser.add_argument('--conf_path', default='./configs/example_config/monocular/neural_strands-monocular.yaml', type=str)
    
    parser.add_argument('--case', default='person_1', type=str)
       
    parser.add_argument('--exp_name', default='first_stage_reconctruction_person_1', type=str)  
    
    parser.add_argument('--exp_path', default='./exps_first_stage', type=str) 
    
    parser.add_argument('--scene_type', default='monocular', type=str, choices=['h3ds', 'monocular']) 
    
    parser.add_argument('--path_to_data', default='./implicit-hair-data/data/', type=str)  

    
    args, _ = parser.parse_known_args()
    args = parser.parse_args()

    main(args)