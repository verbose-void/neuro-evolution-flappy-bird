import arcade
import random
from pipe import *
import numpy as np
import math

GRAVITY = 0.1
SPEED = 10

NET_DIMS = (3, 2, 1)


class Bird:
    start_pos: tuple
    pos: list
    y_vel: list
    radius = 10
    is_dead = False
    alive_length: float = 0

    vision: list
    net_outputs: list

    layer_weights: np.ndarray

    def __init__(self, x: float, y: float, nn=None):
        if nn != None:
            self.layer_weights = nn
        else:
            self.randomize_net()

        self.start_pos = (x, y)
        self.reset()

    def calculate_fitness(self):
        return self.alive_length

    def reset(self):
        self.pos = list(self.start_pos)
        self.is_dead = False
        self.y_vel = 0
        self.alive_length = 0
        self.vision = []
        self.net_outputs = []

    def randomize_net(self):
        self.layer_weights = []

        for i in range(len(NET_DIMS)-1):
            self.layer_weights.append(
                np.random.uniform(
                    size=(NET_DIMS[i], NET_DIMS[i+1])
                )
            )

    def clone(self):
        out = Bird(self.start_pos[0], self.start_pos[1],
                   np.copy(self.layer_weights))
        return out

    def crossover(self, other: 'Bird'):
        child_layer_weights = []

        parentA_layer: np.ndarray
        for i, parentA_layer in enumerate(self.layer_weights):
            parentB_layer = other.layer_weights[i]
            rows = len(parentA_layer)
            cols = len(parentA_layer[0])

            cutoff = (
                np.random.randint(0, high=rows),
                np.random.randint(0, high=cols)
            )

            child_layer = np.zeros((rows, cols))

            for i in range(rows):
                for j in range(cols):

                    # This will copy all nodes from parent 1 until the cutoff is reached,
                    # then it will switch over to parent 2.

                    if i < cutoff[0] or (i == cutoff[0] and j <= cutoff[1]):
                        child_layer[i, j] = parentA_layer[i, j]
                    else:
                        child_layer[i, j] = parentB_layer[i, j]

            child_layer_weights.append(child_layer)

        return Bird(self.start_pos[0], self.start_pos[1], child_layer_weights)

    def activate_layer(self, layer):
        for x in np.nditer(layer, op_flags=['readwrite']):
            # Sigmoid activation
            x[...] = 1/(1+np.exp(-x))

    def look(self, pipe: Pipe):
        # Get distance from the pipe's X
        x_dist = pipe.pos[0] - self.pos[0]
        if x_dist < 0:
            x_dist = 0

        # Get distance from pipe's upper bound
        y_upper_dist = (pipe.pos[1] + HALF_GAP) - self.pos[1]

        # Get distance from pipe's lower bound
        y_lower_dist = (pipe.pos[1] - HALF_GAP) - self.pos[1]

        self.vision = [
            x_dist,
            y_upper_dist,
            y_lower_dist
        ]

    def think(self):
        # Calculate the network's output.

        # Column matrix
        # inputs = np.reshape(inputs, (len(inputs), 1))
        output = self.vision

        l = len(self.layer_weights)-1
        for i, weight_layer in enumerate(self.layer_weights):
            output = np.matmul(output, weight_layer)

            if i != l:
                self.activate_layer(output)

        self.net_outputs = output

    def act(self):
        if self.net_outputs[0] > 0.5:
            self.jump()

    def on_update(self, dt, pipes):
        if self.is_dead:
            return

        self.look(pipes[0])
        self.think()
        self.act()

        self.alive_length += 0.2

        self.y_vel -= GRAVITY

        if self.y_vel < -1:
            self.y_vel = -1

        self.pos[1] += self.y_vel * SPEED

        if self.pos[1] - self.radius <= 0:
            self.pos[1] = self.radius

        elif self.pos[1] + self.radius >= 600:
            self.pos[1] = 600 - self.radius

    def kill(self):
        self.is_dead = True

    def on_draw(self):
        if self.is_dead:
            return

        arcade.draw_circle_filled(
            self.pos[0], self.pos[1], self.radius,
            arcade.color.WHITE
        )

    def check_collision(self, pipe: Pipe):
        px = pipe.pos[0]
        py = pipe.pos[1]
        bx = self.pos[0]
        by = self.pos[1]

        b_right = bx + self.radius
        p_left = px - THICKNESS / 2
        p_right = px + THICKNESS / 2

        b_top = by + self.radius
        b_bottom = by - self.radius

        # If X is inside pipe
        if b_right >= p_left and b_right <= p_right:
            # If Y is outside of the gap
            if b_top >= py + HALF_GAP or b_bottom <= py - HALF_GAP:
                self.kill()

    def jump(self):
        if self.y_vel < 0:
            self.y_vel = 1
