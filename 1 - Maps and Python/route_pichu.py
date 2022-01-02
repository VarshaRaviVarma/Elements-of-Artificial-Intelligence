#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [NAME - Varsha Ravi Varma AND USERNAME - varavi]
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

def path(curr_move, row, col):
        if((curr_move[0] - row) < 0):
                return 'D'
        elif((curr_move[0] - row) > 0):
                return 'U'
        elif((curr_move[1] - col) < 0):
                return 'R'
        elif((curr_move[1] - col) > 0):
                return 'L'


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0,'')]
        #creating a visiting set to keep track of the visited path
        visited = set()

        while fringe:
                (curr_move, curr_dist, move_string)=fringe.pop(0)
                #adding the current move to the visited set
                visited.add(curr_move)
                for move in moves(house_map, *curr_move):
                        if house_map[move[0]][move[1]]=="@":
                                move_string+=path(curr_move,move[0],move[1])
                                move_count = curr_dist + 1
                                #returning the output
                                return (move_count, move_string)
                        else:
                                if house_map[move[0]][move[1]] not in visited:
                                        new_move_string = move_string + path(curr_move,move[0],move[1])
                                        fringe.append((move, curr_dist + 1, new_move_string))

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

