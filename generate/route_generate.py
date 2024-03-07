import random

import networkx as nx


def route_generate(G, num_paths_to_select=30):
    paths_selected = 0
    paths = []
    while paths_selected < num_paths_to_select:
        # 随机选择起始和结束节点
        start_node = random.choice(list(G.nodes))
        end_node = random.choice(list(G.nodes))

        if start_node == end_node:
            continue
        if not nx.has_path(G, start_node, end_node):
            continue

        # 找到路径
        path = nx.shortest_path(G, start_node, end_node)

        paths_selected += 1
        paths.append(path)

    return paths
