from ctypes import *
import time
import os
import shutil

# 常量定义
VCI_USBCAN2 = 41
STATUS_OK = 1
RADAR_ID = 0  # 默认雷达ID
TYPE_CANFD = 1

class VCI_INIT_CONFIG(Structure):  
    _fields_ = [("AccCode", c_uint),
                ("AccMask", c_uint),
                ("Reserved", c_uint),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)
                ]  
class VCI_CAN_OBJ(Structure):  
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte*8),
                ("Reserved", c_ubyte*3)
                ] 
 
### structure
class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("reserved", c_uint),
                ("filter",   c_ubyte),
                ("timing0",  c_ubyte),
                ("timing1",  c_ubyte),
                ("mode",     c_ubyte)]

class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):
    _fields_ = [("acc_code",     c_uint),
                ("acc_mask",     c_uint),
                ("abit_timing",  c_uint),
                ("dbit_timing",  c_uint),
                ("brp",          c_uint),
                ("filter",       c_ubyte),
                ("mode",         c_ubyte),
                ("pad",          c_ushort),
                ("reserved",     c_uint)]

class _ZCAN_CHANNEL_INIT_CONFIG(Union):
    _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]

class ZCAN_CHANNEL_INIT_CONFIG(Structure):
    _fields_ = [("can_type", c_uint),
                ("config", _ZCAN_CHANNEL_INIT_CONFIG)]
				
class ZCAN_CAN_FRAME(Structure):
    _fields_ = [("can_id",  c_uint, 29),
                ("err",     c_uint, 1),
                ("rtr",     c_uint, 1),
                ("eff",     c_uint, 1), 
                ("can_dlc", c_ubyte),
                ("__pad",   c_ubyte),
                ("__res0",  c_ubyte),
                ("__res1",  c_ubyte),
                ("data",    c_ubyte * 8)]

class ZCAN_CANFD_FRAME(Structure):
    _fields_ = [("can_id", c_uint, 29), 
                ("err",    c_uint, 1),
                ("rtr",    c_uint, 1),
                ("eff",    c_uint, 1), 
                ("len",    c_ubyte),
                ("brs",    c_ubyte, 1),
                ("esi",    c_ubyte, 1),
                ("__res",  c_ubyte, 6),
                ("__res0", c_ubyte),
                ("__res1", c_ubyte),
                ("data",   c_ubyte * 64)]

				
class ZCAN_Transmit_Data(Structure):
    _fields_ = [("frame", ZCAN_CAN_FRAME), ("transmit_type", c_uint)]

class ZCAN_Receive_Data(Structure):
    _fields_  = [("frame", ZCAN_CAN_FRAME), ("timestamp", c_ulonglong)]

class ZCAN_TransmitFD_Data(Structure):
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("transmit_type", c_uint)]

class ZCAN_ReceiveFD_Data(Structure):
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("timestamp", c_ulonglong)]


canDLL = windll.LoadLibrary('./ControlCANFD.dll')

canDLL.ZCAN_OpenDevice.restype = c_void_p
canDLL.ZCAN_SetAbitBaud.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_SetDbitBaud.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_SetCANFDStandard.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_InitCAN.argtypes = (c_void_p, c_ulong, c_void_p)
canDLL.ZCAN_InitCAN.restype = c_void_p
canDLL.ZCAN_StartCAN.argtypes = (c_void_p,)
canDLL.ZCAN_Transmit.argtypes = (c_void_p, c_void_p, c_ulong)
canDLL.ZCAN_TransmitFD.argtypes = (c_void_p, c_void_p, c_ulong)
canDLL.ZCAN_GetReceiveNum.argtypes = (c_void_p, c_ulong)
canDLL.ZCAN_Receive.argtypes = (c_void_p, c_void_p, c_ulong, c_long)
canDLL.ZCAN_ReceiveFD.argtypes = (c_void_p, c_void_p, c_ulong, c_long)
canDLL.ZCAN_ResetCAN.argtypes = (c_void_p,)
canDLL.ZCAN_CloseDevice.argtypes = (c_void_p,)

canDLL.ZCAN_ClearFilter.argtypes=(c_void_p,)
canDLL.ZCAN_AckFilter.argtypes=(c_void_p,)
canDLL.ZCAN_SetFilterMode.argtypes=(c_void_p,c_ulong)
canDLL.ZCAN_SetFilterStartID.argtypes=(c_void_p,c_ulong)
canDLL.ZCAN_SetFilterEndID.argtypes=(c_void_p,c_ulong)



# 加载DLL


