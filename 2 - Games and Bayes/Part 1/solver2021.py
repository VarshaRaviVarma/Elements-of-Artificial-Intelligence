#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Code by: [Aman Chaudhary(amanchau), Himanshu Bansal(hhimansh), Varsha Ravi Verma(varavi)]
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import copy

ROWS=5
COLS=5

# Method for printing the board
def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]
    
    
# Returning a list of possible successor states
def successors(state):
    
    # Taking an empty list for storing successor states
    successor_states = []
    
    # Making temp array for next successor states
    temp_state = [[0]*5 for x in range(5)]

    # Calculation for different Movements
    # Right Movements
    # Runnung a loop in range of 5 for each row
    for i in range(5):

        # Creating a empty row
        new_state = [[] for x in range(5)]

        # appending each element by shifting one to right
        for j in range (5):
            if(j>0):
                new_state[i].append(state[i][j-1])
            else:
                new_state[i].append(state[i][4])

            for k in range(5):
                if(k!=i):
                    new_state[k].append(state[k][j])

        # Appending new stae to successor state list as a tuple containing new board, move and cost associated with it
        successor_states.append((new_state, "R" + str(i+1), 5))

    #Left Movements
    # Runnung a loop in range of 5 for each row
    for i in range(5):

        # Creating a empty row
        new_state = [[] for x in range(5)]

        # appending each element by shifting one to left
        for j in range (5):
            if(j<4):
                new_state[i].append(state[i][j+1])
            else:
                new_state[i].append(state[i][0])

            for k in range(5):
                if(k!=i):
                    new_state[k].append(state[k][j])

        # Appending new stae to successor state list as a tuple containing new board, move and cost associated with it
        successor_states.append((new_state, "L" + str(i+1), 5))

    #Down Movements
    # Runnung a loop in range of 5 for each column
    for i in range(5):

        # Making deep copy of empty nested list
        new_state = copy.deepcopy(temp_state)

        # Swapping a particular column data keeping rest same
        for j in range (5):
            for k in range(5):
                if(i==k):
                    new_state[j][k] = state[(j-1)%5][k]
                else:
                    new_state[j][k] = state[j][k]

        # Appending new stae to successor state list as a tuple containing new board, move and cost associated with it
        successor_states.append((new_state, "D" + str(i+1)))          

    #Up Moments
    # Runnung a loop in range of 5 for each column
    for i in range(5):

        # Making deep copy of empty nested list
        new_state = copy.deepcopy(temp_state)

        # Swapping a particular column data keeping rest same
        for j in range (5):
            for k in range(5):
                if(i==k):
                    new_state[j][k] = state[(j+1)%5][k]
                else:
                    new_state[j][k] = state[j][k]

        # Appending new stae to successor state list as a tuple containing new board, move and cost associated with it
        successor_states.append((new_state, "U" + str(i+1)))

    # Outer clockwise Movement
    # Making deep copy of empty nested list
    new_state = copy.deepcopy(temp_state)

    # Running each row and column and if element is on outer ring i.e. its first or last row or first or last column 
    # we are swapping data with data to exact anticlockwise location on outer ring
    for i in range(5):
        for j in range(5):
            if(i==0 and j>0):
                new_state[i][j] = state[i][j-1]
            elif(i==4 and j<4):
                new_state[i][j] = state[i][j+1]
            elif(j==0 and i<4):    
                for k in range(5):
                    if(i==k):
                        new_state[i][j] = state[(i+1)%5][j]
            elif(j==4 and i>0):
                for k in range(5):
                    if(i==k):
                        new_state[i][j] = state[(i-1)%5][j]
            else:
                new_state[i][j] = state[i][j]

    # Appending new state to succesor state list
    successor_states.append((new_state, "Oc"))

    # Outer counter clockwise Movement
    # Making deep copy of empty nested list
    new_state = copy.deepcopy(temp_state)

    # Running each row and column and if element is on outer ring i.e. its first or last row or first or last column 
    # we are swapping data with data to exact clockwise location on outer ring
    for i in range(5):
        for j in range(5):
            if(i==0 and j<4):
                new_state[i][j] = state[i][j+1]
            elif(i==4 and j>0):
                new_state[i][j] = state[i][j-1]
            elif(j==0 and i>0):    
                for k in range(5):
                    if(i==k):
                        new_state[i][j] = state[(i-1)%5][j]
            elif(j==4 and i<4):
                for k in range(5):
                    if(i==k):
                        new_state[i][j] = state[(i+1)%5][j]
            else:
                new_state[i][j] = state[i][j]

    # Appending new state to succesor state list
    successor_states.append((new_state, "Occ"))

    # Inner clockwise Movement
    # Making deep copy of empty nested list
    new_state = copy.deepcopy(temp_state)

    # Running each row and column and if element is on inner ring i.e. its first or last row or first or last column 
    # we are swapping data with data to exact anticlockwise location on inner ring
    for i in range(5):
        for j in range(5):
            if(i==1 and j>1 and j<4):
                new_state[i][j] = state[i][j-1]
            elif(i==3 and j>0 and j<3):
                new_state[i][j] = state[i][j+1]
            elif(j==1 and i>0 and i<3):    
                for k in range(5):
                    if(i==k):
                        new_state[i][j] = state[(i+1)%5][j]
            elif(j==3 and i>1 and i<4):
                for k in range(5):
                    if(i==k):
                        new_state[i][j] = state[(i-1)%5][j]
            else:
                new_state[i][j] = state[i][j]

    # Appending new state to succesor state list
    successor_states.append((new_state, "Ic"))

    #Inner counter clockwise Movement
    # Making deep copy of empty nested list
    new_state = copy.deepcopy(temp_state)

    # Running each row and column and if element is on inner ring i.e. its first or last row or first or last column 
    # we are swapping data with data to exact clockwise location on inner ring
    for i in range(5):
        for j in range(5):
            if(i==1 and j>0 and j<3):
                new_state[i][j] = state[i][j+1]
            elif(i==3 and j>1 and j<4):
                new_state[i][j] = state[i][j-1]
            elif(j==1 and i>1 and i<4):    
                for k in range(5):
                    if(i==k):
                        new_state[i][j] = state[(i-1)%5][j]
            elif(j==3 and i>0 and i<3):
                for k in range(5):
                    if(i==k):
                        new_state[i][j] = state[(i+1)%5][j]
            else:
                new_state[i][j] = state[i][j]

    # Appending new state to succesor state list
    successor_states.append((new_state, "Icc"))
    
    # Returning all succesor states
    return successor_states



