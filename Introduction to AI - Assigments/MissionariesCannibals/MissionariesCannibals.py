

# Author: Jaskaran Singh Luthra (110090236)


# importing libraries
import pydot
import random
from collections import deque

#parent stores the parent of current node i.e (n_m, n_c, side)
#list_of nodes stores the state of current node
# action = (n_m, n_c, side) => no. of missionaries, no. of cannibals. postion of boat (left or right)

parent, action, list_of_nodes = dict(), dict(), dict()


class Missionaries_Cannibals():

    def __init__(self):
        
        self.start = (3, 3, 1)  # Start state is 3 missionaries, 3 cannibals, left side 
        self.goal = (0, 0, 0)   # Goal state is 0 missionaries, 0 cannibals, right side
        self.moves = [(1, 0), (0, 1), (1, 1), (0, 2), (2, 0)]  # Moves allowed for transfering to other side

        self.boat_position = ["right", "left"] # it represents the position of boat
        self.visited = {}   # this parameter will check if a state is visited
        self.solved = False  # to check if we reached the goal state
        self.graph = pydot.Dot(graph_type='graph', bgcolor="#fff3af", label="fig: Missionaries and Cannibal State Space Tree", fontcolor="red", fontsize="24") 

     
    def solve(self, solve_method="dfs"):
        self.visited = dict()
        parent[self.start] = None
        action[self.start] = None
        list_of_nodes[self.start] = None

        return self.dfs(*self.start, 0) if solve_method == "dfs" else self.bfs()


    # this function check for goal state
    def check_goal(self, n_m, n_c, side):
        return (n_m, n_c, side) == self.goal

    # this function check for goal state
    def check_start(self, n_m, n_c, side):
        return (n_m, n_c, side) == self.start

    # this function check constraint of no. of cannibals
    def cannibals_outnumbered(self, n_m, n_c):
        n_m_right = 3 - n_m
        
        n_c_right = 3 - n_c
        return (n_m > 0 and n_c > n_m) \
               or (n_m_right > 0 and n_c_right > n_m_right)

    # check constraint conditions for moving 
    def check_action(self, n_m, n_c):
        """
        Constraints check function
        """
        return (0 <= n_m <= 3) and (0 <= n_c <= 3)


    def solution(self):
        
        state = self.goal   # goal state
        route, steps, nodes = [] ,[], []  # route stores the path followed, steps stores the state

        while state is not None:
            route.append(state)  # store each state in the route
            steps.append(action[state])
            nodes.append(list_of_nodes[state])
        
            state = parent[state]
        
        steps, nodes = steps[::-1], nodes[::-1]

        n_m_left, n_c_left = 3, 3
        n_m_right, n_c_right = 0, 0
    
        
        print("\nSteps\n")
        for i, ((n_m, n_c, side), node) in enumerate(zip(steps[1:], nodes[1:])):
                   
            print(f"{i + 1}: ({n_m},{n_c}),{n_m} missionaries  and {n_c} cannibals moved from {self.boat_position[side]} to {self.boat_position[int(not side)]}.")

            op = -1 if side == 1 else 1
            
            n_m_left = n_m_left + op * n_m
            n_c_left = n_c_left + op * n_c

            n_m_right = n_m_right - op * n_m
            n_c_right = n_c_right - op * n_c
            
        print("Finished")
        print("*" * 60)

    def draw_edge(self, n_m, n_c, side, depth):
        a, b = None, None
        if parent[(n_m, n_c, side)] is not None:
            a = pydot.Node(str(parent[(n_m, n_c, side)] + (depth - 1, )), label=str(parent[((n_m, n_c, side))]))
            self.graph.add_node(a)

            b = pydot.Node(str((n_m, n_c, side, depth)), label=str((n_m, n_c, side)))
            self.graph.add_node(b)

            edge = pydot.Edge(str(parent[(n_m, n_c, side)] + (depth - 1, )), str((n_m, n_c, side, depth) ), dir='forward')
            self.graph.add_edge(edge)
        else:
            
            b = pydot.Node(str((n_m, n_c, side, depth)), label=str((n_m, n_c, side)))
            self.graph.add_node(b)        
        return a, b


# Implimentation using BFS approach
    def bfs(self):
        q = deque()  # Intialising queue
        q.append(self.start + (0, ))
        self.visited[self.start] = True

        # go from a to b where a is the parent[b] and b = (n_m, n_c, side, depth)
        while q:
            n_m, n_c, side, depth = q.popleft()
            
            a, b = self.draw_edge(n_m, n_c, side, depth)    

            
            op = -1 if side == 1 else 1

            can_expand = False

            for x, y in self.moves:
                next_m, next_c, next_s = n_m + op * x, n_c + op * y, int(not side)

                if (next_m, next_c, next_s) not in self.visited:
                    
                    if self.check_action(next_m, next_c):
                        can_expand = True
                        self.visited[(next_m, next_c, next_s)] = True
                        q.append((next_m, next_c, next_s, depth + 1))
                        
                        # Keep track of parent and corresponding action
                        parent[(next_m, next_c, next_s)] = (n_m, n_c, side)
                        action[(next_m, next_c, next_s)] = (x, y, side)
                        list_of_nodes[(next_m, next_c, next_s)] = b
                
            if not can_expand:
                pass
        return False

    def dfs(self, n_m, n_c, side, depth):
        self.visited[(n_m, n_c, side)] = True

        a, b = self.draw_edge(n_m, n_c, side, depth)    

        
        if self.check_start(n_m, n_c, side):
            pass
        elif self.check_goal(n_m, n_c, side):
            return True
        elif self.cannibals_outnumbered(n_m, n_c):
            return False
        else:
            pass

        solution_found = False
        operation = -1 if side == 1 else 1
        
        can_expand = False

        for x, y in self.moves:
            next_m, next_c, next_s = n_m + operation * x, n_c + operation * y, int(not side)

            if (next_m, next_c, next_s) not in self.visited:
                if self.check_action(next_m, next_c):
                    can_expand = True
                    # Keep track of parent state and corresponding action
                    parent[(next_m, next_c, next_s)] = (n_m, n_c, side)
                    action[(next_m, next_c, next_s)] = (x, y, side)
                    list_of_nodes[(next_m, next_c, next_s)] = b

                    solution_found = (solution_found or self.dfs(next_m, next_c, next_s, depth + 1))
                
                    if solution_found:
                        return True


        self.solved = solution_found
        return solution_found

