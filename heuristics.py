import random
import math

class GeneticAlgorithm:
    def __init__(self, population_size, gene_pool, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.gene_pool = gene_pool
        self.population = self._initialize_population()

    def _initialize_population(self):
        return [[random.choice(self.gene_pool) for _ in range(len(self.gene_pool))] for _ in range(self.population_size)]

    def _fitness_function(self, individual):
        return sum(individual)  # Simplified fitness function

    def _mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual[i] = random.choice(self.gene_pool)
        return individual

    def _crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(self.gene_pool) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def _select_parents(self):
        weights = [self._fitness_function(individual) for individual in self.population]
        parent1 = random.choices(self.population, weights=weights, k=1)[0]
        parent2 = random.choices(self.population, weights=weights, k=1)[0]
        return parent1, parent2

    def run(self, generations):
        for _ in range(generations):
            new_population = []
            for _ in range(self.population_size // 2):  #assume population_size is even
                parent1, parent2 = self._select_parents()
                child1, child2 = self._crossover(parent1, parent2)
                new_population.extend([self._mutate(child1), self._mutate(child2)])
            self.population = new_population
        return max(self.population, key=self._fitness_function)


class SimulatedAnnealing:
    def __init__(self, initial_temp, cooling_rate, gene_pool):
        self.temperature = initial_temp
        self.cooling_rate = cooling_rate
        self.gene_pool = gene_pool
        self.current_solution = random.choice(self.gene_pool)
        self.best_solution = self.current_solution

    def _fitness_function(self, solution):
        return sum(solution)

    def _get_neighbor(self):
        neighbor = list(self.current_solution)
        pos_to_modify = random.randint(0, len(neighbor) - 1)
        neighbor[pos_to_modify] = random.choice(self.gene_pool)
        return neighbor

    def _acceptance_probability(self, old_cost, new_cost):
        if new_cost > old_cost:
            return 1
        else:
            return math.exp((new_cost - old_cost) / self.temperature)

    def run(self):
        while self.temperature > 1:
            neighbor = self._get_neighbor()
            current_cost = self._fitness_function(self.current_solution)
            neighbor_cost = self._fitness_function(neighbor)
            if self._acceptance_probability(current_cost, neighbor_cost) > random.random():
                self.current_solution = neighbor
                if self._fitness_function(self.current_solution) > self._fitness_function(self.best_solution):
                    self.best_solution = self.current_solution
            self.temperature *= 1 - self.cooling_rate
        return self.best_solution
