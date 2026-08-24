import random

class Solution:
    def __init__(self, graph, generate=True):
        self.graph = graph
        self.nodes = list(graph.keys())
        self.num_nodes = len(self.nodes)
        
        if generate:
            self.code = [random.choice([0, 1]) for _ in range(self.num_nodes)]
            self.repair()
            self.prune()
        else:
            self.code = [0] * self.num_nodes
            self.fitness = None
            return

        self.fitness = self.fitnessFunction()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def repair(self):
        while not self.is_valid():

            selected = self.get_selected_nodes()

            uncovered = set(self.nodes)

            for u in selected:
                uncovered.discard(u)
                uncovered.difference_update(self.graph[u])

            best_vertex = None
            best_cover = -1

            for v in self.nodes:
                if v in selected:
                    continue

                cover = 0

                if v in uncovered:
                    cover += 1

                for u in self.graph[v]:
                    if u in uncovered:
                        cover += 1

                if cover > best_cover:
                    best_cover = cover
                    best_vertex = v

            if best_vertex is None:
                break

            i = self.nodes.index(best_vertex)
            self.code[i] = 1


    def prune(self):
        changed = True

        while changed:
            changed = False

            selected = list(self.get_selected_nodes())
            random.shuffle(selected)

            for v in selected:

                i = self.nodes.index(v)

                self.code[i] = 0

                if self.is_valid():
                    changed = True
                    break

                self.code[i] = 1


    def fitnessFunction(self):
        selected_nodes = {self.nodes[i] for i in range(self.num_nodes) if self.code[i] == 1}

        covered = set(selected_nodes)
        for u in selected_nodes:
            covered.update(self.graph[u])

        undominated_count = self.num_nodes - len(covered)

        penalty_factor = self.num_nodes + 1
        total_cost = len(selected_nodes) + (undominated_count * penalty_factor)

        self.fitness = total_cost
        return self.fitness

    def get_selected_nodes(self) -> set:
        return {self.nodes[i] for i in range(self.num_nodes) if self.code[i] == 1}

    def is_valid(self) -> bool:
            selected = self.get_selected_nodes()
            covered = set(selected)
            for u in selected:
                covered.update(self.graph[u])
            return len(covered) == self.num_nodes