def init_canfd_channel(channel, abit_br=1000000, dbit_br=4000000):
    """初始化CANFD通道"""
    # 打开设备
    dev_handle = canDLL.ZCAN_OpenDevice(VCI_USBCAN2, 0, 0)
    if dev_handle == 0:
        raise Exception("设备打开失败")

    # 设置波特率
    if canDLL.ZCAN_SetAbitBaud(dev_handle, channel, abit_br) != STATUS_OK:
        raise Exception("仲裁域波特率设置失败")
    if canDLL.ZCAN_SetDbitBaud(dev_handle, channel, dbit_br) != STATUS_OK:
        raise Exception("数据域波特率设置失败")

    # 初始化通道配置
    class ZCAN_CHANNEL_INIT_CONFIG(Structure):
        _fields_ = [("can_type", c_uint),
                    ("config", c_byte*256)]  # 简化配置结构

    init_config = ZCAN_CHANNEL_INIT_CONFIG()
    init_config.can_type = TYPE_CANFD

    ch_handle = canDLL.ZCAN_InitCAN(dev_handle, channel, byref(init_config))
    if ch_handle == 0:
        raise Exception("通道初始化失败")

    # 启动通道
    if canDLL.ZCAN_StartCAN(ch_handle) != STATUS_OK:
        raise Exception("通道启动失败")

    return dev_handle, ch_handle

def build_config_frame(sensor_id, command, params):
    """构建配置帧"""
    frame = ZCAN_TransmitFD_Data()
    frame.transmit_type = 0  # 正常发送
    frame.frame.eff = 1       # 扩展帧
    frame.frame.rtr = 0       # 数据帧
    
    # 计算帧ID
    frame_id = 0x200 + sensor_id * 0x10
    frame.frame.can_id = frame_id
    
    # 填充数据
    data = bytes([0xAA, 0xAA])          # 起始码
    data += frame_id.to_bytes(2, 'little') # 帧ID
    data += bytes([command])            # 命令
    data += params                      # 参数
    data += bytes([0x55, 0x55])         # 结束码
    
    # 填充到CANFD帧
    frame.frame.len = len(data)
    for i in range(min(frame.frame.len, 64)):
        frame.frame.data[i] = data[i]
    
    return frame

def parse_target_data(data):
    result = [0,0,0,0]#目标ID，X坐标，Y坐标,目标高度
    """解析目标数据"""
    if len(data) < 8: return None
    #print(data.hex())
    # 解析点云数据（0x701）
    target_id = data[0] & 0x7F #目标ID
    result[0] = target_id / 8

    dist_y = ((data[1]*32) + (data[2] >> 3)) * 0.05 - 100
    dist_y = round(dist_y, 6)
    dist_x = (((data[2] & 0x07)*256) + data[3]) * 0.05 - 50
    dist_x = round(dist_x, 6)
    result[1] = dist_x
    result[2] = dist_y
    dist_z = ((data[9] * 4) + (data[10] >> 6)) * 0.1 - 30
    dist_z = round(dist_z, 6)
    result[3] = dist_z
    return result
    result[3] = dist_y
    return result


    """
    dist_long = ((data[1] << 5) | (data[2] >> 3)) * 0.05 - 100
    dist_lat = (((data[2] & 0x07) << 8) | data[3]) * 0.05 - 50
    speed = ((data[4] << 2) | (data[5] >> 6)) * 0.25 - 128
    
    return {
        'id': target_id,
        'x': round(dist_lat, 2),
        'y': round(dist_long, 2),
        'speed': round(speed, 2)
    }
    """







