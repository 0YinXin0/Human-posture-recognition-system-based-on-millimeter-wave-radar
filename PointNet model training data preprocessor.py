from test_data import *
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import ttkthemes
from tkinter import *
import os
import glob
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import calinski_harabasz_score
import tkinter.messagebox
from tkinter import filedialog
from tqdm import tqdm
import torch
import argparse
import importlib
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.scrolled import ScrolledText
import shutil


file_path_1 = " " #选择雷达的原始输出文件
file_path_2 = " " #选择动作类别信息的文件
file_path_3 = " " #选择要查看的点云文件
file_path_4 = " " #选择SR75雷达输出的文件
folder_path_1 = " " #选择雷达的原始数据处理的输出文件夹
folder_path_2 = " " #要多帧融合的文件夹
folder_path_3 = " " #多帧融合的输出文件夹
folder_path_4 = " " #点云数据分割的输入文件夹
folder_path_5 = " " #点云数据分割的输出文件夹
folder_path_6 = " " #DBSCAN的输入文件夹
folder_path_7 = " " #DBSCAN的输出文件夹
folder_path_8 = " " #点云采样的输入文件夹
folder_path_9 = " " #点云采样的输出文件夹
folder_path_10 = " " #点云数量评估的输入文件夹
folder_path_11 = " " #模型所在的文件夹
folder_path_12 = " " #测试文件所在的文件夹
folder_path_13 = " " #训练模型所用的数据集的文件夹

text1_entry = "" #SR75雷达原始输出文件转换后的文件的前缀名
text2_entry = "" #多帧融合的帧数
text3_entry = "" #多帧融合和输出文件的文件名前缀
text4_entry = "" #点云数据分割的X坐标的最小值
text5_entry = "" #点云数据分割的X坐标的最大值
text6_entry = "" #点云数据分割的Y坐标的最小值
text7_entry = "" #点云数据分割的Y坐标的最大值
text8_entry = "" #点云数据分割的输出文件的前缀名
text9_entry = "" #点云采样的目标点云数量
text10_entry = "" #DBSCAN的eps
text11_entry = "" #DBSCAN的min_samples
text12_entry = ""


def select_folder(): #选择文件夹
    folder_path = filedialog.askdirectory()
    return folder_path




def select_file_1(): #选择雷达的原始输出文件
    global file_path_1
    file_path_1 = filedialog.askopenfilename()


def select_file_2(): #选择姿态信息的文件
    global file_path_2
    file_path_2 = filedialog.askopenfilename()

def select_file_3(): #选择要查看的点云文件
    global file_path_3
    file_path_3 = filedialog.askopenfilename()

def select_file_4(): #选择SR75雷达输出的文件
    global file_path_4
    file_path_4 = filedialog.askopenfilename()
def select_folder_1(): #选择原始数据处理后的输出文件夹
    global folder_path_1
    folder_path_1 = filedialog.askdirectory()

def select_folder_2(): #要多帧融合的文件夹
    global folder_path_2
    folder_path_2 = filedialog.askdirectory()

def select_folder_3(): #多帧融合的输出文件夹
    global folder_path_3
    folder_path_3 = filedialog.askdirectory()

def select_folder_4(): #点云数据分割的输入文件夹
    global folder_path_4
    folder_path_4 = filedialog.askdirectory()

def select_folder_5(): #点云数据分割的输出文件夹
    global folder_path_5
    folder_path_5 = filedialog.askdirectory()

def select_folder_6(): #要DBSCAN的文件夹
    global folder_path_6
    folder_path_6 = filedialog.askdirectory()

def select_folder_7(): #DBSCAN的输出文件夹
    global folder_path_7
    folder_path_7 = filedialog.askdirectory()

def select_folder_8(): #点云采样的输入文件夹
    global folder_path_8
    folder_path_8 = filedialog.askdirectory()

def select_folder_9(): #点云采样的输出文件夹
    global folder_path_9
    folder_path_9 = filedialog.askdirectory()

