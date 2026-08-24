from itertools import combinations

def brute_force(graph):
    nodes = list(graph.keys())
    n = len(nodes)
    all_nodes_set = set(nodes)

    closed_neighborhoods = {u: set(graph[u]) | {u} for u in nodes}

    for r in range(1, n + 1):
        for subset in combinations(nodes, r):

            covered = set()
            for node in subset:
                covered.update(closed_neighborhoods[node])

            if covered == all_nodes_set:
                return list(subset)
                
    return nodes