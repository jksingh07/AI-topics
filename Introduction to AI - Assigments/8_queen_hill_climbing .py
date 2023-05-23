#Author: Jaskaran Singh Luthra (110090236)


# Importng libraries
import math
import random

class create_state:
    
    global h_value # global variable for h value 
    
    
# Constructor 
    def __init__(self, length, value=None):
        self.h = -1    
        self.length = length
        self.value = value   


# duplicate function uses to create the copy of the data of the board. 
    def duplicate(self,previous_state):
        duplicate_board=[]
        
        for i in previous_state:
            replica_values=[]
            for j in i:
                replica_values.append(j)
            duplicate_board.append(replica_values)
        return duplicate_board
        
# create_first is used to intialise the board with Q and _ All values are inserted randomly
    def create_first(self):
        board=[]
        for i in range(int(self.length)):
            columns_info=[None]*int(self.length)
            random_digit = random.randint(0,int(self.length)-1)
            for j in range(int(self.length)):
                if j == random_digit:
                    columns_info[j]='Q'
                else:
                    columns_info[j]='_'
            board.append(columns_info)
        self.value = board
        
        return self.value
    
 #calculate_h_value is used to calculate the heuristic value of the Q when we make moves   
    def calculate_h_value(self):
        counter=0
                    
        for i in range(len(self.value)):
            for j in range(len(self.value)):
                if self.value[i][j]=='Q':
                    position = [None]*2
                    position[0]=i
                    position[1]=j
                    pos_one, pos_two = self.search_attack_position(position)

                    for k in range(len(self.value)):
                        for l in range(len(self.value)):
                                if self.value[k][l]=='Q':
                                    for m in pos_one:
                                        if m[0] == k and m[1] == l:
                                            counter+=1
                                    for m in pos_two:
                                        if m[0] == k and m[1] == l:
                                            counter+=1
        return math.ceil(counter/2)
        
    

# create_next use to create the next move on board using the current position 
    def create_next(self, previous_position, current_position):
        p = current_position[0]
        q = current_position[1]
        
        previous_p = previous_position[0]
        previous_q = previous_position[1]
        
        next_position = self.duplicate(self.value)
        
        for i in range(0, len(next_position)):
            for j in range(0, len(next_position)):
                if i==p and j==q:
                    next_position[i][j]='Q'

                if i==previous_p and j==previous_q:
                    next_position[i][j]='_'
        return next_position
    


# search_attack_position is used to find the position to attack.
    def search_attack_position(self,location): 
        vertical_stack_pos = []                             
        loc_0 = location[0]
        loc_1=location[1]
        
        if loc_0==0:
            while(loc_0 < len(self.value)-1):
                vertical_attacking_loc=[None]*2
                loc_0+=1

                vertical_attacking_loc[0]=loc_0
                vertical_attacking_loc[1]=loc_1
                vertical_stack_pos.append(vertical_attacking_loc)
        
        elif loc_0==len(self.value):
            while(loc_0>=0):
                vertical_attacking_loc=[None]*2
                loc_0-=1

                vertical_attacking_loc[0]=loc_0
                vertical_attacking_loc[1]=loc_1
                vertical_stack_pos.append(vertical_attacking_loc)
        
        else:
            while(loc_0 < len(self.value)-1):
                vertical_attacking_loc=[None]*2
                loc_0+=1

                vertical_attacking_loc[0]=loc_0
                vertical_attacking_loc[1]=loc_1
                vertical_stack_pos.append(vertical_attacking_loc)
                
            loc_0=location[0]
            loc_1=location[1]
                
            while(loc_0>=0):
                vertical_attacking_loc=[None]*2
                loc_0-=1

                vertical_attacking_loc[0]=loc_0
                vertical_attacking_loc[1]=loc_1
                vertical_stack_pos.append(vertical_attacking_loc)
                
        diagonal_stack_list = []                         
        loc_0=location[0]
        loc_1=location[1]  
        #Checking upper left squares
        while loc_0>0 and loc_0<len(self.value) and loc_1>0 and loc_1<len(self.value):
            diagonal_attacking_loc=[None]*2
            loc_0-=1
            loc_1-=1

            diagonal_attacking_loc[0]=loc_0
            diagonal_attacking_loc[1]=loc_1
            diagonal_stack_list.append(diagonal_attacking_loc)
            
        loc_0=location[0]
        loc_1=location[1]
        
        #Checking lower left squares
        while loc_0>=0 and loc_0<len(self.value)-1 and loc_1>0 and loc_1<len(self.value):
            diagonal_attacking_loc=[None]*2
            loc_0+=1
            loc_1-=1

            diagonal_attacking_loc[0]=loc_0
            diagonal_attacking_loc[1]=loc_1
            diagonal_stack_list.append(diagonal_attacking_loc)
            
        loc_0=location[0]
        loc_1=location[1]
        
        #Checking upper right squares
        while loc_0>0 and loc_0<len(self.value) and loc_1>=0 and loc_1<len(self.value)-1:
            diagonal_attacking_loc=[None]*2
            loc_0-=1
            loc_1+=1

            diagonal_attacking_loc[0]=loc_0
            diagonal_attacking_loc[1]=loc_1
            diagonal_stack_list.append(diagonal_attacking_loc)
        
        loc_0=location[0]
        loc_1=location[1]
        
        #Checking lower right squares
        while loc_0>=0 and loc_0<len(self.value)-1 and loc_1>=0 and loc_1<len(self.value)-1:
            diagonal_attacking_loc=[None]*2
            loc_0+=1
            loc_1+=1

            diagonal_attacking_loc[0]=loc_0
            diagonal_attacking_loc[1]=loc_1
            diagonal_stack_list.append(diagonal_attacking_loc) 
        
        return vertical_stack_pos, diagonal_stack_list
    
