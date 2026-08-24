import math
import matplotlib.pyplot as plt
import random

def draw_graph(graph: dict, dominating_set: set, title: str = "Graph Dominating Set"):
    nodes = list(graph.keys())
    n = len(nodes)
    dominating_set = set(dominating_set)

    pos = {}
    radius = 1.0
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / n
        pos[node] = (radius * math.cos(angle), radius * math.sin(angle))

    plt.figure(figsize=(7, 7))

    drawn_edges = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            edge = tuple(sorted((u, v)))
            if edge not in drawn_edges:
                drawn_edges.add(edge)
                plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 
                         color='#7f8c8d', linewidth=1.5, zorder=1)

    for node in nodes:
        x, y = pos[node]
        
        if node in dominating_set:
            plt.scatter(x, y, s=800, color='#2ecc71', edgecolors='black', linewidths=2, zorder=2)
        else:
            plt.scatter(x, y, s=800, color='white', edgecolors='black', linewidths=2, zorder=2)

        plt.text(x, y, str(node), fontsize=11, fontweight='bold', color='black',
                 ha='center', va='center', zorder=3)

    plt.title(title, fontsize=13, fontweight='bold', pad=15)
    plt.xlim(-1.3, 1.3)
    plt.ylim(-1.3, 1.3)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def read_graph(filename):
    graph = {}

    with open(filename, "r") as f:
        n = int(f.readline().strip())

        for line in f:
            line = line.strip()

            if not line:
                continue

            vertex, neighbors = line.split(":", 1)
            vertex = int(vertex)

            if neighbors.strip():
                graph[vertex] = list(map(int, neighbors.split()))
            else:
                graph[vertex] = []

    return graph

def generate_graph(n=10000, average_degree=200, seed=12345):
    rng = random.Random(seed)

    target_edges = int(n * average_degree / 2)

    adjacency = [[] for _ in range(n)]
    edges = set()

    for v in range(1, n):
        u = rng.randrange(v)

        edges.add((u, v))

        adjacency[u].append(v)
        adjacency[v].append(u)

    remaining = target_edges - (n - 1)

    while remaining > 0:
        u = rng.randrange(n)
        v = rng.randrange(n)

        if u == v:
            continue

        if u > v:
            u, v = v, u

        edge = (u, v)

        if edge in edges:
            continue

        edges.add(edge)

        adjacency[u].append(v)
        adjacency[v].append(u)

        remaining -= 1

    for neighbors in adjacency:
        neighbors.sort()

    return {i: neighbors for i, neighbors in enumerate(adjacency)}

def save_graph(graph, filename):
    with open(filename, "w") as f:
        f.write(f"{len(graph)}\n")

        for v in graph:
            neighbors = " ".join(map(str, graph[v]))
            f.write(f"{v}: {neighbors}\n")