def SR75(OUT,Open,File_number,rader_channel = 0,qdb = 1000000,ddb = 4000000,floder_path = "",a=1.0,b=1.0,c=1.0,d=1.0): #rader_channel 0或1 雷达的通道,Modelss[4~7]是探测的X,Y范围
    
    message = []
    result = [0,0,0,0]#目标ID，X坐标，Y坐标,目标高度
    file_number = 0
    file_path = os.path.join(floder_path,f"cloud_{file_number}.txt")
    try:
        # 初始化CANFD通道
        dev_handle, ch_handle = init_canfd_channel(rader_channel,qdb,ddb)
        print("CANFD通道初始化成功")
        """
        # 设置雷达ID为1
        config_frame = build_config_frame(RADAR_ID, 0x82, bytes([0x01, 0x80, 0x00, 0x00]))
        ret = canDLL.ZCAN_TransmitFD(ch_handle, byref(config_frame), 1)
        if ret != 1:
            raise Exception("配置指令发送失败")
        print("雷达ID配置指令已发送")
        """
        # 接收数据循环
        while (Open[0]):
            # 获取接收帧数量
            rx_num = canDLL.ZCAN_GetReceiveNum(ch_handle, TYPE_CANFD)
            if rx_num > 0:
                # 接收数据
                rcv_frames = (ZCAN_ReceiveFD_Data * rx_num)()
                received = canDLL.ZCAN_ReceiveFD(ch_handle, byref(rcv_frames), rx_num, 100)
                
                for i in range(received):
                    frame = rcv_frames[i].frame
                    data = bytes(frame.data[:frame.len])
                    
                    # 解析配置响应
                    if frame.can_id == 0x201 + RADAR_ID * 0x10:
                        OUT[9].insert("end", f"帧ID = {frame.can_id}\n")
                        #print(f"配置响应: {data.hex()}")
                        try:
                            kkkk = 0
                            with open(file_path, 'w', encoding='utf-8') as file:
                                for i in range(len(message)):
                                    try:
                                        if(a <=  float(message[i][1]) and b >= float(message[i][1]) and c <= float(message[i][2]) and d >= float(message[i][2])):
                                            file.write(str(message[i][1]) + " " + str(message[i][2]) + " " + str(message[i][3]) + "\n")
                                            kkkk = kkkk + 1
                                        #print("文件 :  cloud_" + str(file_number) + "   内容: " + str(message[i][1]) + " " + str(message[i][2]) + " " + str(message[i][3]) + "写入完毕")
                                    except Exception as e:
                                        print(f'写入文件时发生错误: {e}')
                                if kkkk > 0 :        
                                    file_number = file_number + 1
                                    file_path = os.path.join(floder_path,f"cloud_{file_number}.txt")
                                    #print("")
                                    #print("\t <新的文件> \t")
                                    File_number[0] = file_number - 1
                                    message.clear()
                        except Exception as e:
                                print(f"写入文件时出错: {e}")
                    # 解析点云数据

                    if frame.can_id == 0x701:
                        OUT[9].insert("end", f"帧ID = {frame.can_id}\n")
                        OUT[9].insert("end", f"帧内容 = {data}\n")
                        try:
                            # 向文件中写入内容
                            if len(data) == 64 :
                                target = parse_target_data(data)
                                result = target
                                message.append(result)
                            #elif len(data) == 8 :
                                
                                """
                                with open(file_path, 'w', encoding='utf-8') as file:
                                    for i in range(len(message)):
                                        try:
                                            file.write(str(message[i][1]) + " " + str(message[i][2]) + " " + str(message[i][3]) + "\n")
                                            #print("文件 :  cloud_" + str(file_number) + "   内容: " + str(message[i][1]) + " " + str(message[i][2]) + " " + str(message[i][3]) + "写入完毕")
                                            
                                        except Exception as e:
                                            print(f'写入文件时发生错误: {e}')
                                file_number = file_number + 1
                                file_path = os.path.join(floder_path,f"cloud_{file_number}.txt")
                                #print("")
                                #print("\t <新的文件> \t")
                                File_number[0] = file_number - 1
                                message.clear()
                                """
                        except Exception as e:
                                print(f"写入文件时出错: {e}")

    except Exception as e:
        print(f"发生错误: {str(e)}")

    canDLL.ZCAN_CloseDevice(dev_handle)
    print("设备已关闭")






def main():
    Radar_is_on = [True]
    SR75(Radar_is_on)


    
"""
    try:
        # 初始化CANFD通道
        dev_handle, ch_handle = init_canfd_channel(1)
        print("CANFD通道初始化成功")
        
        # 设置雷达ID为1
        config_frame = build_config_frame(RADAR_ID, 0x82, bytes([0x01, 0x80, 0x00, 0x00]))
        ret = canDLL.ZCAN_TransmitFD(ch_handle, byref(config_frame), 1)
        if ret != 1:
            raise Exception("配置指令发送失败")
        print("雷达ID配置指令已发送")
        
        # 接收数据循环
        while True:
            # 获取接收帧数量
            rx_num = canDLL.ZCAN_GetReceiveNum(ch_handle, TYPE_CANFD)
            if rx_num > 0:
                # 接收数据
                rcv_frames = (ZCAN_ReceiveFD_Data * rx_num)()
                received = canDLL.ZCAN_ReceiveFD(ch_handle, byref(rcv_frames), rx_num, 100)
                
                for i in range(received):
                    frame = rcv_frames[i].frame
                    data = bytes(frame.data[:frame.len])
                    
                    # 解析配置响应
                    if frame.can_id == 0x201 + RADAR_ID * 0x10:
                        print(f"配置响应: {data.hex()}")
                    
                    # 解析点云数据
                    elif frame.can_id == 0x701:
                        if len(data) == 64 :
                            target = parse_target_data(data)
                            print(target)
                        elif len(data) == 8 :
                            print("")
                            print("\t \t \t <<<新的一帧>>> \t \t \t")
                        #if target:
                        #    print(f"目标{target['id']}: X={target['x']}m, Y={target['y']}m, 速度={target['speed']}m/s")
            
            time.sleep(0.01)

    except Exception as e:
        print(f"发生错误: {str(e)}")

        canDLL.ZCAN_CloseDevice(dev_handle)
        print("设备已关闭")
"""

if __name__ == "__main__":
    main()