class board_game:

    global n, output  # n = number of queens, output = boolean value 
    output=False
    
    def __init__(self):
        self.win = 0        # for successful move
        self.lost = 0       # for failure
        self.moves = 0      # no. of steps
        self.win_moves = 0  # total successful moves
        self.lost_moves = 0 # total fail moves
        self.c = 0          # counter

#   search_row_position is used to find the position of queen on board.
    def search_row_position(self,value,row_num):    
        for j in range(len(value)):
            if value[row_num][j] == 'Q':
                position = [None]*2
                position[0]= row_num
                position[1]= j     
                break
        return position
    

    def main(self):
        global n_queens     # number of queens

        print("Enter the no. of queens")

        n_queens = input()

        print("Enter the no. of iterations")
        #print("How many runs?")
        iterations = input()

        # Hill Climbing search
        print("\nHill-Climbing search:")
        for x in range(int(iterations)):
            self.moves = 0
            self.hill_climbing_search(x)
        print("\nResults\n")
        
        print("Solving " + str(n_queens) + "-Queens problem using Hill Climbing Search")
        print("No. of Iterations: ", str(iterations))
        print("Rate of Success: ", 100*(self.win/int(iterations)),"%")
        print("Rate of Failure: ", 100*(self.lost/int(iterations)), "%")
        print("Success: Average number of moves are: ", self.win_moves/self.win)
        print("Failure: Average number of moves are: ", self.lost_moves/self.lost)
        print()

#       Hill-climbing search with sideways move. 
        self.win = 0
        self.lost = 0
        self.moves = 0
        self.win_moves = 0
        self.lost_moves = 0
 
        for x in range(int(iterations)):
            self.moves = 0        
            self.hill_climbing_search_sideways(x)
        
        print("\n\nSIDEWAYS MOVE\n")
        print("Solving " + str(n_queens) + "-Queens problem using Hill Climbing Search with SIDEWAYS move")
        print("No. of Iterations: ", str(iterations))
  
        print("Rate of Success: ", 100*(self.win/int(iterations)),"%")
        print("Rate of Failure: ", 100*(self.lost/int(iterations)), "%")
        print("Success: Average number of moves are: ", self.win_moves/self.win)
        print("Failure: Average number of moves are: ", self.lost_moves/self.lost)
        print()
        
#       Random-restart without Sideways move.
        print("\n\nRANDOM RESTART\n")
        
        self.moves = 0
        self.c = 0
        for x in range(int(iterations)):
            y=self.moves
            self.random_restart(0)
        print("WITHOUT SIDEWAYS")
        print("Solving " + str(n_queens) + "-Queens problem using Random-Restart Hill-Climbing search WITHOUT SIDEWAYS move ")
        print("No. of Iterations: ", str(iterations))
##        print("Rate of Success: ", 100*(self.win/int(iterations)),"%")
##        print("Rate of Failure: ", 100*(self.lost/int(iterations)), "%")
        print("Average number of random-restarts without sideways move: ", self.c/int(iterations))
        print("Average number of steps required without sideways move: ", self.moves/int(iterations))
        print()

