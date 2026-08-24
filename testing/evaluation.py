import glob
import time
import os
import pandas as pd
from utilities.graph import read_graph
from algorithms.vns import VNS
from algorithms.brute_force import brute_force
from algorithms.genetic import genetic_algorithm
from algorithms.linear_programing import linear_programing

def evaluate_algorithms(folder, do_brute_force = True):
    files = sorted(glob.glob(f"{folder}/*.txt"))

    vns_success = 0
    vns_np_success = 0
    ga_success = 0

    vns_gap = 0
    vns_np_gap = 0
    ga_gap = 0

    linear_time = 0
    vns_time = 0
    vns_np_time = 0
    ga_time = 0
    bf_time = 0

    total = len(files)
    if do_brute_force:
        total_tasks = 5 * total
    else:
        total_tasks = 4 * total
    finished_tasks = 0

    def progress():
        print(
            f"\rProgress: {finished_tasks}/{total_tasks} "
            f"({finished_tasks / total_tasks * 100:.0f}%)",
            end="",
            flush=True
        )

    progress()

    for filename in files:

        graph = read_graph(filename)

        # ==================================================
        # Linear Programming
        # ==================================================

        start = time.perf_counter()

        exact = linear_programing(graph)

        elapsed = time.perf_counter() - start

        linear_time += elapsed

        optimum = len(exact)

        finished_tasks += 1
        progress()

        # ==================================================
        # Brute force
        # ==================================================

        if do_brute_force:
            start = time.perf_counter()

            result = brute_force(graph)

            elapsed = time.perf_counter() - start

            bf_time += elapsed

            finished_tasks += 1
            progress()

        # ==================================================
        # VNS - no pruning
        # ==================================================

        start = time.perf_counter()

        result = VNS(
            graph,
            1500,
            12,
            do_prune=False
        )

        elapsed = time.perf_counter() - start
        vns_np_time += elapsed

        vns_np_size = len(result.get_selected_nodes())

        if vns_np_size == optimum:
            vns_np_success += 1

        vns_np_gap += (
            (vns_np_size - optimum) / optimum
        )

        finished_tasks += 1
        progress()

        # ==================================================
        # VNS
        # ==================================================

        start = time.perf_counter()

        result = VNS(
            graph,
            1500,
            12
        )

        elapsed = time.perf_counter() - start
        vns_time += elapsed

        vns_size = len(result.get_selected_nodes())

        if vns_size == optimum:
            vns_success += 1

        vns_gap += (
            (vns_size - optimum) / optimum
        )

        finished_tasks += 1
        progress()

        # ==================================================
        # Genetic Algorithm
        # ==================================================

        start = time.perf_counter()

        result = genetic_algorithm(
            200,
            graph,
            eliteSize=10,
            numGenerations=800,
            selectionSize=100,
            mutationSize=75,
            mutationRate=0.06
        )

        elapsed = time.perf_counter() - start
        ga_time += elapsed

        ga_size = len(result.get_selected_nodes())

        if ga_size == optimum:
            ga_success += 1

        ga_gap += (
            (ga_size - optimum) / optimum
        )

        finished_tasks += 1
        progress()

    print()

    # ======================================================
    # Build DataFrame
    # ======================================================

    data = [
        {
            "Algorithm": "Linear Programming",
            "Success": total,
            "Success %": 100.0,
            "Average Gap %": 0.0,
            "Average Time (s)": linear_time / total
        },
        {
            "Algorithm": "VNS",
            "Success": vns_success,
            "Success %": vns_success / total * 100,
            "Average Gap %": vns_gap / total * 100,
            "Average Time (s)": vns_time / total
        },
        {
            "Algorithm": "VNS (no pruning)",
            "Success": vns_np_success,
            "Success %": vns_np_success / total * 100,
            "Average Gap %": vns_np_gap / total * 100,
            "Average Time (s)": vns_np_time / total
        },
        {
            "Algorithm": "Genetic Algorithm",
            "Success": ga_success,
            "Success %": ga_success / total * 100,
            "Average Gap %": ga_gap / total * 100,
            "Average Time (s)": ga_time / total
        }
    ]

    if do_brute_force:
        data.insert(1, {
            "Algorithm": "Brute force",
            "Success": total,
            "Success %": 100.0,
            "Average Gap %": 0.0,
            "Average Time (s)": bf_time / total
        })

    return pd.DataFrame(data)

