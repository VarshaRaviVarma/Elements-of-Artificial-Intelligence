# Simple quintris program! v0.2
# D. Crandall, Sept 2021

# [Aman Chaudhary amanchau  Himanshu Himanshu hhimansh  Varsha Ravi Verma varavi]

## References :

#https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
#https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.68.9918&rep=rep1&type=pdf
#https://towardsdatascience.com/beating-the-world-record-in-tetris-gb-with-genetics-algorithm-6c0b2f5ace9b
#https://www.youtube.com/watch?v=ptUXxWumxfE

import math
from AnimatedQuintris import *
from SimpleQuintris import *
from QuintrisGame import *
from kbinput import *
import time, sys
import copy

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#

class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    #Constructor with the initial values of weights for the heursitic function
    def __init__(self, a = -0.969955173666867, b = -0.001305578454103146, d = -0.2412493759106313, h = -0.013274451954305507, s = -0.028421542706573436) -> None:
        self.a = a
        self.b = b
        self.d = d
        self.h = h
        self.s = s
        self.area_height = 25
        self.area_width = 15

    #Defining a function that calculates and returns the height value of each column    
    def get_col_height(self,area):
        #Defining a list to store the heights of each column
        col_heights = []
        #Converting the board the 2D
        area = [[c for c in a] for a in area]
        #Loop to traverse through the area
        #Traversing through the row
        for i in range(15):
            count1=0 #To keep count of how many 'x' is in the column
            count2=0 #To keep count of how many ' ' is in the column
            #Traversing through the column
            for j in range(25):
                #Checking if the element is the peak of the column height
                if area[j][i] == 'x' and count1 == 0:
                    count1+=1
                    #Appending the column height to the list
                    col_heights.append(self.area_height - j)
                elif area[j][i]==' ':
                    count2+=1
            #Checking if the column is empty
            if count2==self.area_height:
                #Appending height value as '0' if the column is empty
                col_heights.append(0) 
        #Returning the list of column heights           
        return col_heights

    #Defining a function to compute the bumpiness of the board
    def get_bumpiness(self, quintris):
        bumpiness_value = 0
        #Assigning the board as 'area'
        area = quintris.get_board()
        #Assigning the column heights list as 'col_heights'
        col_heights = self.get_col_height(area)
        #Computing the sum of absolute height difference between the columns
        for i in range(len(col_heights)-1):
            bumpiness_value += abs(col_heights[i + 1] - col_heights[i])
        #Returning the bumpiness value of the board
        return bumpiness_value

    def get_deepest_well(self, quintris):
        #Wells is a list that holds the difference in values between the column heights
        wells = []
        #Assigning the board as 'area'
        area = quintris.get_board()
        #Assigning the column heights list as 'col_heights'
        col_heights = self.get_col_height(area)
        #Loop to compute the difference between the column heights and append it to 'wells' list
        for i in range(len(col_heights)):
            #For the first row
            if i == 0:
                well = col_heights[1] - col_heights[0]
                well = well if well > 0 else 0
                wells.append(well)
            #For the last row
            elif i == len(col_heights) - 1:
                well = col_heights[-2] - col_heights[-1]
                well = well if well > 0 else 0
                wells.append(well)
            #For all other rows
            else:
                well1 = col_heights[i - 1] - col_heights[i]
                well2 = col_heights[i + 1] - col_heights[i]
                well1 = well1 if well1 > 0 else 0
                well2 = well2 if well2 > 0 else 0
                well = well1 if well1 >= well2 else well2
                wells.append(well)
        #Computing the deepest well among all the well values in the list
        deepest_well_value = max(wells)
        #Returning the deepest well value
        return deepest_well_value

    #Function to calculate the number of holes
    def get_holes(self, quintris):
        #Called the get_board function on the quintris
        area = quintris.get_board()
        count = 0
        #Converting the board the 2D
        area = [[c for c in a] for a in area]
        for i in range(self.area_width):
            #Assigning the block to false
            block = False
            for j in range(self.area_height):
                #If 'x' is encountered
                if(area[j][i] == 'x'):
                    #Updating block to true
                    block = True
                    #If 'x' is not encountered and block is true
                elif(area[j][i] != 'x' and block):
                    #Increasing the count by 1
                    count += 1
        #Return count
        return count

    #Function to assign the weights for the heuristic
    def weights(self,quintris):
        #Calling the get bumpiness function on the quintris
        bump = self.get_bumpiness(quintris)
        #Calling the get deepest well function on the quintris
        deep_well = self.get_deepest_well(quintris)
        #Calling the get hole function on the quintris
        hole = self.get_holes(quintris)
        #Calling the get board function for complete lines on the board
        board = quintris.get_board()
        #Calling the col height function on the quintris
        heights = self.get_col_height(board)

        #Aggregating the heights by calculating the sum
        agg_height = sum(heights)
        #Storing the 1st index and storing it in score
        score = quintris.state[1]

        #Calculating the heuristic value
        h_value = self.a*(agg_height) + self.b*(bump) + self.d*(deep_well) + self.h*(hole) + self.s*(score)

        #Returning the heuristic value
        return h_value 
    
    #Function to get the best move
    def best_move(self, quintris):
        #Assigning the best score to 0
        best_score = 0

        #Initializing empty lists
        seq = []
        best_seq = []
        seq_flip = []

        #Rotating the piece 3 times 
        try:
            for rotate in range(4):
                seq = []
                #Creating a deepcopy of the quintris
                temp_quintris = copy.deepcopy(quintris)

                for i in range (rotate):
                    #Rotating the temp quintris
                    temp_quintris.rotate()
                    #Appending 'n' to the seq list
                    seq.append('n')

                for i in range(2):
                    #Creating a deepcopy of the temp quintris
                    temp_temp_quintris = copy.deepcopy(temp_quintris)
                    #Creating a deepcopy of the seq
                    seq_flip = copy.deepcopy(seq)

                    while(True):
                        #Extracting the column using the get piece function
                        col = temp_temp_quintris.get_piece()[2]
                        #Moving to the left
                        temp_temp_quintris.left()
                        #Extracting the column using the get piece function
                        new_col = temp_temp_quintris.get_piece()[2]
                        #If col is equal to the new col then break 
                        if(col == new_col):
                            break
                        #Else append 'b'
                        seq.append('b')
                        if(temp_temp_quintris.get_piece()[2] == 0):
                            break
                    for i in range(25):
                        #Creating a deepcopy of the temp temp quintris
                        temp_temp_temp_quintris = copy.deepcopy(temp_temp_quintris)
                        #Calling the down function on the temp temp temp quintris
                        temp_temp_temp_quintris.down()

                        #Initializing the score to 0
                        score = 0
                        #Calling the weights function on the temp temp temp quintris and storing the result in the score
                        score = self.weights(temp_temp_temp_quintris)

                        #Conditional check to check if the score is greater than the best score or the best score is equal to 0
                        if (score > best_score or best_score == 0):
                            best_score = score
                            #Creating a deep copy of the seq 
                            best_seq = copy.deepcopy(seq)
                        
                        #Calling the right function on the temp temp quintris
                        temp_temp_quintris.right()

                        #Conditional check if len(seq)-1 of seq is 'b' and length of seq is not 0
                        if(len(seq) != 0  and seq[len(seq)-1] == 'b'):
                            #Pop from seq
                            seq.pop()
                        else:
                            #Append to seq
                            seq.append('m')
                    
                    #Assigning seq_flip to seq
                    seq = seq_flip
                    #Appending 'h' to seq
                    seq.append('h')
                    #Calling the hflip function on the temp quintris.
                    temp_quintris.hflip()
        except:
            pass
        
        #Returning the best sequence
        return  best_seq

    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        #return random.choice("mnbh") * random.randint(1, 10)

        #Returning the best move on quintris
        return self.best_move(quintris)
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



