# Big Bird

Big Bird is a (hopefully) useful package designed to facilitate the quick and convenient creation of basic genetic algorithms in python.

## Usage
```python
import bigbird

# Big Bird Config
pop_size = 3000
hl_count = 2
layer_counts = [8, 5, 5, 3]
m_r8 = 0.14
step_ratio = 1/3
reinit_r = 0.01
immune = 30

max_generation = 300

population = bigbird.Population(pop_size, hl_count, layer_counts)

for generation in range(max_generation):
    for bird in population.birds:
        bird_inp = your_input_generation_fn()
        bird_out = bird.eval(bird_inp)
        decision = output.tolist().index(max(output))
        bird.fitness = your_fitness_fn(decision)

    champ = sorted(population.birds, key=lambda x: x.fitness)[-1]
    champ.save(fname='./hall-of-fame/champ-' + str(generation) + '.json')

    population.store(immune)
    population.breed()
    population.mutate(m_r8, step_ratio, reinit=reinit_r)
    population.retrieve()
```