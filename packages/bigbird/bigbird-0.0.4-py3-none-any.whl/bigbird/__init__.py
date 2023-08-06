import numpy as np
import copy

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def sig(x):
    return 1 / (1 + np.exp(-4.9 * x))

def xav(i):
    return np.random.normal(0, 1/np.sqrt(i), 1)[0]

def randomize(matrix):
    inputs = len(matrix[0])
    outputs = len(matrix)
    for i in range(outputs):
        for j in range(inputs):
            matrix[i][j] = xav(inputs)

    return matrix

class Population:
    def __init__(self, size, hl_count, layer_node_counts):
        self.creatures = []
        for i in range(size):
            self.creatures.append(Creature(hl_count, layer_node_counts))

    def breed(self):
        odds = []
        for i in self.creatures:
            odds.append(i.fitness)
        odds = softmax(odds)
        
        next_gen = []
        for i in range(len(self.creatures)):
            p1 = np.random.choice(self.creatures, 1, p=odds)[0]
            p2 = np.random.choice(self.creatures, 1, p=odds)[0]
            mats = copy.copy(p1.matrices)
            for matrix in range(len(p1.matrices)):
                for row in range(len(p1.matrices[matrix])):
                    for col in range(len(p1.matrices[matrix][0])):
                        if np.random.uniform() < .5:
                            mats[matrix][row][col] = p2.matrices[matrix][row][col]
            next_gen.append(Creature(0, 0, mat=mats))
        for i in range(len(self.creatures)):
            del self.creatures[-1]
        self.creatures = next_gen

    def mutate(self, mutate_r8, radius_ratio):
        for creature in self.creatures:
            for matrix in range(len(creature.matrices)):
                for row in range(len(creature.matrices[matrix])):
                    for col in range(len(creature.matrices[matrix][0])):
                        if np.random.uniform() < mutate_r8:
                            creature.matrices[matrix][row][col] += np.random.normal(0, 1/np.sqrt(len(creature.matrices[matrix][0])) * radius_ratio, 1)[0]
        



class Creature:
    def __init__(self, hl_count, layer_node_counts, mat = []):
        self.fitness = 0
        if mat:
            self.matrices = mat
        else:
            self.matrices = []
            for i in range(hl_count + 1):
                self.matrices.append(np.empty([layer_node_counts[i+1], layer_node_counts[i]]))
            for matrix in self.matrices:
                matrix = randomize(matrix)

    def eval(self, input):
        hidden = input[:]
        for matrix in self.matrices:
            hidden = sig(np.matmul(matrix, hidden))
        return hidden
