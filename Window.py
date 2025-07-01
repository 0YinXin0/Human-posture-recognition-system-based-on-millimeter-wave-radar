import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import ttkthemes
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.scrolled import ScrolledText
import shutil
from PIL import Image, ImageTk
import os
import SR75
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import glob
import time
import Posture_Recognition
import re
from queue import Queue
from multiprocessing import freeze_support
from ttkbootstrap.dialogs import Messagebox
import pygame
import re

def play_audio(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # 等待播放完成
        pygame.time.Clock().tick(10)



def count(A):
    a = 0
    b = 0
    c = 0
    d = 0
    t = 0
    for i in A:
        t = t + 1
        if t < 5:
            if A[0].get('1.0', 'end') == i.get('1.0', 'end') and A[0].get('1.0', 'end') !="":
                a = a + 1
            if A[1].get('1.0', 'end') == i.get('1.0', 'end') and len(A[1].get('1.0', 'end')) > 1:
                b = b + 1
            if A[2].get('1.0', 'end') == i.get('1.0', 'end') and len(A[2].get('1.0', 'end')) > 1:
                c = c + 1
            if A[3].get('1.0', 'end') == i.get('1.0', 'end') and len(A[3].get('1.0', 'end')) > 1:
                d = d + 1
        result = [a,b,c,d]
    return result    

def Set_State_True(state):
    state[0] = True

def Set_State_False(state):
    state[0] = False


def Set_Current_File(current_file):
    current_file[0] = -1


def select_folder(): #选择文件夹
    return filedialog.askdirectory()


def select_file(): #选择文件
    return filedialog.askopenfilename()

def Image_init(image):
    setting = ImageTk.PhotoImage(Image.open(".\\图标\\设置-48.png"))
    image[0] = setting
    monitor = ImageTk.PhotoImage(Image.open(".\\图标\\监控-48.png"))
    image.append(monitor)
    View_historical_point_clouds = ImageTk.PhotoImage(Image.open(".\\图标\\查看历史点云-48.png"))
    image.append(View_historical_point_clouds)
    game = ImageTk.PhotoImage(Image.open(".\\图标\\游戏-48.png"))
    image.append(game)
    floder = ImageTk.PhotoImage(Image.open(".\\图标\\打开文件夹-32.png"))
    image.append(floder)
    monitoring = ImageTk.PhotoImage(Image.open(".\\图标\\正在监控-48.png"))
    image.append(monitoring)
    Viewing_historical_point_clouds = ImageTk.PhotoImage(Image.open(".\\图标\\正在查看历史点云-48.png"))
    image.append(Viewing_historical_point_clouds)
    playing_game = ImageTk.PhotoImage(Image.open(".\\图标\\玩游戏中-48.png"))
    image.append(playing_game)

def Window_init(window,window_width,window_height):
    OptionMenu_Top_Frame = ttk.Frame(window[0],width=window_width,height=window_height*0.1,bootstyle="info")
    OptionMenu_Top_Frame.place(relx=0,rely=0)   
    OptionMenu_Left_Frame_1 = ttk.Frame(window[0],width=window_width*0.2,height=window_height*0.59,bootstyle="",relief=GROOVE)
    OptionMenu_Left_Frame_1.place(relx=0,rely=0.099)
    OptionMenu_Left_Frame_2 = ttk.Frame(window[0],width=window_width*0.2,height=window_height*0.31,bootstyle="",relief=GROOVE)
    OptionMenu_Left_Frame_2.place(relx=0,rely=0.689)
    OptionMenu_Right_Frame_1 = ttk.Frame(window[0],width=window_width*0.8,height=window_height*0.1,bootstyle="info",relief=GROOVE)
    OptionMenu_Right_Frame_1.place(relx=0.2,rely=0.099)
    OptionMenu_Right_Frame_2 = ttk.Frame(window[0],width=window_width*0.6,height=window_height*0.8,bootstyle="",relief=GROOVE)
    OptionMenu_Right_Frame_2.place(relx=0.2,rely=0.199)
    OptionMenu_Right_Frame_3 = ttk.Frame(window[0],width=window_width*0.2,height=window_height*0.8,bootstyle="",relief=GROOVE)
    OptionMenu_Right_Frame_3.place(relx=0.8,rely=0.199)
    Window_frames = [OptionMenu_Top_Frame,OptionMenu_Left_Frame_1,OptionMenu_Left_Frame_2,OptionMenu_Right_Frame_1,OptionMenu_Right_Frame_2,OptionMenu_Right_Frame_3,window[0]]
    return Window_frames

#def OptionMenu_Top_Frame_init(frame):
        #Top_Frame = frame[0]

def OptionMenu_Left_Frame_1_init(result,Radar_State,Current_File,frame,window_width,window_height):
    Left_Frame_1 = frame[1]

    frame_top = ttk.Frame(Left_Frame_1,width=window_width*0.21,height=window_height*0.39*0.15,bootstyle="success",relief=SUNKEN)
    frame_top.place(relx=0,rely=0)
    ttk.Label(frame_top,text="雷达控制",bootstyle=("success", INVERSE),font=("Times New Roman", 16)).place(relx=0.31,rely=0.22)

    ttk.Label(Left_Frame_1,text="雷达通讯设备:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.01,rely=0.12)
    Equipment = ["创芯CANFD分析仪"]    
    Equipment_combobox = ttk.Combobox(Left_Frame_1, values=Equipment,state="readonly",width=20,font=("Times New Roman", 10))
    Equipment_combobox.place(relx=0.36,rely=0.12)
    Equipment_combobox.set(Equipment[0])

    ttk.Label(Left_Frame_1,text="CAN通道:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.01,rely=0.2)
    channels = [1,2,3,4,5]    
    channel_combobox = ttk.Combobox(Left_Frame_1, values=channels,state="readonly",width=8,font=("Times New Roman", 10))
    channel_combobox.place(relx=0.36,rely=0.2)
    channel_combobox.set(channels[1])


    ttk.Label(Left_Frame_1,text="通讯方式:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.01,rely=0.28)
    communcations = ["CAN","CANFD"]    
    communcations_combobox = ttk.Combobox(Left_Frame_1, values=communcations,state="readonly",width=8,font=("Times New Roman", 10))
    communcations_combobox.place(relx=0.36,rely=0.28)
    communcations_combobox.set(communcations[1])


    ttk.Label(Left_Frame_1,text="仲裁域波特率:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.01,rely=0.36)
    QDBs = ["1M","500K","250K","125K"]    
    QDBS_combobox = ttk.Combobox(Left_Frame_1, values=QDBs,state="readonly",width=8,font=("Times New Roman", 10))
    QDBS_combobox.place(relx=0.36,rely=0.36)
    QDBS_combobox.set(QDBs[0])


    ttk.Label(Left_Frame_1,text="数据域波特率:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.01,rely=0.44)
    DDBs = ["1M","2M","3M","4M","5M"]    
    DDBs_combobox = ttk.Combobox(Left_Frame_1, values=DDBs,state="readonly",width=8,font=("Times New Roman", 10))
    DDBs_combobox.place(relx=0.36,rely=0.44)
    DDBs_combobox.set(DDBs[3])

    ttk.Label(Left_Frame_1,text="雷达型号:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.01,rely=0.52)
    Radar_Type = ["SR75"]    
    Radar_Type_combobox = ttk.Combobox(Left_Frame_1, values=Radar_Type,state="readonly",width=8,font=("Times New Roman", 10))
    Radar_Type_combobox.place(relx=0.36,rely=0.52)
    Radar_Type_combobox.set(Radar_Type[0])


    button = ttk.Button(Left_Frame_1, text="连接雷达",bootstyle=("dark", OUTLINE))
    button.place(relx=0.23,rely=0.85,width=200, height=75)
    button.config(text="连接雷达",command = lambda: not_clicked())

 
    Area_Frame = ttk.Labelframe(Left_Frame_1,text="人体活动区域",bootstyle=PRIMARY,width=window_width*0.195,height=window_height*0.39*0.3).place(relx=0.01,rely=0.6)
    
    ttk.Label(Left_Frame_1,text="X轴 从",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.03,rely=0.65)
    X_minium = ttk.Entry(Left_Frame_1, width=3,font=("Times New Roman", 10))
    X_minium.place(relx=0.19,rely=0.64)
    ttk.Label(Left_Frame_1,text="米  到",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.305,rely=0.65)
    X_maxium = ttk.Entry(Left_Frame_1, width=3,font=("Times New Roman", 10))
    X_maxium.place(relx=0.445,rely=0.64)
    ttk.Label(Left_Frame_1,text="米",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.56,rely=0.65)

    ttk.Label(Left_Frame_1,text="Y轴 从",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.03,rely=0.73)
    Y_minium = ttk.Entry(Left_Frame_1, width=3,font=("Times New Roman", 10))
    Y_minium.place(relx=0.19,rely=0.72)
    ttk.Label(Left_Frame_1,text="米  到",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.305,rely=0.73)
    Y_maxium = ttk.Entry(Left_Frame_1, width=3,font=("Times New Roman", 10))
    Y_maxium.place(relx=0.445,rely=0.72)
    ttk.Label(Left_Frame_1,text="米",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.56,rely=0.73)

    def not_clicked():
        print("连接雷达 \n")

        result[0].delete("1.0", "end")  # 清空文本
        result[1].delete("1.0", "end")  # 清空文本
        result[2].delete("1.0", "end")  # 清空文本
        result[3].delete("1.0", "end")  # 清空文本
        thread_Set_Radar_State_True = threading.Thread(target=Set_State_True,args =(Radar_State,))
        thread_Set_Radar_State_True.start()
        button.config(text="断开雷达", command= lambda: clicked())
                    # 遍历文件夹内所有条目
        for filename in os.listdir(".\\Cloud_File"):
            file_path = os.path.join(".\\Cloud_File", filename)
            try:
                # 如果是文件或符号链接，直接删除
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                # 如果是子文件夹，递归删除其内容
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"删除失败: {file_path} - 错误原因: {e}")

        # 遍历文件夹内所有条目
        for filename_2 in os.listdir(".\\View_Cloud"):
            file_path_2 = os.path.join(".\\View_Cloud", filename_2)
            try:
                # 如果是文件或符号链接，直接删除
                if os.path.isfile(file_path_2) or os.path.islink(file_path_2):
                    os.unlink(file_path_2)
                # 如果是子文件夹，递归删除其内容
                elif os.path.isdir(file_path_2):
                    shutil.rmtree(file_path_2)
            except Exception as e:
                print(f"删除失败: {file_path_2} - 错误原因: {e}")

        thread_Set_Current_File = threading.Thread(target=Set_Current_File,args =(Current_File,))
        thread_Set_Current_File.start()

        if Radar_Type_combobox.current()==0:
            thread_SR75 = threading.Thread(target=Start_SR75,args =(result,Radar_State,Current_File,Equipment_combobox.get(),channel_combobox.get(),communcations_combobox.get(),QDBS_combobox.current(),DDBs_combobox.current(),float(X_minium.get()),float(X_maxium.get()),float(Y_minium.get()),float(Y_maxium.get())))
            thread_SR75.start()
            #thread_Draw_Cloud = threading.Thread(target=Draw_Cloud,args =(frame,Current_File,Radar_State,20,))
            #thread_Draw_Cloud.start()

    def clicked():
        print("断开雷达 \n")
        thread_Set_Radar_State_False = threading.Thread(target=Set_State_False,args =(Radar_State,))
        thread_Set_Radar_State_False.start()
        button.config(text="连接雷达", command=lambda: not_clicked())
    
    
    return [Equipment,Equipment_combobox,channels,channel_combobox,communcations,communcations_combobox,QDBs,QDBS_combobox,DDBs,DDBs_combobox]


def Multi_frame_fusion(start_file,number,source_folder, destination_folder,num_frame,name_file): #将点云数据进行多帧融合
    
    # 获取源文件夹中所有以数字结尾的 txt 文件
    all_txt_files = glob.glob(os.path.join(source_folder, '*.txt'))
    # 筛选出后缀数字在 start_file 到 start_file + num_frame 范围内的文件
    pattern = re.compile(rf'.*_(\d+)\.txt')
    txt_files = []
    for file in all_txt_files:
        match = pattern.match(file)
        if match:
            file_num = int(match.group(1))
            if start_file <= file_num <= start_file + num_frame:
                txt_files.append(file)
    # 对筛选后的文件进行排序
    txt_files.sort(key=lambda x: int(re.search(rf'.*_(\d+)\.txt', x).group(1)))
    
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
        new_file_name = os.path.join(destination_folder, f'{name_file}_{(number - 2)}.txt')
        with open(new_file_name, 'w', encoding='utf-8') as f:
            f.write(merged_content)




def Draw_Cloud(frame,File,State,Rate):
    
    # 状态变量（使用列表实现闭包可变性）
    path = ".\\Cloud_File\\cloud_0.txt"
    fig, canvas , colorbar = [None], [None],[None] # 用列表包装以支持修改
    file_number = 1
    while State[0]:
        if float(file_number) < float((File[0]+1)/Rate):
            file_number = file_number + 1
            Multi_frame_fusion(File[0],file_number,".\\Cloud_File",".\\View_Cloud",Rate,f"VIEW_{Rate}")
            #print("file_number:" + str(file_number) + "File[0] = " + str(File[0]))                  
            # 选择文件
            # 清理旧图形

            # 清空 frame 内的所有子控件
            for widget in frame[4].winfo_children():
                widget.destroy()

            path = f".\\View_Cloud\\VIEW_{Rate}_" + str(file_number - 2) + ".txt"
            try:
                # 读取数据
                data = np.loadtxt(path)
                if data.shape[1] != 3:
                    raise ValueError("文件需要包含x y z三列数据")

                # 创建新图形
                fig[0] = plt.figure(figsize=(8, 6))
                ax = fig[0].add_subplot(111, projection='3d')
                ax.scatter(data[:,0], data[:,1], data[:,2], s=1, c='blue')
                ax.set_xlabel("X"), ax.set_ylabel("Y"), ax.set_zlabel("Z")
                ax.set_title(f"Radar Message(file : {file_number - 2})")
                # 示例：添加颜色映射
                colors = data[:,2]  # 用Z值着色
                scatter = ax.scatter(data[:,0], data[:,1], data[:,2], c=colors, cmap='viridis')
                colorbar = [plt.colorbar(scatter, ax=ax,label="Z-axis height",shrink=0.6)]  # 添加颜色条

                # 嵌入画布
                canvas[0]= FigureCanvasTkAgg(fig[0], master=frame[4])
                canvas[0].draw()
                canvas[0].get_tk_widget().place(x=80, y=10, width=800, height=800)


                """
                # 清理旧图形
                if canvas[0]:
                    canvas[0].get_tk_widget().destroy()
                    plt.close(fig[0])
                if colorbar[0]:
                    colorbar[0].remove()  # 移除旧颜色条
                """
                #time.sleep(0.3)
            except Exception as e:
                print("err")
                #messagebox.showerror("错误", f"加载失败：{str(e)}")
                # 清理旧图形
                
    frame[4].delete("all")



def Draw_Cloud_File(frame,File,position):
    
    fig = [None]
    canvas = [None]
    colorbar = [None] # 用列表包装以支持修改
    try:
        # 读取数据
        data = np.loadtxt(File)
        if data.shape[1] != 3:
            raise ValueError("文件需要包含x y z三列数据")

        # 创建新图形
        fig[0] = plt.figure(figsize=(8, 6))
        ax = fig[0].add_subplot(111, projection='3d')
        ax.scatter(data[:,0], data[:,1], data[:,2], s=1, c='blue')
        ax.set_xlabel("X"), ax.set_ylabel("Y"), ax.set_zlabel("Z")
        ax.set_title(f"Radar Message")
        # 示例：添加颜色映射
        colors = data[:,2]  # 用Z值着色
        scatter = ax.scatter(data[:,0], data[:,1], data[:,2], c=colors, cmap='viridis')
        colorbar = [plt.colorbar(scatter, ax=ax,label="Z-axis height",shrink=0.6)]  # 添加颜色条

        # 嵌入画布
        canvas[0]= FigureCanvasTkAgg(fig[0], master=frame)
        canvas[0].draw()
        canvas[0].get_tk_widget().place(x=position[0], y=position[1], width=position[2], height=position[3])


        """
        # 清理旧图形
        if canvas[0]:
            canvas[0].get_tk_widget().destroy()
            plt.close(fig[0])
        if colorbar[0]:
            colorbar[0].remove()  # 移除旧颜色条
        """
            #time.sleep(0.3)
    except Exception as e:
        print("err")
        #messagebox.showerror("错误", f"加载失败：{str(e)}")
        # 清理旧图形
                
    return [fig,canvas,colorbar]





def Start_SR75(OUT,radar_State,File,equipment,channel,communcations,qdb,ddb,a,b,c,d):
    print("equipment:" + equipment)
    print("communcations:" + communcations)
    if equipment == "创芯CANFD分析仪":
        if communcations == "CANFD":
            print("尝试连接 SR75 雷达 : "  + "SR75" + channel + "qdb:" + str([1000000,500000,250000,125000][qdb]) + "ddb:" + str([1000000,2000000,3000000,4000000,5000000][ddb]) + "文件夹路径:" + "C:\\Users\\e1825\\Desktop\\BiYeLunWen\\HPR\\Cloud_File")
            SR75.SR75(OUT,radar_State,File,int(channel)-1,[1000000,500000,250000,125000][qdb],[1000000,2000000,3000000,4000000,5000000][ddb],"C:\\Users\\e1825\\Desktop\\BiYeLunWen\\HPR\\Cloud_File",a,b,c,d)

def OptionMenu_Left_Frame_2_init(human_posture,Radar_State,Current_File,result,frame,window_width,window_height,path,state,monitor_state,label,Sound_Path):
    Left_Frame_2 = frame[2]

    frame_top = ttk.Frame(Left_Frame_2,width=window_width*0.21,height=window_height*0.39*0.15,bootstyle="success",relief=SUNKEN)
    frame_top.place(relx=0,rely=0)
    ttk.Label(frame_top,text="姿态识别参数",bootstyle=("success", INVERSE),font=("Times New Roman", 16)).place(relx=0.21,rely=0.20)


    Recognize_Patterns_Frame = ttk.Labelframe(Left_Frame_2,text="识别模式",bootstyle=PRIMARY,width=window_width*0.195,height=window_height*0.39*0.42).place(relx=0.01,rely=0.2)
    
    Rate_20_var = tk.BooleanVar()
    Rate_20 = ttk.Checkbutton(Left_Frame_2,text="20帧率模型",variable=Rate_20_var) # 绑定状态变量
    Rate_20.place(relx=0.03,rely=0.3)
    Rate_20.invoke()

    Rate_40_var = tk.BooleanVar()
    Rate_40 = ttk.Checkbutton(Left_Frame_2,text="40帧率模型",variable=Rate_40_var) # 绑定状态变量
    Rate_40.place(relx=0.03,rely=0.41)
    Rate_40.invoke()
    
    Rate_60_var = tk.BooleanVar()
    Rate_60 = ttk.Checkbutton(Left_Frame_2,text="60帧率模型",variable=Rate_60_var) # 绑定状态变量
    Rate_60.place(relx=0.03,rely=0.51)
    Rate_60.invoke()

    Rate_80_var = tk.BooleanVar()
    Rate_80 = ttk.Checkbutton(Left_Frame_2,text="80帧率模型",variable=Rate_80_var) # 绑定状态变量
    Rate_80.place(relx=0.03,rely=0.61)
    Rate_80.invoke()


    button = ttk.Button(Left_Frame_2, text="开始人体姿态识别",bootstyle=("dark", OUTLINE))
    button.place(relx=0.23,rely=0.75,width=200, height=75)
    button.config(text="开始人体姿态识别",command = lambda: not_clicked(result,[button],state,label,monitor_state))


    def not_clicked(Result,B,State,Label,m):
        print("开始人体姿态识别\n")
        Set_State_True(State)        
        B[0].config(text="结束人体姿态识别", command= lambda: clicked(Result,B,State,Label,m))
        thread_recognition = threading.Thread(target=Recognition,args =(human_posture,Result,Radar_State,Current_File,0.08,4,1024,Rate_20_var.get(),Rate_40_var.get(),Rate_60_var.get(),Rate_80_var.get(),path,monitor_state,frame,Sound_Path))
        thread_recognition.start()

    
    def clicked(Result,B,State,Label,m):
        print("结束人体姿态识别\n")
        Set_State_False(State)
        Set_State_False(m) 
        B[0].config(text="开始人体姿态识别", command=lambda: not_clicked(Result,B,State,Label,m)) 


    return [Rate_20,Rate_40,Rate_60,Rate_80] 


def Recognition(human_posture,RESULT,State,File,eps,min_samples,target_num_points,Rate_20,Rate_40,Rate_60,Rate_80,path,monitor_state,frame,Sound_Path):
    print("开始人体姿态识别 : " +  " State = " + str(State[0]) +  " Current_File = " + str(File[0]) + "\n" + " eps = " + str(eps) + " min_samples = " + str(min_samples) + " target_num_points = " + str(target_num_points) + " Rate_20 = " + str(Rate_20) + " Rate_40 = " + str(Rate_40) + " Rate_60 = " + str(Rate_60) + " Rate_80 = " + str(Rate_80))
        # 遍历文件夹内所有条目
    for filename in os.listdir(".\\Rate_20_MFF"):
        file_path = os.path.join(".\\Rate_20_MFF", filename)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"删除失败: {file_path} - 错误原因: {e}")

    for filename_2 in os.listdir(".\\Rate_20_DIF"):
        file_path_2 = os.path.join(".\\Rate_20_DIF", filename_2)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_2) or os.path.islink(file_path_2):
                os.unlink(file_path_2)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_2):
                shutil.rmtree(file_path_2)
        except Exception as e:
            print(f"删除失败: {file_path_2} - 错误原因: {e}")
    

    for filename_3 in os.listdir(".\\Rate_20_DBSCAN"):
        file_path_3 = os.path.join(".\\Rate_20_DBSCAN", filename_3)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_3) or os.path.islink(file_path_3):
                os.unlink(file_path_3)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_3):
                shutil.rmtree(file_path_3)
        except Exception as e:
            print(f"删除失败: {file_path_3} - 错误原因: {e}")


    for filename_4 in os.listdir(".\\Rate_20_Sampling"):
        file_path_4 = os.path.join(".\\Rate_20_Sampling", filename_4)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_4) or os.path.islink(file_path_4):
                os.unlink(file_path_4)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_4):
                shutil.rmtree(file_path_4)
        except Exception as e:
            print(f"删除失败: {file_path_4} - 错误原因: {e}")


    for filename_5 in os.listdir(".\\Rate_40_MFF"):
        file_path_5 = os.path.join(".\\Rate_40_MFF", filename_5)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_5) or os.path.islink(file_path_5):
                os.unlink(file_path_5)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_5):
                shutil.rmtree(file_path_5)
        except Exception as e:
            print(f"删除失败: {file_path_5} - 错误原因: {e}")

    for filename_6 in os.listdir(".\\Rate_40_DIF"):
        file_path_6 = os.path.join(".\\Rate_40_DIF", filename_6)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_6) or os.path.islink(file_path_6):
                os.unlink(file_path_6)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_6):
                shutil.rmtree(file_path_6)
        except Exception as e:
            print(f"删除失败: {file_path_6} - 错误原因: {e}")
    

    for filename_7 in os.listdir(".\\Rate_40_DBSCAN"):
        file_path_7 = os.path.join(".\\Rate_40_DBSCAN", filename_7)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_7) or os.path.islink(file_path_7):
                os.unlink(file_path_7)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_7):
                shutil.rmtree(file_path_7)
        except Exception as e:
            print(f"删除失败: {file_path_7} - 错误原因: {e}")


    for filename_8 in os.listdir(".\\Rate_40_Sampling"):
        file_path_8 = os.path.join(".\\Rate_40_Sampling", filename_8)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_8) or os.path.islink(file_path_8):
                os.unlink(file_path_8)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_8):
                shutil.rmtree(file_path_8)
        except Exception as e:
            print(f"删除失败: {file_path_8} - 错误原因: {e}")


    for filename_9 in os.listdir(".\\Rate_60_MFF"):
        file_path_9 = os.path.join(".\\Rate_60_MFF", filename_9)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_9) or os.path.islink(file_path_9):
                os.unlink(file_path_9)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_9):
                shutil.rmtree(file_path_9)
        except Exception as e:
            print(f"删除失败: {file_path_9} - 错误原因: {e}")

    for filename_10 in os.listdir(".\\Rate_60_DIF"):
        file_path_10 = os.path.join(".\\Rate_60_DIF", filename_10)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_10) or os.path.islink(file_path_10):
                os.unlink(file_path_10)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_10):
                shutil.rmtree(file_path_10)
        except Exception as e:
            print(f"删除失败: {file_path_10} - 错误原因: {e}")
    

    for filename_11 in os.listdir(".\\Rate_60_DBSCAN"):
        file_path_11 = os.path.join(".\\Rate_60_DBSCAN", filename_11)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_11) or os.path.islink(file_path_11):
                os.unlink(file_path_11)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_11):
                shutil.rmtree(file_path_11)
        except Exception as e:
            print(f"删除失败: {file_path_11} - 错误原因: {e}")


    for filename_12 in os.listdir(".\\Rate_60_Sampling"):
        file_path_12 = os.path.join(".\\Rate_60_Sampling", filename_12)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_12) or os.path.islink(file_path_12):
                os.unlink(file_path_12)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_12):
                shutil.rmtree(file_path_12)
        except Exception as e:
            print(f"删除失败: {file_path_12} - 错误原因: {e}")


    for filename_13 in os.listdir(".\\Rate_80_MFF"):
        file_path_13 = os.path.join(".\\Rate_80_MFF", filename_13)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_13) or os.path.islink(file_path_13):
                os.unlink(file_path_13)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_13):
                shutil.rmtree(file_path_13)
        except Exception as e:
            print(f"删除失败: {file_path_13} - 错误原因: {e}")

    for filename_14 in os.listdir(".\\Rate_80_DIF"):
        file_path_14 = os.path.join(".\\Rate_80_DIF", filename_14)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_14) or os.path.islink(file_path_14):
                os.unlink(file_path_14)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_14):
                shutil.rmtree(file_path_14)
        except Exception as e:
            print(f"删除失败: {file_path_14} - 错误原因: {e}")
    

    for filename_15 in os.listdir(".\\Rate_80_DBSCAN"):
        file_path_15 = os.path.join(".\\Rate_80_DBSCAN", filename_15)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_15) or os.path.islink(file_path_15):
                os.unlink(file_path_15)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_15):
                shutil.rmtree(file_path_15)
        except Exception as e:
            print(f"删除失败: {file_path_15} - 错误原因: {e}")


    for filename_16 in os.listdir(".\\Rate_80_Sampling"):
        file_path_16 = os.path.join(".\\Rate_80_Sampling", filename_16)
        try:
            # 如果是文件或符号链接，直接删除
            if os.path.isfile(file_path_16) or os.path.islink(file_path_16):
                os.unlink(file_path_16)
            # 如果是子文件夹，递归删除其内容
            elif os.path.isdir(file_path_16):
                shutil.rmtree(file_path_16)
        except Exception as e:
            print(f"删除失败: {file_path_16} - 错误原因: {e}")






    file_number_20 = 1
    file_number_40 = 1
    file_number_60 = 1
    file_number_80 = 1

    while State[0]:
        if Rate_20:
            if float(file_number_20) < float((File[0]+1)/20):
                file_number_20 = file_number_20 + 1
                print("file_number_20 = " + str(file_number_20))
                RESULT[0].delete("1.0", "end")  # 清空文本
                result_20 = Posture_Recognition.Posture_Recognition(File[0],file_number_20,file_number_40,file_number_60,file_number_80,eps,min_samples,target_num_points,True,False,False,False,path)
                if result_20 is None:
                    RESULT[0].insert("1.0", "未识别到人体")  
                else:   
                    RESULT[0].insert("1.0", result_20)        
        if Rate_40:
            if float(file_number_40) < float((File[0]+1)/40):
                file_number_40 = file_number_40 + 1
                print("file_number_40 = " + str(file_number_40))
                RESULT[1].delete("1.0", "end")  # 清空文本
                result_40 = Posture_Recognition.Posture_Recognition(File[0],file_number_20,file_number_40,file_number_60,file_number_80,eps,min_samples,target_num_points,False,True,False,False,path)
                if result_40 is None:
                    RESULT[1].insert("1.0", "未识别到人体")  
                else:   
                    RESULT[1].insert("1.0", result_40)         
        if Rate_60:
            if float(file_number_60) < float((File[0]+1)/60):
                file_number_60 = file_number_60 + 1
                print("file_number_60 = " + str(file_number_60))
                RESULT[2].delete("1.0", "end")  # 清空文本
                result_60 = Posture_Recognition.Posture_Recognition(File[0],file_number_20,file_number_40,file_number_60,file_number_80,eps,min_samples,target_num_points,False,False,True,False,path)
                if result_60 is None:
                    RESULT[2].insert("1.0", "未识别到人体")  
                else:   
                    RESULT[2].insert("1.0", result_60)           
        if Rate_80:
            if float(file_number_80) < float((File[0]+1)/80):
                file_number_80 = file_number_80 + 1
                print("file_number_80 = " + str(file_number_80))
                RESULT[3].delete("1.0", "end")  # 清空文本
                result_80 = Posture_Recognition.Posture_Recognition(File[0],file_number_20,file_number_40,file_number_60,file_number_80,eps,min_samples,target_num_points,False,False,False,True,path)
                if result_80 is None:
                    RESULT[3].insert("1.0", "未识别到人体")  
                else:   
                    RESULT[3].insert("1.0", result_80)             
        RESULT[4].delete("1.0", "end")  # 清空文本
        R = count(RESULT)
        RESULT[4].insert("1.0",RESULT[R.index(max(R))].get("1.0", "end")) 
        human_posture[0] = RESULT[R.index(max(R))].get("1.0", "end")
        if monitor_state[0] and len(RESULT[4].get("1.0", "end")) != 8 and len(RESULT[4].get("1.0", "end")) != 2:
            print("监控发现人体活动")
            play_audio(Sound_Path[0])
            print("len(RESULT[4].get(1.0, end)) = " + str(len(RESULT[4].get("1.0", "end"))))
        time.sleep(0.1)


