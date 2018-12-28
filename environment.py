import arcade
from population import *
from pipe import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Environment(arcade.Window):
    population: Population
    pipes: list

    def __init__(self, population: Population, pipes: list):
        self.population = population
        self.pipes = pipes
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()
        self.population.on_draw()
        for pipe in self.pipes:
            pipe.on_draw()

    def on_update(self, dt):
        self.population.on_update(dt, self.pipes)

        for pipe in self.pipes:

            for bird in self.population.birds:
                bird.check_collision(pipe)

            if pipe.on_update(dt):
                pipe.randomize(SCREEN_HEIGHT)


if __name__ == '__main__':
    pipe = Pipe(500, 100)
    pipe.randomize(SCREEN_HEIGHT, SCREEN_WIDTH + 50)

    env = Environment(
        Population(10),
        [pipe]
    )

    arcade.run()
