

import random
import numpy as np

from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

from utils import *

import agents


class Environment:
    actions = "move_West move_East move_North".split()

    def __init__(self, size, obstacles, percept_wrong, move_wrong):
        self.size = size
        self.obstacles = obstacles
        self.action_sensors = []
        self.locations = {*locations(self.size)}.difference(self.obstacles)
        self.percept_wrong = percept_wrong
        self.move_wrong = move_wrong
        self.reset()

    def reset(self):
        self.agentLoc = random.choice(list(self.locations))
        self.agentDir = random.choice(['N', 'E', 'S', 'W'])

    def get_percept(self):
        p = self.action_sensors
        self.action_sensors = []
        rel_dirs = {'North': 0, 'East': 1, 'South': 2, 'West': 3}
        for rel_dir, incr in rel_dirs.items():
            nh = next_location(self.agentLoc, next_move(self.agentDir, incr))
            prob = 0.0 + self.percept_wrong
            if (not valid_location(nh, self.size)) or nh in self.obstacles:
                prob = 1.0 - self.percept_wrong
            if random.random() < prob:
                p.append(rel_dir)

        return p

    def doAction(self, action):
        points = -1
        if action == "move_West":
            if random.random() < self.move_wrong:
                # there is a small risk that the agent won't turn
                print('Robot did not turn')
            else:
                self.agentDir = move_left(self.agentDir)
        elif action == "move_East":
            if random.random() < self.move_wrong:
                # tiny likelihood that the agent won't turn
                print('Robot did not turn')
            else:
                self.agentDir = move_right(self.agentDir)
        elif action == "move_North":
            if random.random() < self.move_wrong:
                # There is a small probability that the agent won't move.
                print('Robot did not move')
                loc = self.agentLoc
            else:
                # normal forward move
                loc = next_location(self.agentLoc, self.agentDir)
            if valid_location(loc, self.size) and loc not in self.obstacles:
                self.agentLoc = loc
            else:
                self.action_sensors.append("bump")
        return points  # cost/benefit of action

    def finished(self):
        return False

def main():
    random.seed()
    # pace of action execution
    rate = 1
    
    # likelihood that perception will be incorrect
    percept_wrong = 0.1
    
    # possibility that the agent will refuse to obey the command
    move_wrong = 0.05
    
    # the number of steps to be taken
    n_steps = 40
    
    # environment size
    env_size = 16
    
    # map of the surroundings: 0 is clear, 1 is a wall
    grid = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                    [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
                    [1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
                    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    
    # make a list of potential obstacles' locations.
    obstacles = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:
                obstacles.append((j, env_size - i - 1))

    
    env = Environment(env_size, obstacles, percept_wrong, move_wrong)
    
    agent = agents.logics.find_agent_loc(env.size, env.obstacles, percept_wrong, move_wrong)

    for t in range(n_steps):
        #print('step %d' % t)

        percept = env.get_percept()

        action = agent(percept)

        # learn what the agent thinks about the surroundings
        P = agent.get_posterior()


        env.doAction(action)

 

if __name__ == '__main__':
    main()
