import random

import numpy as np

from snake_neural_network import SnakeNN

from matplotlib import pyplot as plt


snn = SnakeNN()

def create_population(size, num_chromosomes, min_chromosome, max_chromosome):
    pop = []
    for s in range(size):
        agent = []
        for j in range(num_chromosomes):
            agent.append(random.uniform(min_chromosome, max_chromosome))
        pop.append(agent)
    return pop

def fitness_func(agent, show=False):
    snn.set_weights(agent)
    apples, moves = snn.play(show)
    f = apples ** 3 + moves
    if apples == 0:
        f -= moves
    return f + 1
def selection_tournament(population, num_selected):
    population.sort(key=fitness_func, reverse=True)
    return population[:num_selected]

def selection_wheel(population, num_selected):
    fitness_vals = []
    for actor in population:
        fitness_vals.append(fitness_func(actor, False))  # TODO: change here the show value
    new_population = random.choices(population, weights=fitness_vals, cum_weights=None, k=num_selected)
    sorted_new_pop = [x for _, x in sorted(zip(fitness_vals, new_population), reverse=True)]
    return sorted_new_pop, np.average(fitness_vals)

def crossover(population, num_children):
    new_generation = population[:num_children//2]
    for i_c in range(num_children//2):
        parent1 = population[random.randint(0, len(population) - 1)]
        parent2 = population[random.randint(0, len(population) - 1)]
        child = []
        cut_index = random.randint(0, len(population[0]) - 1)
        for j in range(0, len(population[0])):
            if j < cut_index:
                child.append(parent1[j])
            else:
                child.append(parent2[j])
        new_generation.append(child)
    return new_generation

def mutation(population, num_mutations, min_chromosome, max_chromosome):
    for i_m in range(num_mutations):
        agent = population[random.randint(0, len(population) - 1)]
        agent[random.randint(0, len(agent) - 1)] = random.uniform(min_chromosome, max_chromosome)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pop_size = 100
    min_val = -1.  # maximum value of a chromosome
    max_val = 1.
    select_this_many = 20
    num_of_mutations = int(pop_size * 0.008)
    num_of_chromosomes = snn.num_chromosomes
    num_generations = 100
    selection_method = 'wheel'  # wheel or tournament

    p = create_population(pop_size, num_of_chromosomes, min_val, max_val)
    for i_gen in range(num_generations):
        print("Generation", i_gen)
        p = crossover(p, pop_size)
        mutation(p, num_of_mutations, min_val, max_val)
        p, avg_f = selection_wheel(p, num_selected=select_this_many)
        print("Generation", i_gen, " fitness", avg_f)

    snn.set_weights(p[0])
    while True:
        snn.play(show=True)
