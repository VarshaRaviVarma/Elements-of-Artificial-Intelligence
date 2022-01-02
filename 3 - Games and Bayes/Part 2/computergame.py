### SAME FUNCTIONS AS QUINTRIS.PY ###

### CREATED A NEW FILE TO RUN THE GENETIC ALGORITHM ###

import math
from AnimatedQuintris import *
from SimpleQuintris import *
from QuintrisGame import *
from kbinput import *
import copy

class ComputerPlayer:

    def __init__(self, a = -0.6792700054683791, b = -0.18606668535646453, d = -0.5966087168440437, h = -0.21000854571967414, s = 0.3223753991573457) -> None:
        self.a = a
        self.b = b
        self.d = d
        self.h = h
        self.s = s

        self.area_height = 25
        self.area_width = 15
        
    def get_col_height(self,area):
        col_heights = []
        area = [[c for c in a] for a in area]
        for i in range(15):
            count1=0
            count2=0
            for j in range(25):
                if area[j][i] == 'x' and count1 == 0:
                    count1+=1
                    col_heights.append(self.area_height - j)
                elif area[j][i]==' ':
                    count2+=1
            if count2==self.area_height:
                col_heights.append(0)            
        return col_heights

    def get_bumpiness(self, quintris):
        bumpiness_value = 0
        area = quintris.get_board()
        col_heights = self.get_col_height(area)
        for i in range(len(col_heights)-1):
            bumpiness_value += abs(col_heights[i + 1] - col_heights[i])
        return bumpiness_value

    def get_deepest_well(self, quintris):
        wells = []
        area = quintris.get_board()
        col_heights = self.get_col_height(area)
        for i in range(len(col_heights)):
            if i == 0:
                well = col_heights[1] - col_heights[0]
                well = well if well > 0 else 0
                wells.append(well)
            elif i == len(col_heights) - 1:
                well = col_heights[-2] - col_heights[-1]
                well = well if well > 0 else 0
                wells.append(well)
            else:
                well1 = col_heights[i - 1] - col_heights[i]
                well2 = col_heights[i + 1] - col_heights[i]
                well1 = well1 if well1 > 0 else 0
                well2 = well2 if well2 > 0 else 0
                well = well1 if well1 >= well2 else well2
                wells.append(well)
        deepest_well_value = max(wells)
        return deepest_well_value

    def get_holes(self, quintris):
        area = quintris.get_board()
        count = 0
        area = [[c for c in a] for a in area]
        for i in range(self.area_width):
            block = False
            for j in range(self.area_height):
                if(area[j][i] == 'x'):
                    block = True
                elif(area[j][i] != 'x' and block):
                    count += 1
        return count

    def weights(self,quintris):
        bump = self.get_bumpiness(quintris)
        deep_well = self.get_deepest_well(quintris)
        hole = self.get_holes(quintris)
        board = quintris.get_board()
        heights = self.get_col_height(board)

        agg_height = sum(heights)
        score = quintris.state[1]

        h_value = self.a*(agg_height) + self.b*(bump) + self.d*(deep_well) + self.h*(hole) + self.s*(score)

        return h_value 
  
    def best_move(self, quintris):
        best_score = 0
        seq = []
        best_seq = []
        seq_flip = []
        
        for rotate in range(4):
            seq = []
            temp_quintris = copy.deepcopy(quintris)

            for i in range (rotate):
                temp_quintris.rotate()
                seq.append('n')

            for i in range(2):
                temp_temp_quintris = copy.deepcopy(temp_quintris)
                seq_flip = copy.deepcopy(seq)

                while(True):
                    col = temp_temp_quintris.get_piece()[2]
                    temp_temp_quintris.left()
                    new_col = temp_temp_quintris.get_piece()[2]
                    if(col == new_col):
                        break
                    seq.append('b')
                    if(temp_temp_quintris.get_piece()[2] == 0):
                        break

                for i in range(25):
                    temp_temp_temp_quintris = copy.deepcopy(temp_temp_quintris)
                    temp_temp_temp_quintris.down()

                    score = 0
                    score = self.weights(temp_temp_temp_quintris)

                    if (score > best_score or best_score == 0):
                        best_score = score
                        # best = 0
                        best_seq = copy.deepcopy(seq)
                    
                    temp_temp_quintris.right()
                    if(len(seq) != 0  and seq[len(seq)-1] == 'b'):
                        seq.pop()
                    else:
                        seq.append('m')
                
                seq = seq_flip
                seq.append('h')
                temp_quintris.hflip()

        return  best_seq

    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        return self.best_move(quintris)
        #return random.choice("mnbh") * random.randint(1, 10)