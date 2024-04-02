from common.individual import Individual
from common.population import Population
from common.individual_generators import *
from math import cos
import random

class Problem:

    def __init__(self,
                 objective,
                 repair,
                 num_of_variables,
                 variables_range,
                 num_of_individuals,
                 direction,
                 num_of_generations,
                 mutation,
                 expand=True,
                 initial_population_type = 0,
                 objective_vars = 0
                 ):
        self.num_of_variables = num_of_variables
        self.num_of_individuals = num_of_individuals
        self.objective = objective
        self.repair = repair
        self.expand = expand
        self.variables_range = variables_range
        self.direction = direction
        self.num_of_generations = num_of_generations
        self.variables = self.set_variables()
        self.mutation = mutation
        self.initial_population_type = initial_population_type
        
    # Define quais possíveis variáveis do problema
    def set_variables(self):
        variables = [i for i in range(min(self.variables_range), max(self.variables_range) + 1)]
        return variables

    # Cria a população inicial de modo aleatório
    def create_initial_population(self):
        population = Population()
        for k in range(self.num_of_individuals):
            individual = self.generate_individual()
            individual.id = k
            self.calculate_objectives(individual)
            population.append(individual)
            population.last_id = k
        return population


    # Gera um indivíduo
    def generate_individual(self):
        individual = Individual(self.direction)

        chaos_map = ChaosMaps(self.variables_range,self.num_of_variables)
        quasirandom_numbers = QuasiRandomNumberSequences(self.variables_range,self.num_of_variables)
        beta_function = BetaFunctionVariatios(self.variables_range,self.num_of_variables)

        if self.initial_population_type == 0:
            individual.features = [random.randint(min(self.variables_range), max(self.variables_range)) for x in range(self.num_of_variables)]
        elif self.initial_population_type == 1:
            individual.features = chaos_map.generic_logistic_map()
        elif self.initial_population_type == 2:
            individual.features = chaos_map.cosin_map_generation()
        elif self.initial_population_type == 3:
            individual.features = beta_function.latin_hypercube()
        elif self.initial_population_type == 4:
            individual.features = beta_function.multinomial()
        
        return individual

    # Calcula o valor da função objetivo
    def calculate_objectives(self, individual):
        individual.objective = [f(individual) for f in self.objective]
        individual.objective = individual.objective[0]
        self.repair_objective(individual)

    def repair_objective(self, individual):
        temp = [f(individual) for f in self.repair]
        individual = temp[0] 