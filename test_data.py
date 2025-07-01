import os
import numpy as np
import warnings
import pickle

from tqdm import tqdm
from torch.utils.data import Dataset

warnings.filterwarnings('ignore')

def pc_normalize(pc):
    centroid = np.mean(pc, axis=0)
    pc = pc - centroid
    m = np.max(np.sqrt(np.sum(pc**2, axis=1)))
    pc = pc / m
    return pc

def farthest_point_sample(point, npoint):
    """
    Input:
        xyz: pointcloud data, [N, D]
        npoint: number of samples
    Return:
        centroids: sampled pointcloud index, [npoint, D]
    """
    N, D = point.shape
    xyz = point[:,:3]
    centroids = np.zeros((npoint,))
    distance = np.ones((N,)) * 1e10
    farthest = np.random.randint(0, N)
    for i in range(npoint):
        centroids[i] = farthest
        centroid = xyz[farthest, :]
        dist = np.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[mask] = dist[mask]
        farthest = np.argmax(distance, -1)
    point = point[centroids.astype(np.int32)]
    return point

class test_data(Dataset):
    def __init__(self,category_path,folder_path,args):#folder_path：测试文件所在文件夹的路径,category_path:类别文件的路径
        self.npoints = args.num_point
        self.uniform = args.use_uniform_sample
        self.use_normals = args.use_normals
        self.num_category = args.num_category

        self.catfile = category_path #读取识别的的类别数据
        self.cat = [line.rstrip() for line in open(self.catfile)]
        self.classes = dict(zip(self.cat, range(len(self.cat))))#读取类别文件的每一行并去除换行符，将类别名称与对应的索引映射到字典 self.classes 中。
        txt_files = []
        # 遍历指定目录及其子目录
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # 检查文件扩展名是否为txt
                if file.endswith('.txt'):
                    # 构建完整的文件路径
                    txt_files.append(os.path.join(root, file))

        self.datapath = [] #要测试文件的路径的列表
        for i in txt_files:
            self.datapath.append(("jump",i))#将类别名称与对应的文件路径元组添加到 self.datapath 列表中,类别名称用于计算预测的成功率，不需要预测成功率，所以无意义，全用jump
        print('The size of test data is %d' % (len(self.datapath)))


    def __len__(self): #返回数据集的长度
        return len(self.datapath)

    def _get_item(self, index): #返回索引对应的数据

        fn = self.datapath[index]
        cls = self.classes[self.datapath[index][0]]
        label = np.array([cls]).astype(np.int32)
        point_set = np.loadtxt(fn[1], delimiter=' ').astype(np.float32)
        if self.uniform:
            point_set = farthest_point_sample(point_set, self.npoints)
        else:
            point_set = point_set[0:self.npoints, :]
                
        point_set[:, 0:3] = pc_normalize(point_set[:, 0:3])
        if not self.use_normals:
            point_set = point_set[:, 0:3]

        return point_set, label[0]

    def __getitem__(self, index): #返回索引对应的数据
        return self._get_item(index)


if __name__ == '__main__':
    import torch

    data = test_data('/Human_Posture_Recognition_30frames_[monther]/', split='train')#训练的数据文件存放的路径
    DataLoader = torch.utils.data.DataLoader(data, batch_size=16, shuffle=True)
    for point, label in DataLoader:
        print(point.shape)
        print(label.shape)