def select_folder_10(): #点云采样的输出文件夹
    global folder_path_10
    folder_path_10 = filedialog.askdirectory()

def select_folder_11(): #选择模型所在的文件夹
    global folder_path_11
    folder_path_11 = filedialog.askdirectory()


def select_folder_12(): #选择测试文件所在的文件夹
    global folder_path_12
    folder_path_12 = filedialog.askdirectory()

def select_folder_13(): #选择训练模型所用的数据集的文件夹
    global folder_path_13
    folder_path_13 = filedialog.askdirectory()

def get_point_clouds(input_file_path, output_folder,file_name): #将原始数据处理后的输出文件进行处理，将数据块分割成点云
    try:
        # 读取输入文件
        with open(input_file_path, 'r') as file:
            content = file.read()

        # 按数据块分割内容
        data_blocks = content.split('xyz_data')

        # 处理每个数据块
        for i, block in enumerate(data_blocks):
            block = block.strip()
            if block:
                data_lines = []
                for line in block.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('*'):
                        # 提取 x, y, z 的值
                        x_start = line.find('x =') + 4
                        x_end = line.find(',', x_start)
                        x = line[x_start:x_end]

                        y_start = line.find('y =') + 4
                        y_end = line.find(',', y_start)
                        y = line[y_start:y_end]

                        z_start = line.find('z =') + 4
                        z_end = line.find(',', z_start)                     
                        z = line[z_start:z_end]

                        data_lines.append(f"{x} {y} {z}")

                if data_lines:
                    # 创建输出文件
                    output_file_path = f"{output_folder}/{file_name}_{i-1}.txt"
                    with open(output_file_path, 'w') as output_file:
                        output_file.write('\n'.join(data_lines))
        if not state_step2:
            tk.messagebox.showinfo(title='完成!',message='将雷达的原始输出转化为点云数据成功。')
    except FileNotFoundError:
        print(f"输入文件 {input_file_path} 未找到。")
        tk.messagebox.showinfo(title='错误!',message=f"输入文件 {input_file_path} 未找到。")
    except Exception as e:
        print(f"发生错误: {e}")
        tk.messagebox.showinfo(title='错误!',message=f"发生错误: {e}")

def Multi_frame_fusion(source_folder, destination_folder,num_frame,name_file): #将点云数据进行多帧融合
    # 获取源文件夹中所有以数字结尾的 txt 文件
    txt_files = sorted(glob.glob(os.path.join(source_folder, '*[0-9].txt')))
    
    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # 每 num_frame 个文件一组进行合并
    for i in range(0, len(txt_files), num_frame):
        group = txt_files[i:i + num_frame]
        merged_content = ''
        for file in group:
            with open(file, 'r', encoding='utf-8') as f:
                merged_content += f.read()
                if merged_content[-1] != '\n':  # 如果文件不以换行符结尾，添加一个换行符
                    merged_content += '\n'
        
        # 生成新的文件名
        new_file_name = os.path.join(destination_folder, f'{name_file}_{i//num_frame + 1}.txt')
        with open(new_file_name, 'w', encoding='utf-8') as f:
            f.write(merged_content)
    if not state_step2:
        tk.messagebox.showinfo(title='完成!',message='多帧融合完毕。')


