# -*- coding: utf-8 -*-
import random


class Agent:
    """
    A class for simulating an agent
    """

    def __init__(self, environment, agents, y, x):
        # setting attributes
        if (x is None):
            self.x = random.randint(0, 100)
        else:
            self.x = x
        if (y is None):
            self.y = random.randint(0, 100)
        else:
            self.y = y
        self.environment = environment
        self.agents = agents
        self.store = 0

    def move(self):
        # move the agent randomly.
        if random.random() < 0.5:
            self.x = (self.x + 1) % 100
        else:
            self.x = (self.x - 1) % 100

        if random.random() < 0.5:
            self.y = (self.y + 1) % 100
        else:
            self.y = (self.y - 1) % 100

    def eat(self):
        # eat the grass
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10

    def share_with_neighbours(self, neighbourhood):
        # share with other neighbours
        for agent in self.agents:
            dist = self.distance_between(agent)
            if dist <= neighbourhood:
                sum = self.store + agent.store
                ave = sum / 2
                self.store = ave
                agent.store = ave

    def distance_between(self, agent):
        # compute the distance with other agent
        return (((self.x - agent.x) ** 2) + ((self.y - agent.y) ** 2)) ** 0.5
