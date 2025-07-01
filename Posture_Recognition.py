import os
import glob
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import calinski_harabasz_score
import re
import shutil
import argparse
import torch
from tqdm import tqdm
import importlib
from test_data import *
from scipy.spatial import cKDTree
import time

def test(model, loader, args,num_class=8, vote_num=1):
    mean_correct = []
    classifier = model.eval()
    class_acc = np.zeros((num_class, 3))
    result = []
    #p1 = ttk.Progressbar(Main_frame,orient=HORIZONTAL,length=100,mode='determinate',bootstyle=PRIMARY)
    #p1.grid(row=3, column=0)
    #p1['maximum'] = len(loader)
    for _, (points, target) in enumerate(loader):
        #p1['value'] = j+1
        #p1.update()
        if not args.use_cpu:
            points, target = points.cuda(), target.cuda()

        points = points.transpose(2, 1)
        #vote_pool = torch.zeros(target.size()[0], num_class).cuda()        
        device = torch.device("cuda" if torch.cuda.is_available() and not args.use_cpu else "cpu")
        vote_pool = torch.zeros(target.size()[0], num_class).to(device)#灵活选择cpu或者gpu

        for _ in range(vote_num):
            pred, _ = classifier(points)
            vote_pool += pred
        pred = vote_pool / vote_num
        pred_choice = pred.data.max(1)[1]   
        result.extend(pred_choice)
        result = list(map(int, result))
    #p1.destroy()
    return result


def count_non_empty_lines(file_path):#统计文本文件中非空行的数量
    """
    统计文本文件中非空行的数量
    :param file_path: 文件路径
    :return: 非空行数量
    """
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # 过滤空行（包括只有空格的行）
                count += 1
    return count


def Human_Posture_Recognition(Model_path,args,file,floder): #人体姿态识别

    '''CREATE DIR'''
    experiment_dir = Model_path

    test_dataset = test_data(file,floder, args=args)
    #test_dataset = ModelNetDataLoader(root=data_path, args=args, split='test', process_data=False)
    testDataLoader = torch.utils.data.DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)

    '''MODEL LOADING'''
    num_class = args.num_category
    model_name = os.listdir(experiment_dir + '/logs')[0].split('.')[0]
    model = importlib.import_module(model_name)

    classifier = model.get_model(num_class, normal_channel=args.use_normals)
    if not args.use_cpu:
        classifier = classifier.cuda()

    checkpoint = torch.load((str(experiment_dir) + '/checkpoints/best_model.pth'), weights_only=False)#读取训练好的模型
    classifier.load_state_dict(checkpoint['model_state_dict'])

    result = []
    with torch.no_grad():
        num = 0
        for i in test(classifier.eval(), testDataLoader,args,vote_num=args.num_votes, num_class=num_class):
            key = test_dataset.datapath[num][1]
            num  = num + 1
            value = list(test_dataset.classes.keys())[list(test_dataset.classes.values()).index(i)]
            if value.count('_') == 1:
                # 分割字符串并获取 _ 后面的部分
                parts = value.split('_')
                value=parts[1]
            file_name = key.split('\\')[1]
            result.append([file_name,value])
    return result


def Multi_frame_fusion(start_file,name,source_folder, destination_folder,num_frame,name_file): #将点云数据进行多帧融合
    # 获取源文件夹中所有以数字结尾的 txt 文件
    txt_files = sorted(glob.glob(os.path.join(source_folder, '*[0-9].txt')))
    
    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # 每 num_frame 个文件一组进行合并
    for i in range(start_file, start_file + num_frame, num_frame):
        group = txt_files[i:i + num_frame]
        merged_content = ''
        for file in group:
            with open(file, 'r', encoding='utf-8') as f:
                merged_content += f.read()
                if merged_content[-1] != '\n':  # 如果文件不以换行符结尾，添加一个换行符
                    merged_content += '\n'
        
        # 生成新的文件名
        new_file_name = os.path.join(destination_folder, f'{name_file}_{name}.txt')
        with open(new_file_name, 'w', encoding='utf-8') as f:
            f.write(merged_content)

