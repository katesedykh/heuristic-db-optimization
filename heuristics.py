import random
import math


class GeneticAlgorithm:
    def __init__(self, population_size, gene_pool, mutation_rate, max_generations):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.gene_pool = gene_pool
        self.population = self._initialize_population()
        self.max_generations = max_generations

    def _initialize_population(self):
        return [[random.choice(self.gene_pool) for _ in range(len(self.gene_pool))] for _ in range(self.population_size)]

    def _fitness_function(self, individual):
        # Mock fitness function - in a real scenario, this would measure the performance of the query plan
        return random.uniform(0, 1) #placeholder

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
            for _ in range(self.population_size // 2):  # Assume population_size is even
                parent1, parent2 = self._select_parents()
                child1, child2 = self._crossover(parent1, parent2)
                new_population.extend([self._mutate(child1), self._mutate(child2)])
            self.population = new_population
        return max(self.population, key=self._fitness_function)

    def apply(self, parsed_query):
        self.population = self._initialize_population()

        for generation in range(self.max_generations):
            new_population = []
            for _ in range(self.population_size // 2):
                # Selection
                parent1, parent2 = self._select_parents()

                # Crossover
                child1, child2 = self._crossover(parent1, parent2)

                # Mutation
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)

                # Add new children to the new population
                new_population.extend([child1, child2])

            self.population = new_population

        # Select the best plan based on fitness
        best_plan = max(self.population, key=self._fitness_function)
        return best_plan


class SimulatedAnnealing:
    def __init__(self, initial_temp, cooling_rate, gene_pool, min_temperature):
        self.temperature = initial_temp
        self.cooling_rate = cooling_rate
        self.gene_pool = gene_pool
        self.min_temperature = min_temperature
        self.current_solution = random.choice(self.gene_pool)
        self.best_solution = self.current_solution

    def _initialize_state(self, parsed_query):
        # In a real implementation, this would create an initial valid query plan
        return "Initial Plan for " + str(parsed_query) #placeholder

    def _fitness_function(self, solution):
        # Mock fitness function - in a real scenario, this would measure the performance of the query plan
        return random.uniform(0, 1)  #placeholder

    def _get_neighbor(self, current_state):
        # This method should generate a "neighbor" state from the given current state
        # For simplicity, let's assume it makes a small random change to the current state
        neighbor = list(current_state)  # Assuming current_state is a list or similar structure
        pos_to_modify = random.randint(0, len(neighbor) - 1)
        neighbor[pos_to_modify] = random.choice(self.gene_pool)  # Make a small change
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

    def apply(self, parsed_query):
        self.current_solution = self._initialize_state(parsed_query)
        best_solution = self.current_solution

        while self.temperature > self.min_temperature:
            neighbor = self._get_neighbor(self.current_solution)
            current_cost = self._fitness_function(self.current_solution)
            neighbor_cost = self._fitness_function(neighbor)
            if self._acceptance_probability(current_cost, neighbor_cost) > random.random():
                self.current_solution = neighbor

            if self._fitness_function(self.current_solution) > self._fitness_function(best_solution):
                best_solution = self.current_solution

            self.temperature *= self.cooling_rate #cool down

        return best_solution