def OptionMenu_Right_Frame_3_init(frame,window_width,window_height):
    Right_Frame_3 = frame[5]

    frame_top = ttk.Frame(Right_Frame_3,width=window_width*0.21,height=window_height*0.39*0.15,bootstyle="success",relief=SUNKEN)
    frame_top.place(relx=0,rely=0)
    ttk.Label(frame_top,text="识别结果",bootstyle=("success", INVERSE),font=("Times New Roman", 16)).place(relx=0.31,rely=0.22)

    R1 = ttk.Label(Right_Frame_3,text="20帧率模型结果:",bootstyle=("light", INVERSE),font=("Times New Roman", 10))
    R1.place(relx=0.01,rely=0.1)
    result_20 = ttk.Text(Right_Frame_3, width=15, height=1)
    result_20.place(relx=0.41,rely=0.096)

    R2 = ttk.Label(Right_Frame_3,text="40帧率模型结果:",bootstyle=("light", INVERSE),font=("Times New Roman", 10))
    R2.place(relx=0.01,rely=0.17)
    result_40 = ttk.Text(Right_Frame_3, width=15, height=1)
    result_40.place(relx=0.41,rely=0.166)

    R3 = ttk.Label(Right_Frame_3,text="60帧率模型结果:",bootstyle=("light", INVERSE),font=("Times New Roman", 10))
    R3.place(relx=0.01,rely=0.24)
    result_60 = ttk.Text(Right_Frame_3, width=15, height=1)
    result_60.place(relx=0.41,rely=0.236)

    R4 = ttk.Label(Right_Frame_3,text="80帧率模型结果:",bootstyle=("light", INVERSE),font=("Times New Roman", 10))
    R4.place(relx=0.01,rely=0.31)
    result_80 = ttk.Text(Right_Frame_3, width=15, height=1)
    result_80.place(relx=0.41,rely=0.306)

    LabelFrame = ttk.Labelframe(Right_Frame_3,text="结果",bootstyle=PRIMARY,width=369,height=100)
    LabelFrame.place(relx=0.01,rely=0.356)



    ttk.Label(Right_Frame_3,text="姿态识别结果:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.412)
    result = ttk.Text(Right_Frame_3, width=15, height=1)
    result.place(relx=0.405,rely=0.407)

    frame_middle = ttk.Frame(Right_Frame_3,width=window_width*0.21,height=window_height*0.39*0.15,bootstyle="success",relief=SUNKEN)
    frame_middle.place(relx=0,rely=0.49)
    ttk.Label(frame_middle,text="雷达通讯",bootstyle=("success", INVERSE),font=("Times New Roman", 16)).place(relx=0.31,rely=0.22)

    T = tk.Text(Right_Frame_3,width = 45,height = 17 ,font=("Times New Roman", 8))
    T.place(relx=0.005,rely=0.565)



    RESULT = [result_20,result_40,result_60,result_80,result,R1,R2,R3,R4,T]
    return RESULT


def OptionMenu_Right_Frame_1_init(human_posture,frame,window_width,window_height,image,window,models,path,result,state,monitor_state,playback_state,draw_position,game_state):
    Right_Frame_1 = frame[3]
    Function_buttons = [NONE,NONE,NONE,NONE]
    Function_Labels = [NONE,NONE,NONE,NONE]
    f1 = ttk.Button(Right_Frame_1,image = image[0],bootstyle=INFO,command = lambda: Setting_Function(window,image,models,path,result))
    f1.place(relx=0.02,rely=0.05)
    Function_buttons[0] = f1
    l1 = ttk.Label(Right_Frame_1,text="设置",bootstyle=("info", INVERSE),font=("Times New Roman", 10))
    l1.place(relx=0.029,rely=0.7)
    Function_Labels[0] = l1

    f2 = ttk.Button(Right_Frame_1,image = image[1],bootstyle=INFO,command= lambda : Monitor_Function(frame[3],state,monitor_state,Function_buttons,image,Function_Labels,human_posture))
    f2.place(relx=0.09,rely=0.05)
    Function_buttons[1] = f2
    l2 = ttk.Label(Right_Frame_1,text="监控",bootstyle=("info", INVERSE),font=("Times New Roman", 10))
    l2.place(relx=0.099,rely=0.7)
    Function_Labels[1] = l2

    f3 = ttk.Button(Right_Frame_1,image = image[2],bootstyle=INFO,command= lambda : Playback_Function(frame,window_width,window_height,playback_state,image,Function_buttons,Function_Labels,draw_position))
    f3.place(relx=0.16,rely=0.05)
    Function_buttons[2] = f3
    l3 = ttk.Label(Right_Frame_1,text="回放",bootstyle=("info", INVERSE),font=("Times New Roman", 10))
    l3.place(relx=0.169,rely=0.7)
    Function_Labels[2] = l3

    f4 = ttk.Button(Right_Frame_1,image = image[3],bootstyle=INFO,command = lambda : Game_Function(state,human_posture,frame,window_width,window_height,game_state,image,Function_buttons,Function_Labels))
    f4.place(relx=0.23,rely=0.05)
    Function_buttons[3] = f4
    l4 = ttk.Label(Right_Frame_1,text="游戏",bootstyle=("info", INVERSE),font=("Times New Roman", 10))
    l4.place(relx=0.239,rely=0.7)
    Function_Labels[3] = l4

    return [Function_buttons,Function_Labels]

def Setting_Function(window,icon,model,path,result):
    MODEL = [NONE,NONE,NONE,NONE]#模型项的名字
    PATH = [NONE,NONE,NONE,NONE]#模型项的路径
    window_width = 1900 #窗口的宽度
    window_height = 1000 #窗口的高度
    seeting = ttk.Toplevel(window[0],alpha=0.9,size=(window_width, window_height),iconphoto= icon[0] ,position=(400, 100),resizable=(True, True))##里面的参数和Window()父窗口一致
    seeting.attributes("-topmost", True)
    ttk.Frame(seeting,width=window_width,height=window_height*0.1,bootstyle="info",relief=SUNKEN).place(relx=0,rely=0)
    ttk.Label(seeting,text="系 统 设 置 ",bootstyle=("info", INVERSE),font=("Times New Roman", 20)).place(relx=0.45,rely=0.025)


    Model_Area_Frame = ttk.Labelframe(seeting,text="姿态识别所用模型设置",bootstyle=DARK,width=window_width*0.31,height=window_height*0.35).place(relx=0.01,rely=0.12)
    
    ttk.Label(seeting,text="模型1 :  所显示的选项名称:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.15)
    MODEL[0] = ttk.Entry(seeting, width=20,font=("Times New Roman", 10))
    MODEL[0].place(relx=0.15,rely=0.145)
    MODEL[0].insert(0, model[0].cget("text"))  # 在位置 0 插入文本
    def change_option_1_name(m,M,R):
        m[0].configure(text=M[0].get())
        R[5].configure(text=f"{M[0].get()}结果:")
    def select_option_1_path(w,P):
        w.attributes("-topmost", False)
        path = filedialog.askdirectory()
        w.attributes("-topmost", True)
        P[0].delete(0, tk.END)  # 清空文本框内容
        P[0].insert(0, path)  # 在位置 0 插入文本

    def change_option_1_path(P,p):
        p[0] = P[0].get()


    ttk.Button(seeting,text = "确认修改",bootstyle="warning",command = lambda : change_option_1_name(model,MODEL,result)).place(relx=0.265,rely=0.145)
    ttk.Label(seeting,text="模型1路径:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.193)
    PATH[0] = ttk.Entry(seeting, width=37,font=("Times New Roman", 8))
    PATH[0].place(relx=0.072,rely=0.188)
    PATH[0].insert(0, path[0])  # 在位置 0 插入文本
    ttk.Button(seeting,image= icon[4],bootstyle = "light",command =  lambda : select_option_1_path(seeting,PATH)).place(relx=0.237,rely=0.183)
    ttk.Button(seeting,text = "确认修改",bootstyle="warning",command = lambda :change_option_1_path(PATH,path)).place(relx=0.265,rely=0.183)

    def change_option_2_name(m,M,R):
        m[1].configure(text=M[1].get())
        R[6].configure(text=f"{M[1].get()}结果:")

    def select_option_2_path(w,P):
        w.attributes("-topmost", False)
        path = filedialog.askdirectory()
        w.attributes("-topmost", True)
        P[1].delete(0, tk.END)  # 清空文本框内容
        P[1].insert(0, path)  # 在位置 0 插入文本

    def change_option_2_path(P,p):
        p[1] = P[1].get()

    ttk.Label(seeting,text="模型2 :  所显示的选项名称:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.229)
    MODEL[1] = ttk.Entry(seeting, width=20,font=("Times New Roman", 10))
    MODEL[1].place(relx=0.15,rely=0.224)
    MODEL[1].insert(0, model[1].cget("text"))  # 在位置 0 插入文本
    ttk.Button(seeting,text = "确认修改",bootstyle="warning",command = lambda :change_option_2_name(model,MODEL,result)).place(relx=0.265,rely=0.221)
    ttk.Label(seeting,text="模型2路径:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.269)
    PATH[1] = ttk.Entry(seeting, width=37,font=("Times New Roman", 8))
    PATH[1].place(relx=0.072,rely=0.264)
    PATH[1].insert(0, path[1])  # 在位置 0 插入文本
    ttk.Button(seeting,image= icon[4],bootstyle = "light",command =  lambda : select_option_2_path(seeting,PATH)).place(relx=0.237,rely=0.259)
    ttk.Button(seeting,text = "确认修改",bootstyle="warning",command = lambda :change_option_2_path(PATH,path)).place(relx=0.265,rely=0.259)

    def change_option_3_name(m,M,R):
        m[2].configure(text=M[2].get())
        R[7].configure(text=f"{M[2].get()}结果:")

    def select_option_3_path(w,P):
        w.attributes("-topmost", False)
        path = filedialog.askdirectory()
        w.attributes("-topmost", True)
        P[2].delete(0, tk.END)  # 清空文本框内容
        P[2].insert(0, path)  # 在位置 0 插入文本

    def change_option_3_path(P,p):
        p[2] = P[2].get()

    ttk.Label(seeting,text="模型3 :  所显示的选项名称:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.308)
    MODEL[2] = ttk.Entry(seeting, width=20,font=("Times New Roman", 10))
    MODEL[2].place(relx=0.15,rely=0.303)
    MODEL[2].insert(0, model[2].cget("text"))  # 在位置 0 插入文本
    ttk.Button(seeting,text = "确认修改",bootstyle="warning",command = lambda :change_option_3_name(model,MODEL,result)).place(relx=0.265,rely=0.297)
    ttk.Label(seeting,text="模型3路径:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.338)
    PATH[2] = ttk.Entry(seeting, width=37,font=("Times New Roman", 8))
    PATH[2].place(relx=0.072,rely=0.333)
    PATH[2].insert(0, path[2])  # 在位置 0 插入文本
    ttk.Button(seeting,image= icon[4],bootstyle = "light",command =  lambda : select_option_3_path(seeting,PATH)).place(relx=0.237,rely=0.328)
    ttk.Button(seeting,text = "确认修改",bootstyle="warning",command = lambda :change_option_3_path(PATH,path)).place(relx=0.265,rely=0.336)

    def change_option_4_name(m,M,R):
        m[3].configure(text=M[3].get())
        R[8].configure(text=f"{M[3].get()}结果:")

    def select_option_4_path(w,P):
        w.attributes("-topmost", False)
        path = filedialog.askdirectory()
        w.attributes("-topmost", True)
        P[3].delete(0, tk.END)  # 清空文本框内容
        P[3].insert(0, path)  # 在位置 0 插入文本

    def change_option_4_path(P,p):
        p[3] = P[3].get()

    ttk.Label(seeting,text="模型4 :  所显示的选项名称:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.387)
    MODEL[3] = ttk.Entry(seeting, width=20,font=("Times New Roman", 10))
    MODEL[3].place(relx=0.15,rely=0.382)
    MODEL[3].insert(0, model[2].cget("text"))  # 在位置 0 插入文本
    ttk.Button(seeting,text = "确认修改",bootstyle="warning",command = lambda :change_option_4_name(model,MODEL,result)).place(relx=0.265,rely=0.376)
    ttk.Label(seeting,text="模型4路径:",bootstyle=("light", INVERSE),font=("Times New Roman", 10)).place(relx=0.02,rely=0.417)
    PATH[3] = ttk.Entry(seeting, width=37,font=("Times New Roman", 8))
    PATH[3].place(relx=0.072,rely=0.412)
    PATH[3].insert(0, path[2])  # 在位置 0 插入文本
    ttk.Button(seeting,image= icon[4],bootstyle = "light",command =  lambda : select_option_4_path(seeting,PATH)).place(relx=0.237,rely=0.407)
    ttk.Button(seeting,text = "确认修改",bootstyle="warning",command = lambda :change_option_4_path(PATH,path)).place(relx=0.265,rely=0.415)


def Monitor_Function(window,state,monitor_state,button,image,labels,T):
    if state[0] == False and monitor_state[0] == False:
        # 显示信息框
        print("state[0] = " + str(state[0]))
        Messagebox.show_error("人体姿态识别按钮未打开时无法使用监控功能！", "错误！", parent = window)
    else:
        if monitor_state[0] == False:
            T[0].delete("1.0", "end")
            T[1].delete("1.0", "end")
            T[2].delete("1.0", "end")
            T[3].delete("1.0", "end")
            T[4].delete("1.0", "end")
            Set_State_True(monitor_state)
            button[1].configure(image = image[5])
            labels[1].configure(text="监控中")
        else:
            Set_State_False(monitor_state)
            button[1].configure(image = image[1])
            labels[1].configure(text="监控")

def Playback_Function(window,window_width,window_height,playback_state,icon,buttons,labels,draw_position):
    for widget in window[4].winfo_children():
        widget.destroy()

    
    if playback_state[0] == False:
        Set_State_True(playback_state)
        buttons[2].configure(image = icon[6])
        labels[2].configure(text="回放中")
        ttk.Frame(window[4],width=window_width,height=window_height*0.1,bootstyle="info",relief=SUNKEN).place(relx=0,rely=0)
        ttk.Label(window[4],text="回 放 功 能",bootstyle=("info", INVERSE),font=("Times New Roman", 20)).place(relx=0.41,rely=0.025)
        ttk.Frame(window[4],width=window_width,height=window_height*0.1,bootstyle="info",relief=SUNKEN).place(relx=0,rely=0.9)

        canv = [None,None,None]
        def draw(can,position):
            # 清理旧图形
            if can[0] is not None:
                can[1][0].get_tk_widget().destroy()
                plt.close(can[0][0])
            if can[2] is not None:
                can[2][0].remove()  # 移除旧颜色条
            
            file_path = select_file()
            can = Draw_Cloud_File(window[4],file_path,position)
        ttk.Button(window[4],text = "选 择 回 放 文 件",bootstyle=SUCCESS,padding=(32, 15),command =lambda : draw(canv,draw_position)).place(relx=0.43,rely=0.92)

    else:
        Set_State_False(playback_state)
        buttons[2].configure(image = icon[2])
        labels[2].configure(text="回放")
        for widget in window[4].winfo_children():
            widget.destroy()

def Game_Function(state,human_posture,window,window_width,window_height,game_state,icon,buttons,labels):
    if state[0] == False and game_state[0] == False :
        # 显示信息框
        print("state[0] = " + str(state[0]))
        Messagebox.show_error("人体姿态识别按钮未打开时无法使用游戏功能！", "错误！", parent = window[4])
    else:
        for widget in window[4].winfo_children():
            widget.destroy()

        if game_state[0] == False:
            Set_State_True(game_state)
            buttons[3].configure(image = icon[7])
            labels[3].configure(text="游戏中")
            ttk.Frame(window[4],width=window_width,height=window_height*0.1,bootstyle="info",relief=SUNKEN).place(relx=0,rely=0)
            ttk.Label(window[4],text="游 戏 功 能",bootstyle=("info", INVERSE),font=("Times New Roman", 20)).place(relx=0.41,rely=0.025)
            ttk.Frame(window[4],width=window_width,height=window_height*0.1,bootstyle="info",relief=SUNKEN).place(relx=0,rely=0.9)
        
            def Game(human_posture,frame,STAT):
                file_path = select_file()
                thread_start_game = threading.Thread(target=start_game,args =(file_path,human_posture,frame,STAT,))
                thread_start_game.start()


            def start_game(file_path,human_posture,Frame,ST):
                # 启动游戏
                with open(file_path, "r", encoding="utf-8") as file:
                    lines = [line.rstrip("\n") for line in file]


                M = ttk.Label(Frame[4],text="当前动作为 : ",bootstyle=("info", INVERSE),font=("Times New Roman", 20))
                M.place(relx=0.32,rely=0.44)
                t =len(lines)
                k = 0
                i = lines[k]
                M.configure(text= f"当前要做动作为 :  {i}")
                while k < t-1 and ST[0] == True :
                    m = human_posture[4].get("1.0", "end")
                    w = re.sub(r"[^a-zA-Z]", "", m)
                    j = re.sub(r"[^a-zA-Z]", "", i)
                    if w == j :
                        k = k + 1
                        i = lines[k]
                        M.configure(text= f"当前要做动作为 :  {i}")
                        print("已做到!")
                        play_audio(".\\音效\\游戏通过.mp3")

                    


            ttk.Button(window[4],text = "开 始 游 戏",bootstyle=SUCCESS,padding=(32, 15),command = lambda : Game(human_posture,window,game_state)).place(relx=0.43,rely=0.92)

        else:
            Set_State_False(game_state)
            buttons[3].configure(image = icon[3])
            labels[3].configure(text="游戏")
            for widget in window[4].winfo_children():
                widget.destroy()

def main(): 
    os.environ["LOKY_MAX_CPU_COUNT"] = "8"  # 手动设置核心数
    Radar_State_T = [True]  # 雷达状态
    Recognition_State = [False] #姿态识别状态
    Current_File_T = [-1]  # 文件索引
    Monitor_State = [False] #监控状态
    Models = [None] #模型文件路径
    OptionMenu_Right_Frame_1 = [NONE,NONE] #功能区功能按钮列表和功能标签列表
    IMAGE = [None]  # 图标数据
    PATH = [".\\Models\\20Frames",".\\Models\\40Frames",".\\Models\\60Frames",".\\Models\\80Frames"]#姿态识别所用模型的路径
    Monitor_Sound_Path = [".\\音效\\简短门铃声电子清脆.mp3"]
    Playback_State = [False] #回放状态
    Draw_Position = [295,101,620,620]#回放功能点云图绘制位置x,y,width,height
    Game_State = [False] #游戏状态
    Human_posture = [None] #人体姿态输出结果
    # 使用 Manager 创建共享列表
    window_width = 1900 #窗口的宽度
    window_height = 1000 #窗口的高度
    Window_main = ttk.Window(
        title="基于三维毫米波雷达点云的人体姿态识别系统",        #设置窗口的标题
        themename="minty",     #设置主题
        size=(window_width,window_height),        #窗口的大小
        position=(400,100),     #窗口所在的位置
        minsize=(0,0),          #窗口的最小宽高
        maxsize=(1920,1080),    #窗口的最大宽高
        resizable=None,         #设置窗口是否可以更改大小
        alpha=1,              #设置窗口的透明度(0.0完全透明）
        )
    

    Window = [Window_main]
    Window_frames = Window_init(Window,window_width,window_height)#窗口里的各个frame,OptionMenu_Top_Frame,OptionMenu_Left_Frame_1,OptionMenu_Left_Frame_2,OptionMenu_Right_Frame_1,OptionMenu_Right_Frame_2,OptionMenu_Right_Frame_3
    #OptionMenu_Top_Frame_init(Window_frames)

    Recognition_result = OptionMenu_Right_Frame_3_init(Window_frames,window_width,window_height)    
    
    OptionMenu_Left_Frame_1 = OptionMenu_Left_Frame_1_init(Recognition_result,Radar_State_T,Current_File_T,Window_frames,window_width,window_height) #左边窗口里的各个Frame,[Equipment,Equipment_combobox,channels,channel_combobox,communcations,communcations_combobox,QDBs,QDBS_combobox,DDBs,DDBs_combobox,folder_path]
    
    Models = OptionMenu_Left_Frame_2_init(Human_posture,Radar_State_T,Current_File_T,Recognition_result,Window_frames,window_width,window_height,PATH,Recognition_State,Monitor_State,OptionMenu_Right_Frame_1,Monitor_Sound_Path)
    #返回四种模型是否启用以及雷达检测范围
    Image_init(IMAGE)

    OptionMenu_Right_Frame_1 = OptionMenu_Right_Frame_1_init(Recognition_result,Window_frames,window_width,window_height,IMAGE,Window,Models,PATH,Recognition_result,Recognition_State,Monitor_State,Playback_State,Draw_Position,Game_State)
    

    Window_main.mainloop()

if __name__ == "__main__":
    freeze_support()  # 支持打包
    main()