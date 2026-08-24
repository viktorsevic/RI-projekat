import random
import copy
from .problem_solution import Solution

def selection(population, selectionSize):
    participants = random.sample(population, selectionSize)
    return min(participants)

def crossover(p1, p2, c1, c2):
    j = random.randrange(len(p1.code))

    c1.code[:j] = p1.code[:j]
    c2.code[j:] = p1.code[j:]

    c1.code[j:] = p2.code[j:]
    c2.code[:j] = p2.code[:j]

    c1.repair()
    c2.repair()

    if random.uniform(0,1) < 0.1:
        c1.prune()
    if random.uniform(0,1) < 0.1:
        c2.prune()

    c1.fitness = c1.fitnessFunction()
    c2.fitness = c2.fitnessFunction()

def mutation(population, mutationSize, mutationRate):
    participants = random.sample(population, mutationSize)
    for participant in participants:
        if random.uniform(0, 1) < mutationRate:
            i = random.randrange(len(participant.code))
            participant.code[i] = 1 - participant.code[i]

            participant.fitness = participant.fitnessFunction()

def genetic_algorithm(populationSize, graph, eliteSize, numGenerations, selectionSize, mutationSize, mutationRate):
    population = [Solution(graph) for _ in range(populationSize)]

    for _ in range(numGenerations):
        newPopulation = []
        population.sort()

        for i in range(eliteSize):
            newPopulation.append(copy.deepcopy(population[i]))

        for i in range(eliteSize, populationSize, 2):
            p1 = selection(population, selectionSize)
            p2 = selection(population, selectionSize)

            c1 = Solution(graph, generate=False)
            c2 = Solution(graph, generate=False)
            newPopulation.append(c1)
            newPopulation.append(c2)

            crossover(p1, p2, c1, c2)

        mutation(newPopulation, mutationSize, mutationRate)
        population = newPopulation

    return min(population)