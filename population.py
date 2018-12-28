from bird import *
import random

X = 80


class Population:
    birds: list

    def __init__(self, size):
        self.birds = []

        for i in range(size):
            self.birds.append(Bird(X, 400))

    def on_draw(self):
        for bird in self.birds:
            bird.on_draw()

    def on_update(self, dt, pipes):
        dead_count = 0

        for bird in self.birds:
            bird.on_update(dt, pipes)
            if bird.is_dead:
                dead_count += 1

        if dead_count >= len(self.birds):
            # Reset all birds
            for bird in self.birds:
                bird.reset()

            self.natural_selection()

    def pick_random(self):
        max_sum = sum([b.calculate_fitness() for b in self.birds])
        r = random.random() * max_sum
        running_sum = 0
        for b in self.birds:
            running_sum += b.calculate_fitness()
            if running_sum >= r:
                return b

        raise Exception('This shouldn\'t happen.')

    def natural_selection(self):
        s = sorted(self.birds, key=lambda b: b.calculate_fitness(), reverse=True)[
            0:round(len(self.birds)/2)]

        parent_pairs = []
        new_birds = []
        parent_pairs.append([s[0], s[0]])

        for i in range(len(s)-1):
            parent_pairs.append([
                s[i],
                s[i+1]
            ])

        for i in range(len(self.birds) - len(parent_pairs)):
            # Fill in the rest of the spots with randomly chosen birds
            new_birds.append(self.pick_random())

        for parent_pair in parent_pairs:
            new_birds.append(parent_pair[0].crossover(parent_pair[1]))

        self.birds = new_birds
