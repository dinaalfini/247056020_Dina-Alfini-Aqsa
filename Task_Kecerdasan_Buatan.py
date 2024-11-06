import random

# Activity durations (in hours)
activity_durations = {
    'A': 2,
    'B': 3,
    'C': 2,
    'D': 4
}

# Maximum total duration allowed (in hours)
max_total_duration = 8

# Constraint functions
def is_valid_schedule(schedule):
    """
    Check if a given schedule satisfies all constraints.
    """
    # A must be scheduled before B
    if schedule['A'] >= schedule['B']:
        return False

    # C and D cannot overlap
    if not (schedule['C'] + activity_durations['C'] <= schedule['D'] or
            schedule['D'] + activity_durations['D'] <= schedule['C']):
        return False

    # Total duration cannot exceed maximum allowed time
    if max(schedule.values()) + max(activity_durations.values()) > max_total_duration:
        return False

    return True

# Fitness function
def fitness(schedule):
    """
    Calculate fitness score of a schedule, rewarding valid schedules.
    Higher fitness indicates better alignment with constraints.
    """
    fitness_score = 0

    # Check each constraint
    if schedule['A'] < schedule['B']:
        fitness_score += 1  # A before B
    if schedule['C'] + activity_durations['C'] <= schedule['D'] or schedule['D'] + activity_durations['D'] <= schedule['C']:
        fitness_score += 1  # C and D do not overlap
    if max(schedule.values()) + max(activity_durations.values()) <= max_total_duration:
        fitness_score += 1  # Total duration constraint satisfied

    return fitness_score

# GA Functions
def create_individual():
    """
    Generate a random schedule.
    """
    return {activity: random.randint(0, max_total_duration - duration) for activity, duration in activity_durations.items()}

def crossover(parent1, parent2):
    """
    Perform crossover to create a child schedule from two parents.
    """
    child = {}
    for activity in activity_durations:
        # Randomly inherit start time from one of the parents
        child[activity] = parent1[activity] if random.random() < 0.5 else parent2[activity]
    return child

def mutate(individual):
    """
    Mutate a schedule by adjusting the start time of one activity.
    """
    activity = random.choice(list(activity_durations.keys()))
    individual[activity] = random.randint(0, max_total_duration - activity_durations[activity])

# Genetic Algorithm
def genetic_algorithm(population_size=10, generations=50):
    # Initial population
    population = [create_individual() for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate fitness for each individual and sort by fitness
        population = sorted(population, key=lambda ind: fitness(ind), reverse=True)

        # Display best solution in this generation
        best_individual = population[0]
        print(f"Generation {generation}: Best fitness = {fitness(best_individual)} | Schedule = {best_individual}")

        # Stop if we find an optimal schedule
        if fitness(best_individual) == 3:
            print("Optimal schedule found!")
            break

        # Select top individuals for reproduction
        next_generation = population[:population_size // 2]

        # Generate new individuals through crossover and mutation
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(next_generation, 2)
            child = crossover(parent1, parent2)
            if random.random() < 0.1:  # Mutation chance of 10%
                mutate(child)
            next_generation.append(child)

        population = next_generation

    # Return the best schedule found
    return best_individual

# Execute the genetic algorithm
best_schedule = genetic_algorithm()
print("Best schedule found:", best_schedule)