def Dynamic_interference_filtering(name,num_frame,input_folder,output_folder,a,b,c,d): #点云数据分割
    input_file_path = os.path.join(input_folder, f"MFF_{num_frame}_{name}.txt")
    output_file_path = os.path.join(output_folder, f"DIF_{num_frame}_{name}.txt")
    # 打开输入文件
    valid_lines = []
    with open(input_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                # 分割每行内容为数字列表
                nums = [float(num) for num in line.strip().split(' ')]
                print(f"a = {a}, b = {b}, c = {c} , d = {d} ,nums[0] = {nums[0]}, nums[1] = {nums[1]} ")
                # 检查是否有三个数字，并且是否满足条件
                if len(nums) == 3 and a <= nums[0] and nums[0] <= b and c <= nums[1] and nums[1] <= d:
                    valid_lines.append(line)
            except ValueError:
                # 若无法转换为数字，则跳过该行
                continue

        # 将符合条件的行写入输出文件
        if valid_lines:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.writelines(valid_lines)

def FDBSCAN(file_path,output_file_path,eps,min_samples):
    try:
        data = pd.read_csv(file_path, header=None, delimiter=' ')
        points = data.values.tolist()

        db = DBSCAN(eps=eps, min_samples=min_samples).fit(points)

        filtered_points = [point for point, label in zip(points,db.labels_) if label != -1]
        df = pd.DataFrame(filtered_points)
        df.to_csv(output_file_path, header=False, index=False, sep=' ')

    except Exception as e:
        print("错误", f"处理文件 {file_path} 时出错: {e}")

def read_point_cloud(file_path): #    从 TXT 文件读取点云数据
    """
    从 TXT 文件读取点云数据
    :param file_path: 输入的 TXT 文件路径
    :return: 包含点云数据的 numpy 数组，每行代表一个点的 (x, y, z) 坐标
    """
    try:
        return np.loadtxt(file_path)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查路径。")
        return np.empty((0, 3))
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return np.empty((0, 3))

def adjust_point_cloud_file(points, target_lines):#对点云进行上采样
    """
    调整点云文件的行数到指定数量。

    :param input_file_path: 输入的点云文件路径
    :param output_file_path: 输出的点云文件路径
    :param target_lines: 目标行数
    """
    try:
        # 读取输入文件
        current_lines = len(points)

        if current_lines < target_lines:
            # 若当前行数小于目标行数，随机复制点云
            num_to_add = target_lines - current_lines
            random_indices = np.random.choice(current_lines, num_to_add)
            additional_points = points[random_indices]
            new_points = np.vstack((points, additional_points))
        else:
            new_points = points

        # 保存新的点云数据到输出文件
        return new_points
    
    except FileNotFoundError:
        print(f"输入文件未找到。")
    except Exception as e:
        print(f"发生错误: {e}")

def random_downsample(points, target_num_points):#对点云进行随机下采样
    """
    对输入的点云数据进行随机下采样
    :param points: 原始点云数据的 numpy 数组
    :param target_num_points: 目标点云数量
    :return: 下采样后的点云数据的 numpy 数组
    """
    if len(points) <= target_num_points:
        return points
    indices = np.random.choice(len(points), target_num_points, replace=False)
    return points[indices]

def process_point_cloud(points, target_num_points):#根据点云数量决定上采样或下采样
    """
    根据点云数量决定上采样或下采样
    :param points: 原始点云数据的 numpy 数组
    :param target_num_points: 目标点云数量
    :return: 处理后的点云数据的 numpy 数组
    """
    if len(points) < target_num_points:
        return adjust_point_cloud_file(points, target_num_points)
    else:
        return random_downsample(points, target_num_points)

def process_folder(input_file_path,output_file_path, target_num_points):#点云上采样/下采样

    points = read_point_cloud(input_file_path)

    processed_points = process_point_cloud(points, target_num_points)

    np.savetxt(output_file_path, processed_points, fmt='%.6f', delimiter=' ')

def Posture_Recognition(Current_File,file_number_20,file_number_40,file_number_60,file_number_80,eps,min_samples,target_num_points,Rate_20,Rate_40,Rate_60,Rate_80,PATH):
    
    parser = argparse.ArgumentParser('Testing')
    parser.add_argument('--use_cpu', action='store_true', default=True, help='use cpu mode')
    parser.add_argument('--gpu', type=str, default='0', help='specify gpu device')
    parser.add_argument('--batch_size', type=int, default=8, help='batch size in training')
    parser.add_argument('--num_category', default=5, type=int, choices=[5,8,10],  help='training on ModelNet10/40')
    parser.add_argument('--num_point', type=int, default=1024, help='Point Number')
    #parser.add_argument('--log_dir', type=str,required=True, help='Experiment root')
    parser.add_argument('--log_dir', type=str,default="2025-04-08_14-41", help='Experiment root')
    parser.add_argument('--use_normals', action='store_true', default=False, help='use normals')
    parser.add_argument('--use_uniform_sample', action='store_true', default=False, help='use uniform sampiling')
    parser.add_argument('--num_votes', type=int, default=3, help='Aggregate classification scores with voting')
    args_I = parser.parse_args()
    try:
        if Rate_20:
            print(f"开始20帧率识别,Current_File = {Current_File},file_number_20 = {file_number_20}")
            Multi_frame_fusion(Current_File - 20,file_number_20 - 2,".\\Cloud_File", ".\\Rate_20_MFF",20,"MFF_20")
            if os.path.isfile(f".\\Rate_20_MFF\\MFF_20_{file_number_20 - 2}.txt"):
                FDBSCAN(f".\\Rate_20_MFF\\MFF_20_{file_number_20 - 2}.txt",f".\\Rate_20_DBSCAN\\DBSCAN_20_{file_number_20 - 2}.txt",eps,min_samples)
                if count_non_empty_lines(f".\\Rate_20_DBSCAN\\DBSCAN_20_{file_number_20 - 2}.txt") > 0 :
                    process_folder(f".\\Rate_20_DBSCAN\\DBSCAN_20_{file_number_20 - 2}.txt", f".\\Rate_20_Sampling\\Sampling_20_{file_number_20 - 2}.txt", target_num_points)
                    if count_non_empty_lines(f".\\Rate_20_Sampling\\Sampling_20_{file_number_20 - 2}.txt") > 0 :
                        result_20 = Human_Posture_Recognition(PATH[0],args_I,".\\attitude.txt",".\\Rate_20_Sampling")
                        for filename in os.listdir(".\\Rate_20_Sampling"):
                            file_path = os.path.join(".\\Rate_20_Sampling", filename)
                        try:
                            # 如果是文件或符号链接，直接删除
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                            # 如果是子文件夹，递归删除其内容
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except Exception as e:
                            print(f"删除失败: {file_path} - 错误原因: {e}")
                        return result_20[0][1]
                    else:
                        return None
                else:
                    return None
            else:
                return None

        if Rate_40:
            print(f"开始40帧率识别,Current_File = {Current_File},file_number_40 = {file_number_40}")
            Multi_frame_fusion(Current_File - 40,file_number_40 - 2,".\\Cloud_File", ".\\Rate_40_MFF",40,"MFF_40")
            if os.path.isfile(f".\\Rate_40_MFF\\MFF_40_{file_number_40 - 2}.txt"):
                FDBSCAN(f".\\Rate_40_MFF\\MFF_40_{file_number_40 - 2}.txt",f".\\Rate_40_DBSCAN\\DBSCAN_40_{file_number_40 - 2}.txt",eps,min_samples)
                if count_non_empty_lines(f".\\Rate_40_DBSCAN\\DBSCAN_40_{file_number_40 - 2}.txt") > 0 :
                    process_folder(f".\\Rate_40_DBSCAN\\DBSCAN_40_{file_number_40 - 2}.txt", f".\\Rate_40_Sampling\\Sampling_40_{file_number_40 - 2}.txt", target_num_points)
                    if count_non_empty_lines(f".\\Rate_40_Sampling\\Sampling_40_{file_number_40 - 2}.txt") > 0 :  
                        result_40 = Human_Posture_Recognition(PATH[1],args_I,".\\attitude.txt",".\\Rate_40_Sampling")
                        for filename_2 in os.listdir(".\\Rate_40_Sampling"):
                            file_path_2= os.path.join(".\\Rate_40_Sampling", filename_2)
                        try:
                            # 如果是文件或符号链接，直接删除
                            if os.path.isfile(file_path_2) or os.path.islink(file_path_2):
                                os.unlink(file_path_2)
                            # 如果是子文件夹，递归删除其内容
                            elif os.path.isdir(file_path_2):
                                shutil.rmtree(file_path_2)
                        except Exception as e:
                            print(f"删除失败: {file_path_2} - 错误原因: {e}")
                        return result_40[0][1]
                    else:
                        return None
                else:
                    return None
            else:
                return None

        if Rate_60:
            print(f"开始60帧率识别,Current_File = {Current_File},file_number_60 = {file_number_60}")
            Multi_frame_fusion(Current_File - 60,file_number_60 - 2,".\\Cloud_File", ".\\Rate_60_MFF",60,"MFF_60")
            if os.path.isfile(f".\\Rate_60_MFF\\MFF_60_{file_number_60 - 2}.txt"):
                FDBSCAN(f".\\Rate_60_MFF\\MFF_60_{file_number_60 - 2}.txt",f".\\Rate_60_DBSCAN\\DBSCAN_60_{file_number_60 - 2}.txt",eps,min_samples)
                if count_non_empty_lines(f".\\Rate_60_DBSCAN\\DBSCAN_60_{file_number_60 - 2}.txt") > 0 :
                    process_folder(f".\\Rate_60_DBSCAN\\DBSCAN_60_{file_number_60 - 2}.txt", f".\\Rate_60_Sampling\\Sampling_60_{file_number_60 - 2}.txt", target_num_points)
                    if count_non_empty_lines(f".\\Rate_60_Sampling\\Sampling_60_{file_number_60 - 2}.txt") > 0 :  
                        result_60 = Human_Posture_Recognition(PATH[2],args_I,".\\attitude.txt",".\\Rate_60_Sampling")
                        for filename_3 in os.listdir(".\\Rate_60_Sampling"):
                            file_path_3= os.path.join(".\\Rate_60_Sampling", filename_3)
                        try:
                            # 如果是文件或符号链接，直接删除
                            if os.path.isfile(file_path_3) or os.path.islink(file_path_3):
                                os.unlink(file_path_3)
                            # 如果是子文件夹，递归删除其内容
                            elif os.path.isdir(file_path_3):
                                shutil.rmtree(file_path_3)
                        except Exception as e:
                            print(f"删除失败: {file_path_3} - 错误原因: {e}")
                        return result_60[0][1]
                    else: 
                        return None
                else:
                    return None
            else:
                return None
    



        if Rate_80:
            print(f"开始80帧率识别,Current_File = {Current_File},file_number_80 = {file_number_80}")
            Multi_frame_fusion(Current_File - 80,file_number_80 - 2,".\\Cloud_File", ".\\Rate_80_MFF",80,"MFF_80")
            if os.path.isfile(f".\\Rate_80_MFF\\MFF_80_{file_number_80 - 2}.txt"):
                FDBSCAN(f".\\Rate_80_DIF\\DIF_80_{file_number_80 - 2}.txt",f".\\Rate_80_DBSCAN\\DBSCAN_80_{file_number_80 - 2}.txt",eps,min_samples)
                if count_non_empty_lines(f".\\Rate_80_DBSCAN\\DBSCAN_80_{file_number_80 - 2}.txt") > 0 :
                    process_folder(f".\\Rate_80_DBSCAN\\DBSCAN_80_{file_number_80 - 2}.txt", f".\\Rate_80_Sampling\\Sampling_80_{file_number_80 - 2}.txt", target_num_points)
                    if count_non_empty_lines(f".\\Rate_80_Sampling\\Sampling_80_{file_number_80 - 2}.txt") > 0 :  
                        result_80 = Human_Posture_Recognition(PATH[3],args_I,".\\attitude.txt",".\\Rate_80_Sampling")
                        for filename_4 in os.listdir(".\\Rate_80_Sampling"):
                            file_path_4 = os.path.join(".\\Rate_80_Sampling", filename_4)
                        try:
                            # 如果是文件或符号链接，直接删除
                            if os.path.isfile(file_path_4) or os.path.islink(file_path_4):
                                os.unlink(file_path_4)
                            # 如果是子文件夹，递归删除其内容
                            elif os.path.isdir(file_path_4):
                                shutil.rmtree(file_path_4)
                        except Exception as e:
                            print(f"删除失败: {file_path_4} - 错误原因: {e}")
                        return result_80[0][1]
                    else:
                        return None
                else:
                    return None
            else:
                return None
    except Exception as e:
        print("err = " + str(e))