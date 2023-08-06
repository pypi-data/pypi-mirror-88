# Big Bird

Big Bird is a (hopefully) useful package designed to facilitate the quick and convenient creation of basic genetic algorithms in python.

## Example Code
```python
import bigbird

# Config Parameters
generation_size = 300                   # Creatures per generation
hidden_layer_count = 3                  # How many hidden layers each creature has
layer_node_counts = [10, 7, 7, 7, 3]    # No. of nodes in each layer (i.e. 10 input, 7 per hidden layer, 3 output)
mutation_rate = 0.35                    # Chance of a weight mutation occuring
step_ratio = 1 / 3                      # Ratio of mutation perturbation std dev to weight initialization std dev

population = bigbird.Population(generation_size, hidden_layer_count, layer_node_counts)

for generation in range(100):           # Train for 100 generation
    for bird in population:             # Evaluates each member in the population
        input = your_input_generation_function()
        output = bird.eval(input)
        decision = output.index(max(output))
        bird.fitness = your_fitness_evaluation_function(decision)
    
    population.breed()
    population.mutate()
```