# check if we've reached the goal if yes returning true otherwise false
def is_goal(state):
    goal_state = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
    if(state == goal_state):
        return True
    return False

# Function is for finding the heuristic cost
def heuristic(current_state):

    # Calculating mahattan but in keeping in mind the condition the first cell can directly go to 
    # last cell of row and vice verca and same for columns
    manhattan_distance = 0
    goal_state = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]    
    
    # Iterating through each number from 1 to 25
    for i in range(1, 26):

        # taking current distance as 0
        distance = 0

        # taking out position of i in current state
        x = [x for x in current_state if i in x][0]
        curr_list_coordinates = (current_state.index(x), x.index(i))

        # taking out position of i in goal state
        x = [x for x in goal_state if i in x][0]
        goal_state_coordinates = (goal_state.index(x), x.index(i))

        # calculating x_distance and y_stance
        x_distance = abs(goal_state_coordinates[0] - curr_list_coordinates[0])
        y_distance = abs(goal_state_coordinates[1] - curr_list_coordinates[1]) 

        # if distance of any axis is greate than 2 i.e. 3 or 4 we subtract it from 5 to get distance
        if x_distance > 2:
            x_distance = 5 - x_distance
        if y_distance > 2:
            y_distance = 5 - y_distance

        # calculating distance and adding it to total manhaatan distance
        distance = x_distance + y_distance
        manhattan_distance += distance

    # Returning manhattan distance/5 because in a move atleast 5 tile get displaced
    return manhattan_distance/5
    
def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not ≥÷≥ any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    # Converting tuple to list
    temp_list = []
    for i in range(25):
        temp_list.append(initial_board[i])
    
    # Converting list to nested list to make board
    i=0
    state_list = []
    while i<len(temp_list):
        state_list.append(temp_list[i:i+5])
        i+=5
    
    # setting initial board as nested list
    initial_board = state_list

    # Calculating the total cost for initial board f(s) being the total cost f(s) = c(s) + h(s) here c(s) is 0
    cost = heuristic(initial_board)
    
    # Implementing fringe in form of priority queue using dictionary of python (Setting cost as key and a list(all the states with same cost) of tupples(current board, cost to reach there, steps to reach there) as value)
    fringe = {cost :[(initial_board, 0, [])]}
    
    # Taking a list of all visted states
    visited = [initial_board]

    # Iterating through Fringe till find a solution or Fringe is empty (No Solution Case)
    while fringe:

        # Making list of all priorities(costs) using dictionary keys method which give list of all keys
        priorties = fringe.keys()

        # Use min method on list of priorities (cost) to find min priority (cost)
        min_priority = min(priorties)
        
        # Retrieving the list of min priority (cost) boards
        min_priority_states = fringe.pop(min_priority)

        # Taking first element from min priority (cost) boards list
        (current_board, current_moves, move_list) = min_priority_states[0]
        
        # Slicing the min priority(cost) boards list
        min_priority_states = min_priority_states[1:]

        # Checking if length of min priority list is not zero and if not zero setting it back to dictionary
        if len(min_priority_states) != 0:
            fringe[min_priority] = min_priority_states
        
        # Calling succesors function to get all the possible moves with current board (returning new board, move to do it and cost to do it)
        for move in successors(current_board):
            
            # Checking if board is already traversed if yes then skipping it
            if move[0] in visited:
                continue

            # appending the board into visited board list
            visited.append(move[0])

            # Checking checking if board is goal state and if it is returning the move list
            if is_goal(move[0]):
                move_list.append(move[1])
                return move_list
            
            # Calculating total cost by adding heuristic cost and cost to reach that state
            cost = current_moves + 1 + heuristic(move[0])

            # Appending the move to movie_list
            move_list.append(move[1])

            # checking if cost is in the fringe if its there we are appending it to fringe and if not we are adding it 
            if cost in fringe:
                fringe[cost].append((move[0], current_moves + 1, move_list))
            else:
                fringe[cost] = [(move[0], current_moves + 1, move_list)]
            move_list = move_list[0:len(move_list)-1]
                
# Please don't modify anything below this line
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))