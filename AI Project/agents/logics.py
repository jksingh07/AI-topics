
import random
import numpy as np

from utils import *


best_turn = {('N', 'E'): 'move_East',
             ('N', 'S'): 'move_East',
             ('N', 'W'): 'move_West',
             ('E', 'S'): 'move_East',
             ('E', 'W'): 'move_East',
             ('E', 'N'): 'move_West',
             ('S', 'W'): 'move_East',
             ('S', 'N'): 'move_East',
             ('S', 'E'): 'move_West',
             ('W', 'N'): 'move_East',
             ('W', 'E'): 'move_East',
             ('W', 'S'): 'move_West'}


class find_agent_loc:

    def __init__(self, size, obstacles, percept_wrong, move_wrong):
        self.size = size
        self.obstacles = obstacles
        # list of right position
        self.locations = list({*locations(self.size)}.difference(self.obstacles))
        # from a location to its index in the list, a dictionary
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}

        self.previous_move = None

        self.directions = {'N': [(0, 1), (1, 0), (0, -1), (-1, 0)],
                           'E': [(1, 0), (0, -1), (-1, 0), (0, 1)],
                           'S': [(0, -1), (-1, 0), (0, 1), (1, 0)],
                           'W': [(-1, 0), (0, 1), (1, 0), (0, -1)]}

        # move_North neighbour for each direction (N, E, S, W)
        self.front_locs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Factor of transition for each place.
        self.T = np.zeros((len(self.locations)*len(self.directions), len(self.locations)*len(self.directions)),
                          float)
        # Fill diagonal with initial likelihood that robot is present and facing this way.
        np.fill_diagonal(self.T, 1)

        # probability of a robot performing a certain activity correctly and incorrectly
        self.passed_move = 1-move_wrong
        self.failed_move = move_wrong

        # For each location's sensor factor. There are four potential directions for each place.
        self.sensor = np.ones((len(self.locations), len(self.directions)), float)

        # probabilities of the sensor's returned true and false values
        self.sensor_correct = 1-percept_wrong
        self.sensor_false = percept_wrong
        self.sensor_bump = 1

        # uniform posterior over valid locations and directions
        possible_location = 1.0/(len(self.locations)*len(self.directions))
        self.P = possible_location * np.ones((len(self.locations) * len(self.directions), 1), np.float)

    def __call__(self, percept):

        
        print(f"\n\n\nPrevious move: {self.previous_move}")
        print(f"Current percept: {percept}")
        self.update_sensor_value(percept)
        self.update_transition_value()
        self.update_posterior()
        action = self.heuristic(percept)

        return action

    def heuristic(self, percept):
        """
        Returns an action that pushes the robot against a wall and into a corner, providing more details about the likelihood of the position.
        Robotic movement becomes random once we have 85% confidence in its location, and it stops attempting to explore its surroundings.
        """

        # find index of most probable location and direction
        index_loc_dir = np.argmax(self.P[:, 0])
        
        # calculate index of location
        location_index = int(np.floor(index_loc_dir/len(self.directions)))
        
        # calculate index of direction
        direction_index = int(index_loc_dir % len(self.directions))
        orientations = ['N', 'E', 'S', 'W']

        print(f" Location : {self.locations[location_index]}")
        print(f"Probability of robot being in the current location: {round(self.P[index_loc_dir, 0], 3)}")

        action = 'move_North'

        # Robot movement should be planned so that it can explore the world if we are unsure of its whereabouts.
        if self.P[index_loc_dir, 0] < 0.85:
            if percept is not None:
                if 'North' in percept:
                    # Turn right if there is a wall in front and to the west.
                    if 'West' in percept and 'East' not in percept:
                        action = 'move_East'
                    # Turn west if there is a wall in front and to the right.
                    elif 'West' not in percept and 'East' in percept:
                        action = 'move_West'
                        
                    # Turn west or right to compel the robot to move while touching the wall if there is only a wall in front.
                    else:
                        action = np.random.choice(['move_West', 'move_East'], 1, p=[0.5, 0.5])
                        
                # make robot move while it is in contact with a wall
                elif 'East' in percept or 'West' in percept:
                    action = 'move_North'
                # Turn right or west to contact the wall if there is a wall in our rear.
                else:
                    action = np.random.choice(['move_West', 'move_East'], 1, p=[0.5, 0.5])
                    
            # Force the robot to move North if there are no perceptions.
            else:
                #print("NO PERCEPTS")
                action = 'move_North'
        # heuristic when we are sure where robot is. Some random moves
        else:
            #print("JUST MOVE")
            # Let's turn if there is a wall up ahead.
            if 'North' in percept:
                if 'West' in percept and 'East' not in percept:
                    action = 'move_East'
                elif 'West' not in percept and 'East' in percept:
                    action = 'move_West'
                else:
                    action = np.random.choice(['move_West', 'move_East'], 1, p=[0.5, 0.5])
            else:
                
                action = np.random.choice(['move_North', 'move_West', 'move_East'], 1, p=[0.95, 0.025, 0.025])

        self.previous_move = action

        return action


    def update_sensor_value(self, percept):
        """
        This feature refreshes the sensor factor for all potential directions and locations in this area.
        determines how many percepts in each direction and location are accurate. We must take into account the possibility of sensor error.

        For instance, if we are in position (loc[0], loc[1]) and are considering EAST direction and FORWARD percept,
        we must determine if there is a wall in (loc[0]+1, loc[1]), as FORWARD in this context denotes EAST.

        We must determine whether there is a wall in (loc[0], loc[1]+1) if, for instance, we are in location (loc[0], loc[1]) and
        are considering SOUTH direction and move South percept. This is because move South, in this context, means NORTH.
        """

        # reset sensor factor before updating it
        self.sensor[self.sensor > 0] = 1

        for location_index, loc in enumerate(self.locations):  # loop over each location

            for direction_index, neighbour in enumerate(self.directions.values()):  # loop over each direction
                # for current considered direction check if there's wall in percept direction.

                if 'North' in percept:
                    if (loc[0] + neighbour[0][0], loc[1] + neighbour[0][1]) not in self.locations:
                        if 'bump' in percept:
                            # if bump was detected, that means that this sensor reading was 100% correct
                            self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_bump
                        else:
                            # if percept was correct (Sensor detected wall in this direction and it is there)
                            self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_correct
                    else:
                        # if percept was NOT correct (Sensor detected wall in this direction, but it is NOT there)
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_false
                else:
                    if (loc[0] + neighbour[0][0], loc[1] + neighbour[0][1]) not in self.locations:
                        if 'bump' in percept:
                            # if bump was detected and sensor returned nothing in forward direction that means that this
                            # sensor reading is 100% false
                            self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * 0
                        else:
                            # if lack of percept in this direction was NOT correct
                            # (Sensor didn't detect wall in this direction, but the wall is there)
                            self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_false
                    else:
                        # if lack of percept in this direction was correct
                        # (Sensor didn't detect wall in this direction and the wall is NOT there)
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_correct

                if 'East' in percept:
                    if (loc[0] + neighbour[1][0], loc[1] + neighbour[1][1]) not in self.locations:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_correct
                    else:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_false
                else:
                    if (loc[0] + neighbour[1][0], loc[1] + neighbour[1][1]) not in self.locations:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_false
                    else:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_correct

                if 'South' in percept:
                    if (loc[0] + neighbour[2][0], loc[1] + neighbour[2][1]) not in self.locations:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_correct
                    else:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_false
                else:
                    if (loc[0] + neighbour[2][0], loc[1] + neighbour[2][1]) not in self.locations:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_false
                    else:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_correct

                if 'West' in percept:
                    if (loc[0] + neighbour[3][0], loc[1] + neighbour[3][1]) not in self.locations:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_correct
                    else:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_false
                else:
                    if (loc[0] + neighbour[3][0], loc[1] + neighbour[3][1]) not in self.locations:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_false
                    else:
                        self.sensor[location_index, direction_index] = self.sensor[location_index, direction_index] * self.sensor_correct

    def update_transition_value(self):
        """
        Using the previous action, updates the transition factor.
        If the robot pivoted, it would remain in place while changing its course. For instance, if the robot was facing North and
        its previous move was to turn right, it would now be facing East. This means that, given a minor chance that the robot failed to
        complete its previous activity, we must "pass" probability in each position from NORTH to EAST.
        And this is true for every direction and place (turning right requires turning east to south, turning west requires turning east to north, etc.).

        Robot would shift position and direction if moving forward. For instance, if the robot was at position (5, 9) and its last action was forward,
        we would need to determine whether a wall exists in each of the following directions: [5, 10] -> N, [6, 9] -> E, [5, 8] -> S, and [4, 9] -> W.
        We would then update the transition factor to account for this information and the slight possibility that the robot failed its last move.
        """

        # Robot remained in place but changed course if prior action was to turn right.
        if self.previous_move == 'move_East':
            # Set the entire Transition Factor to 0 before filling the diagonal with 1.
            self.T[self.T > 0] = 0
            np.fill_diagonal(self.T, 1)

            for location_index, loc in enumerate(self.locations):
                location_index_N = location_index * len(self.directions)  # index of direction- NORTH

                for direction_index, dirs in enumerate(self.directions):
                    # calculate index for all directions
                    location_index_D = location_index_N + direction_index  

                    # calculate the right direction's index in relation to the previous direction.
                    new_dir_idx_T = location_index_D + 1

                    # direction change from west to north
                    if new_dir_idx_T > location_index_N + 3:
                        new_dir_idx_T = location_index_N

                    # set the new direction and last direction values.
                    self.T[location_index_D, new_dir_idx_T] = self.passed_move
                    self.T[location_index_D, location_index_D] = self.failed_move

        # Robot remained in place but changed course if prior action was to turn west.
        elif self.previous_move == 'move_West':
            # Set the entire Transition Factor to 0 before filling the diagonal with 1.
            self.T[self.T > 0] = 0
            np.fill_diagonal(self.T, 1)

            for location_index, loc in enumerate(self.locations):
                location_index_N = location_index * len(self.directions)  # index of direction- NORTH

                for direction_index, dirs in enumerate(self.directions):

                    # calculate index for all directions
                    location_index_D = location_index_N + direction_index  

                    # compare the index for the west direction to the previous direction.
                    new_dir_idx_T = location_index_D - 1

                    # direction change from north to east
                    if new_dir_idx_T < location_index_N:
                        new_dir_idx_T = location_index_N + 3

                    # set the new direction and last direction values
                    self.T[location_index_D, new_dir_idx_T] = self.passed_move
                    self.T[location_index_D, location_index_D] = self.failed_move

        # Otherwise, the robot moved to a new position and saved its direction if the previous operation had been forward
        else:
            for location_index, loc in enumerate(self.locations):
                for direction_index, neighbour in enumerate(self.front_locs):
                    new_loc = (loc[0] + neighbour[0], loc[1] + neighbour[1])

                    # calculate the position index and direction in the T matrix.
                    location_index_D = location_index * len(self.directions) + direction_index  

                    if new_loc in self.locations:
                        new_loc_idx = self.loc_to_idx[new_loc] * len(self.directions) + direction_index
                        self.T[location_index_D, :] = 0  

                        # probability that the robot remained where it was even though moving forward was its last action
                        self.T[location_index_D, location_index_D] = self.failed_move
                        
                        # probability that the robot relocated
                        self.T[location_index_D, new_loc_idx] = self.passed_move
                    else:
                        # If the wall is in the advancing direction, the robot has remained in the last position.
                        self.T[location_index_D, :] = 0
                        self.T[location_index_D, location_index_D] = 1

    def update_posterior(self):
        """
        Updates the directions and locations for each location in this area. based on sensor data and robot transitions.
        """
        # sensor array to fit the geometry of the transition array
        sensor_reshaped = self.sensor.reshape([len(self.locations)*len(self.directions), 1])
        
        # transpose transition factor
        self.T = self.T.transpose()
        
        # update posterior
        self.P = sensor_reshaped * self.T.dot(self.P)
        
        # normalize posterior so its sum = 1
        self.P = self.P / self.P.sum(axis=0, keepdims=1)

    def get_posterior(self):
        """
        gives back the posterior of each place and the directions therein in array form.
        """
    
        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)

        for location_index, loc in enumerate(self.locations):
            # calculating the location index in the north
            location_index_N = location_index*len(self.directions)
            # get odds for all directions near your current position.
            P_arr[loc[0], loc[1], :] = self.P[location_index_N:location_index_N + 4, 0]
        return P_arr

    def move_North(self, current_location, current_direction):
        if current_direction == 'N':
            ret_loc = (current_location[0], current_location[1] + 1)
        elif current_direction == 'E':
            ret_loc = (current_location[0] + 1, current_location[1])
        elif current_direction == 'W':
            ret_loc = (current_location[0] - 1, current_location[1])
        elif current_direction == 'S':
            ret_loc = (current_location[0], current_location[1] - 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, current_direction

    def move_South(self, current_location, current_direction):
        if current_direction == 'N':
            ret_loc = (current_location[0], current_location[1] - 1)
        elif current_direction == 'E':
            ret_loc = (current_location[0] - 1, current_location[1])
        elif current_direction == 'W':
            ret_loc = (current_location[0] + 1, current_location[1])
        elif current_direction == 'S':
            ret_loc = (current_location[0], current_location[1] + 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, current_direction

    @staticmethod
    def move_East(current_location, current_direction):
        directions_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (directions_index[current_direction] + 1) % 4
        return current_location, dirs[idx]

    @staticmethod
    def move_West(current_location, current_direction):
        directions_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (directions_index[current_direction] + 4 - 1) % 4
        return current_location, dirs[idx]
