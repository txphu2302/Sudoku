import random
import copy

def get_fixed_positions(grid):
    # Returns a 9x9 matrix with True for fixed cells and False otherwise.
    fixed = [[True if grid[i][j] != 0 else False for j in range(9)] for i in range(9)]
    return fixed

def create_candidate(grid, fixed):
    candidate = copy.deepcopy(grid)
    for i in range(9):
        missing = [n for n in range(1, 10) if n not in candidate[i]]
        random.shuffle(missing)
        for j in range(9):
            if not fixed[i][j]:
                candidate[i][j] = missing.pop()
    return candidate

def create_initial_population(grid, fixed, population_size):
    return [create_candidate(grid, fixed) for _ in range(population_size)]

def fitness(candidate):
    # Conflict count for columns and 3x3 blocks.
    conflicts = 0
    # Column conflicts.
    for j in range(9):
        col = [candidate[i][j] for i in range(9)]
        conflicts += (9 - len(set(col)))
    # Block conflicts.
    for block_i in range(3):
        for block_j in range(3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(candidate[block_i * 3 + i][block_j * 3 + j])
            conflicts += (9 - len(set(block)))
    return conflicts

def tournament_selection(population, fitnesses, tournament_size=3):
    selected = random.sample(list(zip(population, fitnesses)), tournament_size)
    selected.sort(key=lambda x: x[1])
    return copy.deepcopy(selected[0][0])

def crossover(parent1, parent2, fixed):
    child = []
    # For each row, choose one parent's entire row ensuring fixed remains.
    for i in range(9):
        row = parent1[i] if random.random() < 0.5 else parent2[i]
        # Repair: enforce fixed cell values from the original puzzle.
        fixed_nums = {j: parent1[i][j] for j in range(9) if fixed[i][j]}
        # Extract mutable positions and fill missing numbers to guarantee permutation.
        mutable_vals = [row[j] for j in range(9) if not fixed[i][j]]
        fixed_set = set(fixed_nums.values())
        missing = [n for n in range(1,10) if n not in fixed_set]
        if len(mutable_vals) != len(missing):
            random.shuffle(missing)
            mutable_vals = missing
        new_row = []
        m_iter = iter(mutable_vals)
        for j in range(9):
            if fixed[i][j]:
                new_row.append(fixed_nums[j])
            else:
                new_row.append(next(m_iter))
        child.append(new_row)
    return child

def mutate(candidate, fixed, mutation_rate):
    for i in range(9):
        if random.random() < mutation_rate:
            # Get indices of mutable positions in the row.
            mutable = [j for j in range(9) if not fixed[i][j]]
            if len(mutable) >= 2:
                a, b = random.sample(mutable, 2)
                candidate[i][a], candidate[i][b] = candidate[i][b], candidate[i][a]
    return candidate

def genetic_algorithm(grid, population_size=500, generations=1000, mutation_rate=0.05, display_callback=None):
    fixed = get_fixed_positions(grid)
    population = create_initial_population(grid, fixed, population_size)
    for gen in range(generations):
        fitnesses = [fitness(candidate) for candidate in population]
        best_fit = min(fitnesses)
        if best_fit == 0:
            best_candidate = population[fitnesses.index(best_fit)]
            print(f"Solution found at generation {gen}")
            return best_candidate
        if display_callback:
            best_candidate = population[fitnesses.index(best_fit)]
            display_callback(best_candidate)
        new_population = []
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child = crossover(parent1, parent2, fixed)
            child = mutate(child, fixed, mutation_rate)
            new_population.append(child)
        population = new_population
    print("No perfect solution found. Returning best candidate.")
    best_candidate = min(population, key=lambda candidate: fitness(candidate))
    return best_candidate

if __name__ == '__main__':
    # Example sudoku grid (0 = empty).
    grid = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7],
    ]
    solution = genetic_algorithm(grid)
    print("Solved grid:")
    for row in solution:
        print(row)
