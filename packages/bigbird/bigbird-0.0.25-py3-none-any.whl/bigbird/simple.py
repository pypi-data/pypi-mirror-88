import numpy as np
import codecs, json
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

class SimplePopulation:
    def __init__(self, size, hl_count, layer_node_counts):
        self.lake = []
        self.birds = []
        for i in range(size):
            self.birds.append(SimpleBird(hl_count, layer_node_counts))

    def store(self, immune):
        for i in range(len(self.lake)):
            del self.lake[i]
        i = sorted(self.birds, key=lambda x: x.fitness)[-immune:]
        for bird in i:
            self.lake.append(copy.deepcopy(bird))

    def retrieve(self):
        np.random.shuffle(self.birds)
        for i in range(len(self.lake)):
            del self.birds[0]
            self.birds.append(copy.deepcopy(self.lake[i]))
        for i in range(len(self.lake)):
            del self.lake[0]

    def breed(self):
        odds = []
        total_fit = 0
        for i in self.birds:
            total_fit += i.fitness
        for i in self.birds:
            odds.append(i.fitness / (total_fit - i.fitness))
        odds /= np.sum(odds)
        
        next_gen = []
        while len(next_gen) < len(self.birds):
            p1 = np.random.choice(self.birds, 1, p=odds)[0]
            p2 = np.random.choice(self.birds, 1, p=odds)[0]
            mats = copy.deepcopy(p1.matrices)
            for matrix in range(len(p1.matrices)):
                for row in range(len(p1.matrices[matrix])):
                    for col in range(len(p1.matrices[matrix][0])):
                        if np.random.uniform() < .5:
                            mats[matrix][row][col] = p2.matrices[matrix][row][col]
            next_gen.append(SimpleBird(0, 0, mat=mats))
        for i in range(len(self.birds)):
            del self.birds[-1]
        self.birds = next_gen

    def mutate(self, mutate_r8, radius_ratio, reinit=0.01):
        for bird in self.birds:
            if np.random.uniform() < .98:
                for matrix in range(len(bird.matrices)):
                    for row in range(len(bird.matrices[matrix])):
                        for col in range(len(bird.matrices[matrix][0])):
                            if np.random.uniform() < mutate_r8:
                                if np.random.uniform() < reinit:
                                    bird.matrices[matrix][row][col] = np.random.normal(0, 1 / np.sqrt(len(bird.matrices[matrix][0])), 1)[0]
                                else:
                                    bird.matrices[matrix][row][col] += np.random.normal(0, radius_ratio / np.sqrt(len(bird.matrices[matrix][0])), 1)[0]

class SimpleBird:
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
