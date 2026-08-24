import numpy as np
from docplex.mp.model import Model

def linear_programing(graph):
    nodes = list(graph.keys())

    model = Model(name="Minimum_Dominating_Set")

    x = model.binary_var_dict(nodes, name="x")
    model.minimize(model.sum(x[v] for v in nodes))

    for v in nodes:
        neighbors = graph[v]
        model.add_constraint(x[v] + model.sum(x[u] for u in neighbors) >= 1, ctname=f"cover_{v}")

    solution = model.solve()
    
    if solution:
        return [v for v in nodes if solution.get_value(x[v]) > 0.5]
    else:
        print("Optimalno rešenje nije pronađeno.")
        return []