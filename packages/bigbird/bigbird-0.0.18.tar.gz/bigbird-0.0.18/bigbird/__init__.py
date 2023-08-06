import numpy as np
import codecs, json
import copy
import random

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
        self.birds = []
        print('Initializing Population:')
        for i in range(size):
            print(str(i) + '/' + str(size), end='\r')
            self.birds.append(Bird(hl_count, layer_node_counts))
        print('')

    def breed(self):
        odds = []
        total_fit = 0
        for i in self.birds:
            total_fit += i.fitness
        for i in self.birds:
            odds.append(i.fitness / (total_fit - i.fitness))
        odds /= np.sum(odds)
        print([max(odds), min(odds)])
        
        next_gen = []
        print('Breeding:')
        while len(next_gen) < len(self.birds):
            print(str(len(next_gen)) + '/' + str(len(self.birds)), end='\r')
            p1 = np.random.choice(self.birds, 1, p=odds)[0]
            p2 = np.random.choice(self.birds, 1, p=odds)[0]
            mats = copy.copy(p1.matrices)
            for matrix in range(len(p1.matrices)):
                for row in range(len(p1.matrices[matrix])):
                    for col in range(len(p1.matrices[matrix][0])):
                        if np.random.uniform() < .5:
                            mats[matrix][row][col] = p2.matrices[matrix][row][col]
            next_gen.append(Bird(0, 0, mat=mats))
        print('')
        for i in range(len(self.birds)):
            del self.birds[-1]
        self.birds = next_gen

    def mutate(self, mutate_r8, radius_ratio, reinit=0.01, immune=1):
        police = []
        print('Mutating:')
        complete = 0
        for i in range(immune):
            print(str(complete) + '/' + str(len(self.birds)), end='\r')
            police.append(sorted(self.birds, key=lambda x: x.fitness)[-i])
            complete += 1
        for bird in self.birds:
            print(str(complete) + '/' + str(len(self.birds)), end='\r')
            complete += 1
            if np.random.uniform() < .98:
                for matrix in range(len(bird.matrices)):
                    for row in range(len(bird.matrices[matrix])):
                        for col in range(len(bird.matrices[matrix][0])):
                            if np.random.uniform() < mutate_r8:
                                bird.matrices[matrix][row][col] += np.random.normal(0, radius_ratio / np.sqrt(len(bird.matrices[matrix][0])), 1)[0]
        random.shuffle(self.birds)
        print('')
        for i in range(immune):
            del self.birds[i]
            self.birds.append(police[i])
        random.shuffle(self.birds)

class Bird:
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

    def save(self, fname='./big-bird.json'):
        record = []
        for i in self.matrices:
            record.append(i.tolist())
        json.dump(record, codecs.open(fname, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)