def Dynamic_interference_filtering(input_folder,output_folder,file_name,a,b,c,d): #点云数据分割
    # 遍历输入文件夹中的所有文件
    index = 0
    for filename in os.listdir(input_folder):
        # 只处理 txt 文件
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            output_filename = f'{file_name}_{index:02d}.txt'
    # 若输出文件夹不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    index = 0
    for filename in os.listdir(input_folder):
        # 只处理 txt 文件
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            output_filename = f'{file_name}_{index:02d}.txt'
            output_file_path = os.path.join(output_folder, output_filename)
            valid_lines = []

            # 打开输入文件
            with open(input_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        # 分割每行内容为数字列表
                        nums = [float(num) for num in line.strip().split(' ')]
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
                index += 1
    if not state_step2:
        tk.messagebox.showinfo(title='完成!',message='点云数据分割完毕。')


def FDBSCAN(input_folder_path,output_folder_path,eps,min_samples):
    if not input_folder_path or not output_folder_path:
        tk.messagebox.showwarning("警告", "请选择输入文件夹和输出文件夹。")
        return

    all_files = []
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    if not all_files:
        tk.messagebox.showwarning("警告", "未找到有效的 TXT 文件。")
        return

    for file_path in all_files:
        try:
            data = pd.read_csv(file_path, header=None, delimiter=' ')
            points = data.values.tolist()

            db = DBSCAN(eps=eps, min_samples=min_samples).fit(points)

            filtered_points = [point for point, label in zip(points,db.labels_) if label != -1]
            df = pd.DataFrame(filtered_points)

            output_file_name = os.path.basename(file_path)
            output_file_path = os.path.join(output_folder_path, output_file_name)
            df.to_csv(output_file_path, header=False, index=False, sep=' ')

        except Exception as e:
            tk.messagebox.showerror("错误", f"处理文件 {file_path} 时出错: {e}")
    if not state_step2:
        tk.messagebox.showinfo("完成", "DBSCAN所有文件处理完成。")

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


def process_folder(input_folder, output_folder, target_num_points):#点云上采样/下采样
    """
    处理输入文件夹中的所有 TXT 点云文件，进行上采样或下采样并保存到输出文件夹
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    :param target_num_points: 目标点云数量
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.txt'):
                input_file_path = os.path.join(root, file)
                points = read_point_cloud(input_file_path)
                if points.size == 0:
                    tk.messagebox.showinfo("注意",f"跳过文件 {input_file_path}，未成功读取到点云数据。")
                    continue

                processed_points = process_point_cloud(points, target_num_points)

                output_file_path = os.path.join(output_folder, file)
                np.savetxt(output_file_path, processed_points, fmt='%.6f', delimiter=' ')
                print(f"处理后的点云数据已保存到 {output_file_path}")
    if not state_step2:
        tk.messagebox.showinfo("完成", f"采样完成。")




def count_lines_in_txt_files(input_dir):#点云数量/密度评估
    results = []
    line_counts = []
    # 遍历输入文件夹下的所有文件和子文件夹
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    # 以只读模式打开文件并统计行数
                    with open(file_path, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for _ in f)
                        results.append(f'{file}:{line_count}')
                        line_counts.append(line_count)
                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {e}")

    if line_counts:
        average_lines = sum(line_counts) / len(line_counts)
        max_lines = max(line_counts)
        min_lines = min(line_counts)
        results.append(f'\n平均行数: {average_lines}')
        results.append(f'最大行数: {max_lines}')
        results.append(f'最小行数: {min_lines}')
        tk.messagebox.showinfo("完成", f"点云数量/密度评估完成。\n平均行数: {average_lines}。 \n 最大行数: {max_lines}。 \n 最小行数: {min_lines}。")
    else:
        results.append('\n未找到符合条件的txt文件')













def visualize_point_cloud(points):
    """
    可视化点云数据。

    :param points: 包含点云数据的numpy数组，形状为 (n, 3)
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1)  # 绘制点云
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()




#////窗口部分

# 创建主窗口,窗口布局

root = ttk.Window(
        title="人体姿态识别PointNet++模型训练数据预处理点云数据系统",        #设置窗口的标题
        themename="cerculean",     #设置主题
        size=(1200,800),        #窗口的大小
        position=(700,200),     #窗口所在的位置
        minsize=(0,0),          #窗口的最小宽高
        maxsize=(1920,1080),    #窗口的最大宽高
        resizable=None,         #设置窗口是否可以更改大小
        alpha=1.0,              #设置窗口的透明度(0.0完全透明）
        )



main_menu = ttk.Menu(root)




