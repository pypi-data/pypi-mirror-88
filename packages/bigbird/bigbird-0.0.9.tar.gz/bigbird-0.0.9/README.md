# Big Bird

Big Bird is a (hopefully) useful package designed to facilitate the quick and convenient creation of basic genetic algorithms in python.

## Example Code
```python
import bigbird

# Config Parameters
generation_size = 300
hidden_layer_count = 3
layer_node_counts = [10, 7, 7, 7, 3]
mutation_rate = 0.35
step_ratio = 1 / 3

population = bigbird.Population(generation_size, hidden_layer_count, layer_node_counts)

for generation in range(100):
    for bird in population:
        input = your_input_generation_function()
        output = bird.eval(input)
        decision = output.index(max(output))
        bird.fitness = your_fitness_evaluation_function(decision)
    
    population.breed()
    population.mutate(mutation_rate, step_ratio)
```