import networkx as nx
import random


def topology_generate(num_node=400):
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