import time
import pandas as pd


def evaluate_on_graph(graph, do_brute_force = True):
    # Results
    vns_success = 0
    vns_np_success = 0
    ga_success = 0

    vns_gap = 0
    vns_np_gap = 0
    ga_gap = 0
    bf_time = 0

    # ==================================================
    # Linear Programming
    # ==================================================

    start = time.perf_counter()

    exact = linear_programing(graph)

    linear_time = time.perf_counter() - start

    optimum = len(exact)

    print("Finished linear!")

    # ==================================================
    # Brute force
    # ==================================================

    if do_brute_force:
        start = time.perf_counter()

        result = brute_force(graph)

        bf_time = time.perf_counter() - start

        print("Finished brute force!")

    # ==================================================
    # VNS no pruning
    # ==================================================

    start = time.perf_counter()

    result = VNS(graph, 3000, 20, do_prune=False)

    vns_np_time = time.perf_counter() - start

    vns_np_size = len(result.get_selected_nodes())

    if vns_np_size == optimum:
        vns_np_success += 1

    vns_np_gap += (vns_np_size - optimum) / optimum

    print("Finished VNS(no pruning)!")

    # ==================================================
    # VNS
    # ==================================================

    start = time.perf_counter()

    result = VNS(graph, 3000, 20)

    vns_time = time.perf_counter() - start

    vns_size = len(result.get_selected_nodes())

    if vns_size == optimum:
        vns_success += 1

    vns_gap += (vns_size - optimum) / optimum

    print("Finished VNS!")

    # ==================================================
    # GA
    # ==================================================

    start = time.perf_counter()

    result = genetic_algorithm(
        200, graph,
        eliteSize=10,
        numGenerations=1000,
        selectionSize=50,
        mutationSize=75,
        mutationRate=0.05
    )

    ga_time = time.perf_counter() - start

    ga_size = len(result.get_selected_nodes())

    if ga_size == optimum:
        ga_success += 1

    ga_gap += (ga_size - optimum) / optimum

    print("Finished genetic!")

    # ==================================================
    # DataFrame
    # ==================================================

    results = [
        {
            "Algorithm": "Linear Programming",
            "Success": 1,
            "Success %": 100.0,
            "Average Gap %": 0.0,
            "Average Time (s)": linear_time
        },
        {
            "Algorithm": "VNS",
            "Success": vns_success,
            "Success %": vns_success * 100,
            "Average Gap %": vns_gap * 100,
            "Average Time (s)": vns_time
        },
        {
            "Algorithm": "VNS (no pruning)",
            "Success": vns_np_success,
            "Success %": vns_np_success * 100,
            "Average Gap %": vns_np_gap * 100,
            "Average Time (s)": vns_np_time
        },
        {
            "Algorithm": "Genetic Algorithm",
            "Success": ga_success,
            "Success %": ga_success * 100,
            "Average Gap %": ga_gap * 100,
            "Average Time (s)": ga_time
        }
    ]

    if do_brute_force:
        results.insert(1, {
            "Algorithm": "Brute force",
            "Success": 1,
            "Success %": 100.0,
            "Average Gap %": 0.0,
            "Average Time (s)": bf_time
        })

    return pd.DataFrame(results)

def save_evaluation(df, filename):
    os.makedirs(f"{os.path.dirname(filename)}.csv", exist_ok=True)
    df.to_csv(filename, index=False)