#       Random-restart with Sideways move.
        
        self.moves = 0
        self.c = 0
        for x in range(int(iterations)):
            self.random_restart(1)
        print("\nWITH SIDEWAYS\n")
        print("Solving " + str(n_queens) + "-Queens problem using Random-Restart Hill-Climbing search WITH SIDEWAYS move ")
##        print("Rate of Success: ", 100*(self.win/int(iterations)),"%")
##        print("Rate of Failure: ", 100*(self.lost/int(iterations)), "%")
        print("Average number of random-restarts: ", self.c/int(iterations))
        print("Average number of steps required: ", self.moves/int(iterations))
        print()

#   Hill-Climbing search.     
    def hill_climbing_search(self, n_calls):
        h_value=-1
        
        original_board = create_state(n_queens)
        original_board.value = original_board.create_first()
        original_board.h = original_board.calculate_h_value()
        if output:
            if n_calls < 4:
                print("Search Sequence " + str(n_calls+1) + ":")
                print("Initial state:")
                for x in original_board.value:
                    for y in x:
                        print(y, end=" ")
                    print()
                print("h value:", original_board.h)
                print()

        min_h_board_value = original_board.value
        while h_value !=0:
            location_min_h = []
            prev_board = create_state(n_queens, min_h_board_value)
            prev_board.h = prev_board.calculate_h_value()
            h_value = prev_board.h
            for i in range(int(n_queens)):
                position = self.search_row_position(prev_board.value,i)
                for j in range(int(n_queens)):
                    current_position = [None]*2
                    current_position[0]=i
                    current_position[1]=j
                    if current_position == position:
                        continue    

                    board_ahead = create_state(n_queens)
                    board_ahead.value = prev_board.create_next(position, current_position)
                    board_ahead.h = board_ahead.calculate_h_value()

                    if board_ahead.h <= h_value:
                        h_value = board_ahead.h
                        save_position =current_position
                        save_position.append(board_ahead.h)
                        location_min_h.append(save_position)
                        
            if location_min_h:            
                l = len(location_min_h)-1
                while l>=0:
                    y = location_min_h[l]
                    if y[2] != h_value:
                        del location_min_h[l]
                    l-=1

                random_digit = random.randint(0,len(location_min_h)-1)
                dash_position = location_min_h[random_digit]
                del dash_position[2]
                parent_position = self.search_row_position(prev_board.value,dash_position[0])
                min_h_board_value = prev_board.create_next(parent_position, dash_position)

            if h_value == prev_board.h:
                if h_value == 0:
                    if n_calls < 4:
                        if output:
                            print("Solution found.")
                    self.win +=1
                else:
                    self.lost_moves +=self.moves
                    if output:
                        if n_calls < 4:
                            for x in min_h_board_value:
                                for y in x:
                                    print(y, end=" ")

                                print()
                            print("h value: " + str(h_value))
                            print()
                            print("Solution not found.")
                            print()
                    self.lost +=1
                break

            else:
                self.moves +=1
                if output:
                    if n_calls < 4:
                        print("Next state:")
                        for x in min_h_board_value:
                            for y in x:
                                print(y, end=" ")

                            print()
                        print("h value:", h_value)
                        print()

                if h_value==0:
                    self.win_moves += self.moves
                    if output:
                        if n_calls < 4:
                            print("Solution found.")
                            print()
                    self.win += 1


    def hill_climbing_search_sideways(self, n_calls):
        n_tries = 0
        h_value=-1
        
        original_board = create_state(n_queens)
        original_board.value = original_board.create_first()
        original_board.h = original_board.calculate_h_value()
        if output:
            if n_calls < 4:
                print("Search: Iteration " + str(n_calls+1) + ":")
                print("First state:")
                for x in original_board.value:
                    for y in x:
                        print(y, end=" ")
                    print()
                print("h value:", original_board.h)
                print()

        min_h_board_value = original_board.value
        while h_value !=0:
            location_min_h = []
            self.moves +=1
            high_h = 0 
            prev_board = create_state(n_queens, min_h_board_value)
            prev_board.h = prev_board.calculate_h_value()
            h_value = prev_board.h
            for i in range(int(n_queens)):
                loc = self.search_row_position(prev_board.value,i)
                for j in range(int(n_queens)):
                    current_position = [None]*2
                    current_position[0]=i
                    current_position[1]=j
                    if current_position == loc:
                        continue    

                    board_ahead = create_state(n_queens)
                    board_ahead.value = prev_board.create_next(loc, current_position)
                    board_ahead.h = board_ahead.calculate_h_value()

                    if board_ahead.h <= h_value:
                        h_value = board_ahead.h
                        save_position =current_position
                        high_h = 1
                        if board_ahead.h < h_value:
                            n_tries = 0
                        save_position.append(board_ahead.h)
                        location_min_h.append(save_position)
                        
            if location_min_h:            
                l = len(location_min_h)-1
                while l>=0:
                    y = location_min_h[l]
                    if y[2] != h_value:
                        del location_min_h[l]
                    l-=1

                random_digit = random.randint(0,len(location_min_h)-1)
                dash_position = location_min_h[random_digit]
                del dash_position[2]
                parent_position = self.search_row_position(prev_board.value,dash_position[0])
                min_h_board_value = prev_board.create_next(parent_position, dash_position)
            
            if h_value == prev_board.h:                
                if h_value == 0:
                    if output:
                        if n_calls < 4:
                            print("Congrats!!!, Solution found successfully.")
                            print()
                    self.win_moves += self.moves
                    self.win +=1                
                else:
                    if high_h != 0:
                        n_tries +=1
                        if output:
                            if n_calls < 4:
                                print("Next state:")
                                for x in min_h_board_value:
                                    for y in x:
                                        print(y, end=" ")

                                    print()
                                print("h value:", h_value)
                                print()                        
                    else:
                        self.lost_moves +=self.moves
                        self.lost +=1
                        if output:
                            if n_calls < 4:
                                print("Sorry, Solution not found.")
                                print()
                        break
                    if n_tries >=100:
                        self.lost_moves +=self.moves
                        self.lost +=1
                        if output:
                            if n_calls < 4:
                                for x in min_h_board_value:
                                    for y in x:
                                        print(y, end=" ")
                                    print()
                                print("h value:", h_value)
                                print()
                                
                                print("After 100 Iterations: Sorry, Solution not found")
                                print()
                        break
            else:
                if output:
                    if n_calls < 4:
                        print("Next state:")
                        for x in min_h_board_value:
                            for y in x:
                                print(y, end=" ")

                            print()
                        print("h value:", h_value)
                        print()

                if h_value==0:
                    self.win_moves += self.moves
                    if output:
                        if n_calls < 4:
                            print("Congrats!!!, Solution found successfully.")
                            print()
                    self.win += 1


    def random_restart(self, hill_climb_sideways):
        n_tries=0
        h_value=-1
        
        while h_value != 0:
            self.c +=1
            original_board = create_state(n_queens)
            original_board.value = original_board.create_first()
            original_board.h = original_board.calculate_h_value()
            
            if original_board.h == 0:
                self.win +=1
                break

            min_h_board_value = original_board.value
            while h_value !=0:
                location_min_h = []
                high_h = 0
                prev_board = create_state(n_queens, min_h_board_value)
                prev_board.h = prev_board.calculate_h_value()
                h_value = prev_board.h
                for i in range(int(n_queens)):
                    position = self.search_row_position(prev_board.value,i)
                    for j in range(int(n_queens)):
                        current_position = [None]*2
                        current_position[0]=i
                        current_position[1]=j
                        if current_position == position:
                            continue    

                        board_ahead = create_state(n_queens)
                        board_ahead.value = prev_board.create_next(position, current_position)
                        board_ahead.h = board_ahead.calculate_h_value()

                        if board_ahead.h <= h_value:
                            if board_ahead.h < h_value:
                                n_tries = 0
                            h_value = board_ahead.h
                            save_position =current_position                            
                            save_position.append(board_ahead.h)
                            location_min_h.append(save_position)
                            high_h = 1     
                
                if h_value == 0 or high_h == 0: 
                    if h_value == 0:
                        self.moves+=1
                        self.win_moves += self.moves
                        self.win +=1

                    if high_h == 0:
                        self.lost_moves +=self.moves
                        self.lost +=1
                    break

                if location_min_h:            
                    l = len(location_min_h)-1
                    while l>=0:
                        y = location_min_h[l]
                        if y[2] != h_value:
                            del location_min_h[l]
                        l-=1
                    random_digit = random.randint(0,len(location_min_h)-1)
                    dash_position = location_min_h[random_digit]
                    del dash_position[2]
                    parent_position = self.search_row_position(prev_board.value,dash_position[0])
                    min_h_board_value = prev_board.create_next(parent_position, dash_position)

                if h_value == prev_board.h:
                    if hill_climb_sideways == 0:
                        break

                    if hill_climb_sideways == 1:
                        self.moves+=1
                        if high_h != 0:
                            n_tries +=1
                        if n_tries >=100:
                            break
                else:
                    self.moves+=1                        


start = board_game()
start.main()