def create__window_SR75_point_cloud_data(): #创建将雷达原始输出文件数据转为点云文件功能的子窗口
    window_SR75_point_cloud_data = ttk.Toplevel()
    window_SR75_point_cloud_data.title("将雷达原始输出文件数据转为点云文件")

    ttk.Label(window_SR75_point_cloud_data,text="雷达文件读取/点云输出路径:",bootstyle=INFO).grid(row=0, column=0)
    ttk.Button(window_SR75_point_cloud_data, text="选择输入文件", command=select_file_1,bootstyle=(INFO, OUTLINE)).grid(row=0, column=1)
    ttk.Button(window_SR75_point_cloud_data, text="选择输出文件夹", command=select_folder_1,bootstyle=(INFO, OUTLINE)).grid(row=0, column=2)
    ttk.Label(window_SR75_point_cloud_data,text="输出的文件的前缀名:",bootstyle=INFO).grid(row=1, column=0)   
    text1_entry = ttk.Entry(window_SR75_point_cloud_data,width=10,bootstyle="dark")
    text1_entry.grid(row=1, column=1)
    def convert_button_1(): #将SR75雷达的输出文件转换到点云文件的功能
        get_point_clouds(file_path_1,folder_path_1,text1_entry.get())
    ttk.Button(window_SR75_point_cloud_data, text="读取点云数据", command=convert_button_1,bootstyle=(INFO, OUTLINE)).grid(row=2, column=1)

    window_SR75_point_cloud_data.mainloop()

def create__window_Data_segmentation(): #创建点云数据分割功能的子窗口
    window_Data_segmentation = ttk.Toplevel()
    window_Data_segmentation.title("点云数据分割")

    ttk.Label(window_Data_segmentation,text="文件读取/输出路径:",bootstyle=INFO).grid(row=0, column=0)
    ttk.Button(window_Data_segmentation, text="选择输入文件夹", command=select_folder_4,bootstyle=(INFO, OUTLINE)).grid(row=0, column=1)
    ttk.Button(window_Data_segmentation, text="选择输出文件夹", command=select_folder_5,bootstyle=(INFO, OUTLINE)).grid(row=0, column=2)
    ttk.Label(window_Data_segmentation, text="要提取的点云坐标范围:",bootstyle=INFO).grid(row=1, column=0)
    
    text4_entry = ttk.Entry(window_Data_segmentation,width=5,bootstyle="dark")
    text4_entry.grid(row=2, column=0)
    ttk.Label(window_Data_segmentation, text="<= X <=").grid(row=2, column=1)
    text5_entry = ttk.Entry(window_Data_segmentation, width=5,bootstyle="dark")
    text5_entry.grid(row=2, column=2)
    text6_entry = ttk.Entry(window_Data_segmentation, width=5,bootstyle="dark")
    text6_entry.grid(row=3, column=0)
    ttk.Label(window_Data_segmentation, text="<= Y <=").grid(row=3, column=1)
    text7_entry = ttk.Entry(window_Data_segmentation, width=5,bootstyle="dark")
    text7_entry.grid(row=3, column=2)
    ttk.Label(window_Data_segmentation, text="输出的文件的前缀名:").grid(row=4, column=0)
    text8_entry = ttk.Entry(window_Data_segmentation, width=10,bootstyle="dark")
    text8_entry.grid(row=4, column=1)
    def convert_button_3(): #点云数据分割
        Dynamic_interference_filtering(folder_path_4, folder_path_5,text8_entry.get(),float(text4_entry.get()),float(text5_entry.get()),float(text6_entry.get()),float(text7_entry.get()))
    ttk.Button(window_Data_segmentation, text="点云数据分割", command=convert_button_3,bootstyle=(INFO, OUTLINE)).grid(row=5, column=1)

    window_Data_segmentation.mainloop()


