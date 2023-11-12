import pickle
import os
import multiprocessing
import random
import numpy as np
import matplotlib.pyplot as plt
from snake_neural_network import SnakeNN

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
MULTITHREADING = True


# Save the training state of the generation and population within a dedicated file "save_state"
def save_training_state(generation, population, fitnesses):
    state = {
        'generation': generation,
        'population': population,
        'fitness': fitnesses
    }
    with open('save_state.pkl', 'wb') as file:
        pickle.dump(state, file)


# Load the training state if it exists, else, we generate a basic population
def load_training_state():
    if os.path.exists('save_state.pkl'):
        with open('save_state.pkl', 'rb') as file:
            state = pickle.load(file)
            print(state['generation'])
        return state['generation'], state['population'], state['fitness']
    else:
        return 0, create_population(pop_size, num_of_chromosomes, min_val, max_val), []


def create_population(size, num_chromosomes, min_chromosome, max_chromosome):
    pop = []
    for s in range(size):
        agent = []
        for j in range(num_chromosomes):
            agent.append(random.uniform(min_chromosome, max_chromosome))
        pop.append(agent)
    return pop


def fitness_func(agent, show=False):
    snn = SnakeNN()
    snn.set_weights(agent)
    apples, moves = snn.play(show)
    f = 0.001 + (2 * apples) ** 3 * moves
    return f


def selection_tournament(population, num_selected):
    population.sort(key=fitness_func, reverse=True)
    return population[:num_selected]


def selection_wheel(population, num_selected):
    fitness_vals = []
    pool = multiprocessing.Pool()
    if MULTITHREADING:
        for f in pool.map(fitness_func, population):
            fitness_vals.append(f)
    else:
        for actor in population:
            fitness_vals.append(fitness_func(actor))
    new_population = random.choices(population, weights=fitness_vals, cum_weights=None, k=num_selected)
    sorted_new_pop = [x for _, x in sorted(zip(fitness_vals, new_population), reverse=True)]
    return sorted_new_pop, np.average(fitness_vals)


def crossover(population, num_children, num_preserved):
    new_generation = population[:num_children - num_preserved]
    for i_c in range(num_children - num_preserved):
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
    pop_size = 300
    min_val = -1.  # maximum value of a chromosome
    max_val = 1.
    select_this_many = pop_size // 3
    num_of_mutations = int(pop_size * 0.008)
    num_of_chromosomes = SnakeNN().num_chromosomes
    num_generations = 400
    selection_method = 'wheel'  # wheel or tournament
    start_generation, p, fitnesses = load_training_state()

    for i_gen in range(start_generation, num_generations):
        if i_gen != 0:
            p = crossover(p, pop_size, select_this_many)
            mutation(p, num_of_mutations, min_val, max_val)
        p, avg_f = selection_wheel(p, num_selected=select_this_many)
        fitnesses.append(avg_f)
        save_training_state(i_gen + 1, p, fitnesses)

    snn_test = SnakeNN()
    snn_test.set_weights(p[0])

    plt.plot(range(len(fitnesses)), fitnesses)
    plt.show()

    while True:
        snn_test.play(show=True)
