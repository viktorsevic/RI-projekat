import random
from .problem_solution import Solution


def is_valid(solution):
    return solution.is_valid()


def shake(solution, k):
    indexes = random.sample(
        range(solution.num_nodes),
        min(k, solution.num_nodes)
    )

    for i in indexes:
        solution.code[i] = not solution.code[i]

    solution.fitnessFunction()


def VNS(graph, numIters, max_k, do_prune=True):
    current = Solution(graph)

    best = Solution(graph, generate=False)
    best.code = current.code.copy()
    best.fitness = current.fitness

    for _ in range(numIters):

        k = 1

        while k <= max_k:
            candidate = Solution(graph, generate=False)
            candidate.code = current.code.copy()
            candidate.fitness = current.fitness

            shake(candidate, k)
            candidate.repair()
            if do_prune:
                candidate.prune()

            candidate.fitness = candidate.fitnessFunction()

            if candidate.fitness < current.fitness:
                current = candidate
                if current.fitness < best.fitness:
                    best.code = current.code.copy()
                    best.fitness = current.fitness
                    k = 1
                else:
                    k += 1
            else:
                k += 1

    return best