def create_window_Multi_frame_fusion(): #创建多帧融合功能的子窗口
    window_Multi_frame_fusion = ttk.Toplevel()
    window_Multi_frame_fusion.title("点云数据多帧融合") 
    ttk.Label(window_Multi_frame_fusion,text="文件读取/输出路径:",bootstyle=INFO).grid(row=0, column=0)
    ttk.Button(window_Multi_frame_fusion, text="选择输入文件夹", command=select_folder_2,bootstyle=(INFO, OUTLINE)).grid(row=0, column=1)
    ttk.Button(window_Multi_frame_fusion, text="选择输出文件夹", command=select_folder_3,bootstyle=(INFO, OUTLINE)).grid(row=0, column=2)
    text2_entry = ttk.Entry(window_Multi_frame_fusion, width=10,bootstyle="dark")
    ttk.Label(window_Multi_frame_fusion,text="请输入融合的帧数:",bootstyle=INFO).grid(row=1, column=0)    
    text2_entry.grid(row=1, column=1)
    text3_entry = ttk.Entry(window_Multi_frame_fusion, width=10,bootstyle="dark")
    ttk.Label(window_Multi_frame_fusion,text="输出的文件的前缀名:",bootstyle=INFO).grid(row=2, column=0)    
    text3_entry.grid(row=2, column=1)    
    def convert_button_2(): #将点云数据进行多帧融合
        Multi_frame_fusion(folder_path_2, folder_path_3,int(text2_entry.get()),text3_entry.get())
    ttk.Button(window_Multi_frame_fusion, text="多帧融合", command=convert_button_2,bootstyle=(INFO, OUTLINE)).grid(row=3, column=1)
    
    window_Multi_frame_fusion.mainloop()

def create_window_DBSCAN(): #创建DBSCAN功能的子窗口
    window_DBSCAN = ttk.Toplevel()
    window_DBSCAN.title("DBSCAN") 
    ttk.Label(window_DBSCAN,text="文件读取/输出路径:",bootstyle=INFO).grid(row=0, column=0)
    ttk.Button(window_DBSCAN, text="选择输入文件夹", command=select_folder_6,bootstyle=(INFO, OUTLINE)).grid(row=0, column=1)
    ttk.Button(window_DBSCAN, text="选择输出文件夹", command=select_folder_7,bootstyle=(INFO, OUTLINE)).grid(row=0, column=2)
    ttk.Label(window_DBSCAN,text="请输入eps:",bootstyle=INFO).grid(row=1, column=0)   
    text10_entry = ttk.Entry(window_DBSCAN, width=5,bootstyle="dark")
    text10_entry.grid(row=1, column=1)
    ttk.Label(window_DBSCAN,text="请输入Min_Pts:",bootstyle=INFO).grid(row=2, column=0)
    text11_entry = ttk.Entry(window_DBSCAN, width=5,bootstyle="dark")
    text11_entry.grid(row=2, column=1)
    def convert_button_4(): #DBSCAN
        FDBSCAN(folder_path_6,folder_path_7,float(text10_entry.get()),int(text11_entry.get()))
    ttk.Button(window_DBSCAN, text="DBSCAN", command=convert_button_4,bootstyle=(INFO, OUTLINE)).grid(row=3, column=1)

    window_DBSCAN.mainloop()

def create_window_Sampling(): #创建点云文件采样功能的子窗口
    window_Sampling = ttk.Toplevel()
    window_Sampling.title("点云文件采样")
    ttk.Label(window_Sampling,text="文件读取/输出路径:",bootstyle=INFO).grid(row=0, column=0)
    ttk.Button(window_Sampling, text="选择输入文件夹", command=select_folder_8,bootstyle=(INFO, OUTLINE)).grid(row=0, column=1)
    ttk.Button(window_Sampling, text="选择输出文件夹", command=select_folder_9,bootstyle=(INFO, OUTLINE)).grid(row=0, column=2)
    text9_entry = ttk.Entry(window_Sampling, width=10)
    ttk.Label(window_Sampling,text="采样后的点云数量:",bootstyle=INFO).grid(row=1, column=0)
    text9_entry.grid(row=1, column=1)
    def convert_button_5(): #点云采样按钮
        process_folder(folder_path_8, folder_path_9, int(text9_entry.get()))
    ttk.Button(window_Sampling, text="采样", command=convert_button_5,bootstyle=(INFO, OUTLINE)).grid(row=2, column=2)

    window_Sampling.mainloop()

