import os
import pickle
import random

import networkx as nx

from tools.tools import strcat


class GraphManager:
    G_dir = 'record/'
    @staticmethod
    def gen_topology(num_node=400):
        # 创建图
        G = nx.Graph()

        # 添加自治域节点
        num_autonomous_systems = num_node
        autonomous_systems = range(1, num_autonomous_systems + 1)
        G.add_nodes_from(autonomous_systems)

        # 添加自治域间连接
        for i in range(1, num_autonomous_systems):
            # 随机选择一个节点进行连接
            connected_node = random.randint(1, num_autonomous_systems)
            if i == connected_node:
                continue
            G.add_edge(i, connected_node)

        return G
    @classmethod
    def save_G(cls, seed, G):
        G_dir = strcat(cls.G_dir, seed)
        G_path = strcat(G_dir)
        if not os.path.exists(G_dir):
            os.mkdir(G_dir)
        if not os.path.exists(G_path):
            os.mkdir(G_path)
        with open(G_path, 'wb') as f:
            f.write(G)

    @classmethod
    def load_G(cls,seed):
        G_path = strcat(cls.G_dir, seed)
        if not os.path.exists(G_path):
            G = cls.gen_topology()
            cls.save_G(seed, G)
        else:
            with open(G_path, 'rb') as f:
                G = pickle.load(f)
        return G



