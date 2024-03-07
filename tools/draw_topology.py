import networkx as nx
import matplotlib.pyplot as plt

def draw_topology(G, ROUTE):
    # 绘制图形
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, seed=42)  # 使用 spring layout 进行布局
    nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=8)

    # 绘制路径
    for i, path in enumerate(ROUTE):
        edges = [(path[2][j], path[2][j + 1]) for j in range(len(path[2]) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.7, edge_color='r', label=f"Path {i + 1}")

    # 显示图形
    plt.title('Autonomous System Topology with Cross Connections (400 ASes)')
    plt.show()