def create_window_quantity_density_evaluation(): #创建点云文件点云数量/点云密度评估功能的子窗口
    window_quantity_density_evaluation = ttk.Toplevel()
    window_quantity_density_evaluation.title("点云文件点云数量/点云密度评估") 
    ttk.Button(window_quantity_density_evaluation, text="选择要评估的文件夹", command=select_folder_10,bootstyle=(INFO, OUTLINE)).grid(row=0, column=0)
    def convert_button_6(): #点云数量/密度评估按钮
        count_lines_in_txt_files(folder_path_10)
    ttk.Button(window_quantity_density_evaluation, text="评估", command=convert_button_6,bootstyle=(INFO, OUTLINE)).grid(row=0, column=1)

    window_quantity_density_evaluation.mainloop()

def create_window_Point_cloud_image(): #创建查看点云图像功能的子窗口
    window_Point_cloud_image = ttk.Toplevel()
    window_Point_cloud_image.title("查看点云图像") 
    ttk.Button(window_Point_cloud_image, text="选择要查看的点云文件", command=select_file_3,bootstyle=(INFO, OUTLINE)).grid(row=0, column=0)
    def convert_button_8(): #查看点云
        try:
            # 尝试用空格分隔符读取文件
            points = np.loadtxt(file_path_3)
        except ValueError:
            # 若空格分隔失败，尝试用逗号分隔符读取文件
            points = np.loadtxt(file_path_3, delimiter=',')
        visualize_point_cloud(points)
    ttk.Button(window_Point_cloud_image, text="查看", command=convert_button_8,bootstyle=(INFO, OUTLINE)).grid(row=0, column=1)

    window_Point_cloud_image.mainloop()



Main_frame = ttk.Frame(root,bootstyle="solar")
Main_frame.pack(padx=(0, 0),expand=YES,fill=BOTH)


state_step1 = IntVar(0)#是否加载测试文件夹
state_step2 = IntVar(0)#是否加载测试的SR75雷达文件

lf_pre_work = ttk.Labelframe(Main_frame,text="姿态识别准备工作",bootstyle=PRIMARY)
lf_pre_work.grid(row=0, column=0)




def select_folder_test():
    if state_step1.get() == 1:
            global file_path_2
            file_path_2 = os.path.join(os.path.abspath('.'), "attitude.txt")
            select_folder_12()

def select_file_test():
    if state_step2.get() == 1:
        select_file_4()

def recg_from_file():
   if state_step2.get() == 1:
        select_file_4()










ttk.Button(Main_frame, text="将SR75雷达原始输出文件转化为点云文件", command=create__window_SR75_point_cloud_data,bootstyle=(PRIMARY, "outline-toolbutton")).grid(row=0, column=1)
ttk.Button(Main_frame, text="点云数据分割", command=create__window_Data_segmentation,bootstyle=(PRIMARY, "outline-toolbutton")).grid(row=0, column=2)
ttk.Button(Main_frame, text="多帧融合", command=create_window_Multi_frame_fusion,bootstyle=(PRIMARY, "outline-toolbutton")).grid(row=0, column=3)
ttk.Button(Main_frame, text="DBSCAN融合", command=create_window_DBSCAN,bootstyle=(PRIMARY, "outline-toolbutton")).grid(row=1, column=1)
ttk.Button(Main_frame, text="点云文件采样", command=create_window_Sampling,bootstyle=(PRIMARY, "outline-toolbutton")).grid(row=1, column=2)
ttk.Button(Main_frame, text="点云文件点云数量/点云密度评估", command=create_window_quantity_density_evaluation,bootstyle=(PRIMARY, "outline-toolbutton")).grid(row=2, column=1)
ttk.Button(Main_frame, text="查看点云图像", command=create_window_Point_cloud_image,bootstyle=(PRIMARY, "outline-toolbutton")).grid(row=2, column=2)



# 运行主循环
root.mainloop()