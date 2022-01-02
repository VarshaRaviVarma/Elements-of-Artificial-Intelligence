#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
# [Aman Chaudhary amanchau  Himanshu Himanshu hhimansh  Varsha Ravi Verma varavi]
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import copy

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

# function to convert String to 2D board
def convert_board(board, N):

    # taking empty list
    board_matrix = []

    # Iterating number of rows
    for i in range(N):
        # Retrieving a row
        row = board[:N]
        
        # changing the board to remaing elements
        board = board[N:]

        # Appending each by dividing it to colums
        board_matrix.append([c for c in row])

    # returning the 2D matrix
    return board_matrix

# Method to get coordinates of black pieces by checking where b, B and $ is present
def get_black_pieces(board):
    return [(row_i,col_i) for col_i in range(len(board[0])) for row_i in range(len(board)) if board[row_i][col_i] in 'bB$']
 
# Method to get coordinates of white pieces by checking where w, W and @ is present
def get_white_pieces(board):
    return [(row_i,col_i) for col_i in range(len(board[0])) for row_i in range(len(board)) if board[row_i][col_i] in 'wW@']
 
# Method to calculate heuristic value of board
def get_utility_value(board, is_black):

    # get white and black pieces
    white_pieces = get_white_pieces(board)
    black_pieces = get_black_pieces(board)

    # if computer is black piece then calculating utility accordingly
    if is_black:
        return (len(black_pieces)-len(white_pieces)) * 500 + len(black_pieces) * 50
    else:
        return (len(white_pieces)-len(black_pieces)) * 500 + len(white_pieces) * 50

# method for calculating max level of alpha beta pruning tree
def max_value(board, alpha, beta, is_black, depthlevel):

    # if we reach the terminal state of board or depth level upto which we want to iterate returning utility value of state
    if isTerminal(board) or depthlevel == 0:
        return get_utility_value(board, is_black)
    
    # decreasing depth value by 1
    depthlevel -=1

    # Iterating through each successor board 
    for b in get_moves(board, is_black):

        # Calculating alpha values and comparing it with with beta value for pruning
        alpha = max(alpha, min_value(b, alpha, beta, not(is_black), depthlevel))
        if alpha >= beta:
            return alpha
    return alpha

# method for calculating min level of alpha beta pruning tree
def min_value(board, alpha, beta, is_black, depthlevel):

    # if we reach the terminal state of board or depth level upto which we want to iterate returning utility value of state
    if isTerminal(board) or depthlevel == 0:
        return get_utility_value(board, is_black)

    # decreasing depth value by 1
    depthlevel -=1

    # Iterating through each successor board
    for b in get_moves(board, is_black):

        # Calculating beta values and comparing it with with alpha value for pruning
        beta = min(beta, max_value(b, alpha, beta, not(is_black), depthlevel))
        if alpha >= beta:
            return beta
    return beta

# Calculating if we have reached the terminal state
def isTerminal(board):
    if len(get_black_pieces(board)) == 0 or len(get_white_pieces(board)) == 0:
        return True
    return False

# Method to get_moves for board  
def get_moves(board, is_black):

    # Allthe different moves direction on each piece depending on color of piece
    pichu_regular_dir = []
    pichu_capture_dir = []
    pikachu_regular_dir =[]
    pikachu_capture_dir =[]
    raichu_dir =[[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
    if is_black:
        pichu_regular_dir = [[-1, -1], [-1, 1]]
        pichu_capture_dir = [[-2, -2], [-2, 2]]
        pikachu_regular_dir = [[0, -1], [0, 1], [-1, 0], [0, -2], [0, 2], [-2, 0]]
        pikachu_capture_dir = [[0, -3], [0, 3], [-3, 0], [0, -2], [0, 2], [-2, 0]]
        
    else:
        pichu_regular_dir = [[1, -1], [1, 1]]
        pichu_capture_dir = [[2, -2], [2, 2]]
        pikachu_regular_dir = [[0, -1], [0, 1], [1, 0], [0, -2], [0, 2], [2, 0]]
        pikachu_capture_dir = [[0, -3], [0, 3], [3, 0], [0, -2], [0, 2], [2, 0]]
        
    # getting coordinates of black and white pieces
    black_pieces = get_black_pieces(board)
    white_pieces = get_white_pieces(board)

    # setting the turn of pieces
    turn_pieces = white_pieces
    if is_black:
        turn_pieces = black_pieces
    reg_valid_states = []
    cap_valid_states = []

    #Iterating through each piece
    for piece in turn_pieces: 

        # checking if turn is of black piece
        if is_black:

            # checking pieces is b
            if board[piece[0]][piece[1]] == 'b':

                # Doing the capture direction of pichus
                for capture_dir in pichu_capture_dir:

                    # Making deep copy of board
                    temp_board = copy.deepcopy(board)

                    # calculating new rol, new col, captured row and captured col
                    new_row = piece[0] + capture_dir[0]
                    new_col = piece[1] + capture_dir[1]
                    capture_row = piece[0] + capture_dir[0] // 2
                    capture_col = piece[1] + capture_dir[1] // 2

                    # checking codition for valid move
                    if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and temp_board[capture_row][capture_col] == "w":
                        temp_board[piece[0]][piece[1]] = '.'
                        temp_board[new_row][new_col] = 'b'
                        temp_board[capture_row][capture_col] = '.'
                        if new_row == 0:
                            temp_board[new_row][new_col] = '$'
                        cap_valid_states.append(temp_board)
                
                # Doing the regular move of pichu        
                for regular_dir in pichu_regular_dir:
                    temp_board = copy.deepcopy(board)
                    new_row = piece[0] + regular_dir[0]
                    new_col = piece[1] + regular_dir[1]
                    if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == ".":
                        temp_board[piece[0]][piece[1]] = '.'
                        temp_board[new_row][new_col] = 'b'
                        if new_row == 0:
                            temp_board[new_row][new_col] = '$'
                        reg_valid_states.append(temp_board)

            # checking if piece is black pikachu   
            if board[piece[0]][piece[1]] == 'B':
                
                # Iterating every capture move pikachu
                for capture_dir in pikachu_capture_dir:

                    # making deep copy of board and calculating new row
                    temp_board = copy.deepcopy(board)
                    new_row = piece[0] + capture_dir[0]
                    new_col = piece[1] + capture_dir[1]
                    capture_row = 0
                    capture_col = 0

                    # This is for capture move where pieces 2 cells
                    if abs(capture_dir[0]) == 2 or abs(capture_dir[1]) == 2: 

                        # calculating the coordinates of capture cell
                        capture_row = piece[0] + capture_dir[0] // 2
                        capture_col = piece[1] + capture_dir[1] // 2

                        # Checking condition for valid move and performing the move
                        if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and (temp_board[capture_row][capture_col] == "w" or temp_board[capture_row][capture_col] == "W"):
                            temp_board[piece[0]][piece[1]] = '.'
                            temp_board[new_row][new_col] = 'B'
                            temp_board[capture_row][capture_col] ='.'
                            if new_row == 0:
                                temp_board[new_row][new_col] = '$'
                            cap_valid_states.append(temp_board)
                    else:

                        # calculating the capture cell direction and its for 3 cell move
                        capture_row_dir = capture_dir[0]//3
                        capture_col_dir = capture_dir[1]//3

                        # checking if two cells are in range of board
                        if 0<= piece[0] + capture_row_dir<len(temp_board) and 0 <= piece[1] + capture_col_dir<len(temp_board[0]) and 0 <=piece[0] + capture_row_dir*2<len(temp_board) and 0 <= piece[1] + capture_col_dir*2<len(temp_board[0]):
                           
                            # Checking if both cells have have white piece
                            if temp_board[piece[0] + capture_row_dir][piece[1] + capture_col_dir] in 'wW@' and temp_board[piece[0] + capture_row_dir * 2][piece[1] + capture_col_dir * 2] in 'wW@':
                                continue
                           
                            # if next cell has white pichu and pikachu
                            if temp_board[piece[0] + capture_row_dir][piece[1] + capture_col_dir] in 'wW':

                                # Calculating the coordinated capture cells
                                capture_row = piece[0] + capture_row_dir
                                capture_col = piece[1] + capture_col_dir

                                # Checking if the cells between them is any black piece
                                found = False
                                if capture_row_dir == 0:
                                    for K in range(piece[1] + capture_col_dir, new_col):
                                        if temp_board[piece[0]][K] in 'bB$':
                                            found = True
                                if capture_col_dir == 0:
                                    for K in range(piece[0] + capture_row_dir, new_row):
                                        if temp_board[K][piece[1]] in 'bB$':
                                            found = True

                                # Checking if the move is valid
                                if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and (temp_board[capture_row][capture_col] == "w" or temp_board[capture_row][capture_col] == "W") and not found:
                                    temp_board[piece[0]][piece[1]] = '.'
                                    temp_board[new_row][new_col] = 'B'
                                    temp_board[capture_row][capture_col] ='.'
                                    if new_row == 0:
                                        temp_board[new_row][new_col] = '$'
                                    cap_valid_states.append(temp_board)
                            else:

                                # Calculating the coordinated capture cells
                                capture_row = piece[0] + capture_row_dir * 2
                                capture_col = piece[1] + capture_col_dir * 2

                                # Checking if the cells between them is any black piece
                                found = False
                                if capture_row_dir == 0:
                                    for K in range(piece[1] + capture_col_dir, new_col):
                                        if temp_board[piece[0]][K] in 'bB$':
                                            found = True
                                if capture_col_dir == 0:
                                    for K in range(piece[0] + capture_row_dir, new_row):
                                        if temp_board[K][piece[1]] in 'bB$':
                                            found = True

                                # Checking if the move is valid
                                if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and (temp_board[capture_row][capture_col] == "w" or temp_board[capture_row][capture_col] == "W") and not found:
                                    temp_board[piece[0]][piece[1]] = '.'
                                    temp_board[new_row][new_col] = 'B'
                                    temp_board[capture_row][capture_col] ='.'
                                    if new_row == 0:
                                        temp_board[new_row][new_col] = '$'
                                    cap_valid_states.append(temp_board)
                
                # Iterating every regular move of pikachu
                for regular_dir in pikachu_regular_dir:

                    # Making deep copy of board and calculating new row and col
                    temp_board = copy.deepcopy(board)
                    new_row = piece[0] + regular_dir[0]
                    new_col = piece[1] + regular_dir[1]
                    present_flag = True

                    # Checking valid moves
                    if abs(regular_dir[0]) != 1 or abs(regular_dir[1]) != 1:
                        if 0 <= piece[0] + regular_dir[0]//2 < len(board) and 0 <= piece[1] + regular_dir[1]//2 < len(board[0]) and temp_board[piece[0] + regular_dir[0]//2][piece[1] + regular_dir[1]//2] != ".":
                            present_flag = False
                    if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and present_flag:
                        temp_board[piece[0]][piece[1]] = '.'
                        temp_board[new_row][new_col] = 'B'
                        if new_row == 0:
                            temp_board[new_row][new_col] = '$'
                        reg_valid_states.append(temp_board)

            # checking if piece is black raichu   
            if board[piece[0]][piece[1]] == '$':

                # Iterate through every direction of raichu and checking for valid moves
                for raichu_move in raichu_dir:
                    not_captured = True
                    captured_loc =(-1, -1)
                    if raichu_move[0] == 0 and raichu_move[1] == 1:
                        col = piece[1]
                        while col < len(board[0]) - 1:
                            temp_board = copy.deepcopy(board)
                            if temp_board[piece[0]][col+1] == '.':
                                temp_board[piece[0]][col+1] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                col += 1
                            elif temp_board[piece[0]][col+1] in 'wW@' and col + 2< len(board[0]) and temp_board[piece[0]][col+2] == '.' and not_captured:
                                temp_board[piece[0]][col+2] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[piece[0]][col+1] = '.'
                                captured_loc = (piece[0], col + 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                col += 2
                            else:
                                break
                    elif raichu_move[0] == 0 and raichu_move[1] == -1:
                        col = piece[1]
                        while col > 0:
                            temp_board = copy.deepcopy(board)
                            if temp_board[piece[0]][col-1] == '.':
                                temp_board[piece[0]][col-1] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                col -= 1
                            elif temp_board[piece[0]][col-1] in 'wW@' and col - 2>=0 and temp_board[piece[0]][col-2] == '.' and not_captured:
                                temp_board[piece[0]][col-2] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[piece[0]][col-1] = '.'
                                captured_loc = (piece[0], col - 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                col -= 2
                            else:
                                break
                    elif raichu_move[1] == 0 and raichu_move[0] == 1:
                        row = piece[0]
                        while row < len(board) - 1:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row + 1][piece[1]] == '.':
                                temp_board[row + 1][piece[1]] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row += 1
                            elif temp_board[row + 1][piece[1]] in 'wW@' and row + 2< len(board) and temp_board[row + 2][piece[1]] == '.' and not_captured:
                                temp_board[row + 2][piece[1]] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row + 1][piece[1]] = '.'
                                captured_loc = (row + 1, piece[1])
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row += 2
                            else:
                                break
                    elif raichu_move[1] == 0 and raichu_move[0] == -1:
                        row = piece[0]
                        while row > 0:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row - 1][piece[1]] == '.':
                                temp_board[row - 1][piece[1]] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row -= 1
                            elif temp_board[row - 1][piece[1]] in 'wW@' and row - 2>= 0 and temp_board[row - 2][piece[1]] == '.' and not_captured:
                                temp_board[row - 2][piece[1]] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row - 1][piece[1]] = '.'
                                captured_loc = (row - 1, piece[1])
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row -= 2
                            else:
                                break
                    elif raichu_move[1] == 1 and raichu_move[0] == 1:
                        row = piece[0]
                        col = piece[1]
                        while row < len(board) - 1 and col < len(board[0]) - 1:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row + 1][col + 1] == '.':
                                temp_board[row + 1][col + 1] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row += 1
                                col += 1
                            elif temp_board[row + 1][col + 1] in 'wW@' and row + 2< len(board) and col + 2< len(board[0]) and temp_board[row + 2][col + 2] == '.' and not_captured:
                                temp_board[row + 2][col + 2] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row + 1][col + 1] = '.'
                                captured_loc =(row + 1, col + 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row += 2
                                col += 2
                            else:
                                break
                    elif raichu_move[1] == -1 and raichu_move[0] == -1:
                        row = piece[0]
                        col = piece[1]
                        while row > 0  and col > 0:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row - 1][col - 1] == '.':
                                temp_board[row - 1][col - 1] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row -= 1
                                col -= 1
                            elif temp_board[row - 1][col - 1] in 'wW@' and row - 2>=0 and col - 2>=0 and temp_board[row - 2][col - 2] == '.' and not_captured:
                                temp_board[row - 2][col - 2] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row - 1][col - 1] = '.'
                                captured_loc =(row - 1, col - 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row -= 2
                                col -= 2
                            else:
                                break
                    elif raichu_move[1] == 1 and raichu_move[0] == -1:
                        row = piece[0]
                        col = piece[1]
                        while row > 0 and col < len(board[0]) - 1:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row - 1][col + 1] == '.':
                                temp_board[row - 1][col + 1] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row -= 1
                                col += 1
                            elif temp_board[row - 1][col + 1] in 'wW@' and row - 2>=0 and col + 2< len(board[0]) and temp_board[row - 2][col + 2] == '.' and not_captured:
                                temp_board[row - 2][col + 2] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row - 1][col + 1] = '.'
                                captured_loc =(row - 1, col + 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row -= 2
                                col += 2
                            else:
                                break
                    elif raichu_move[1] == -1 and raichu_move[0] == 1:
                        row = piece[0]
                        col = piece[1]
                        while row < len(board) - 1 and col > 0:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row + 1][col - 1] == '.':
                                temp_board[row + 1][col - 1] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row += 1
                                col -= 1
                            elif temp_board[row + 1][col - 1] in 'wW@' and row + 2< len(board) and col - 2>=0 and temp_board[row + 2][col - 2] == '.' and not_captured:
                                temp_board[row + 2][col - 2] = '$'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row + 1][col - 1] = '.'
                                captured_loc =(row + 1, col - 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row += 2
                                col -= 2
                            else:
                                break
        else:
            # If piece is not black then its white and performing all the same thing that we have one with black piece i.e. moves
            if board[piece[0]][piece[1]] == 'w':
                for capture_dir in pichu_capture_dir:
                    temp_board = copy.deepcopy(board)
                    new_row = piece[0] + capture_dir[0]
                    new_col = piece[1] + capture_dir[1]
                    capture_row = piece[0] + (capture_dir[0] // 2)
                    capture_col = piece[1] + (capture_dir[1] // 2)
                    if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and temp_board[capture_row][capture_col] == "b":
                        temp_board[piece[0]][piece[1]] = '.'
                        temp_board[new_row][new_col] = 'w'
                        temp_board[capture_row][capture_col] = '.'
                        if new_row == len(temp_board) - 1:
                            temp_board[new_row][new_col] = '@'
                        cap_valid_states.append(temp_board)

                for regular_dir in pichu_regular_dir:
                    temp_board = copy.deepcopy(board)
                    new_row = piece[0] + regular_dir[0]
                    new_col = piece[1] + regular_dir[1]
                    if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == ".":
                        temp_board[piece[0]][piece[1]] = '.'
                        temp_board[new_row][new_col] = 'w'
                        if new_row == len(temp_board) - 1:
                            temp_board[new_row][new_col] = '@'
                        reg_valid_states.append(temp_board)
                
            if board[piece[0]][piece[1]] == 'W':
                
                for capture_dir in pikachu_capture_dir:
                    temp_board = copy.deepcopy(board)
                    new_row = piece[0] + capture_dir[0]
                    new_col = piece[1] + capture_dir[1]
                    capture_row = 0
                    capture_col = 0
                    if abs(capture_dir[0]) == 2 or abs(capture_dir[1]) == 2: 
                        capture_row = piece[0] + capture_dir[0] // 2
                        capture_col = piece[1] + capture_dir[1] // 2
                        if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and (temp_board[capture_row][capture_col] == "b" or temp_board[capture_row][capture_col] == "B"):
                            
                            temp_board[piece[0]][piece[1]] = '.'
                            temp_board[new_row][new_col] = 'W'
                            temp_board[capture_row][capture_col] ='.'
                            if new_row == len(board) - 1:
                                temp_board[new_row][new_col] = '@'
                            cap_valid_states.append(temp_board)
                    else:
                        
                        capture_row_dir = capture_dir[0]//3
                        capture_col_dir = capture_dir[1]//3
                        
                        if 0<piece[0] + capture_row_dir<len(temp_board) and 0< piece[1] + capture_col_dir<len(temp_board[0]) and 0<piece[0] + capture_row_dir*2<len(temp_board) and 0< piece[1] + capture_col_dir*2<len(temp_board[0]):
                            if temp_board[piece[0] + capture_row_dir][piece[1] + capture_col_dir] in 'bB$' and temp_board[piece[0] + capture_row_dir * 2][piece[1] + capture_col_dir * 2] in 'bB$':
                                continue
                            if temp_board[piece[0] + capture_row_dir][piece[1] + capture_col_dir] in 'bB':
                                capture_row = piece[0] + capture_row_dir
                                capture_col = piece[1] + capture_col_dir
                                found = False
                                if capture_row_dir == 0:
                                    for K in range(piece[1] + capture_col_dir, new_col):
                                        if temp_board[piece[0]][K] in 'wW@':
                                            found = True
                                if capture_col_dir == 0:
                                    for K in range(piece[0] + capture_row_dir, new_row):
                                        if temp_board[K][piece[1]] in 'wW@':
                                            found = True
                                if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and (temp_board[capture_row][capture_col] == "b" or temp_board[capture_row][capture_col] == "B") and not found:
                                    temp_board[piece[0]][piece[1]] = '.'
                                    temp_board[new_row][new_col] = 'W'
                                    temp_board[capture_row][capture_col] ='.'
                                    if new_row == len(temp_board) - 1:
                                        temp_board[new_row][new_col] = '@'
                                    cap_valid_states.append(temp_board)
                            else:
                                capture_row = piece[0] + capture_row_dir * 2
                                capture_col = piece[1] + capture_col_dir * 2
                                i = piece[0] + capture_row_dir
                                found = False
                                if capture_row_dir == 0:
                                    for K in range(piece[1] + capture_col_dir, new_col):
                                        if temp_board[piece[0]][K] in 'wW@':
                                            found = True
                                if capture_col_dir == 0:
                                    for K in range(piece[0] + capture_row_dir, new_row):
                                        if temp_board[K][piece[1]] in 'wW@':
                                            found = True
                                
                                if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and (temp_board[capture_row][capture_col] == "b" or temp_board[capture_row][capture_col] == "B") and not found:
                                    temp_board[piece[0]][piece[1]] = '.'
                                    temp_board[new_row][new_col] = 'W'
                                    temp_board[capture_row][capture_col] ='.'
                                    if new_row == len(temp_board) - 1:
                                        temp_board[new_row][new_col] = '@'
                                    cap_valid_states.append(temp_board)

                for regular_dir in pikachu_regular_dir:
                    temp_board = copy.deepcopy(board)
                    new_row = piece[0] + regular_dir[0]
                    new_col = piece[1] + regular_dir[1]
                    present_flag = True
                    if abs(regular_dir[0]) != 1 or abs(regular_dir[1]) != 1:
                        if 0 <= piece[0] + regular_dir[0]//2 < len(board) and 0 <= piece[1] + regular_dir[1]//2 <len(board[0]) and temp_board[piece[0] + regular_dir[0]//2][piece[1] + regular_dir[1]//2] != ".":
                            present_flag = False
                    if 0<= new_row <len(temp_board) and 0<=new_col<len(temp_board[0]) and temp_board[new_row][new_col] == "." and present_flag:
                        temp_board[piece[0]][piece[1]] = '.'
                        temp_board[new_row][new_col] = 'W'
                        if new_row == len(temp_board) - 1:
                            temp_board[new_row][new_col] = '@'
                        reg_valid_states.append(temp_board)
                
            if board[piece[0]][piece[1]] == '@':
                for raichu_move in raichu_dir:
                    not_captured = True
                    captured_loc =(-1, -1)
                    if raichu_move[0] == 0 and raichu_move[1] == 1:
                        col = piece[1]
                        while col < len(board[0]) - 1:
                            temp_board = copy.deepcopy(board)
                            if temp_board[piece[0]][col+1] == '.':
                                temp_board[piece[0]][col+1] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                col += 1
                            elif temp_board[piece[0]][col+1] in 'bB$' and col + 2< len(board[0]) and temp_board[piece[0]][col+2] == '.' and not_captured:
                                temp_board[piece[0]][col+2] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[piece[0]][col+1] = '.'
                                captured_loc = (piece[0], col + 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                col += 2
                            else:
                                break
                    elif raichu_move[0] == 0 and raichu_move[1] == -1:
                        col = piece[1]
                        while col > 0:
                            temp_board = copy.deepcopy(board)
                            if temp_board[piece[0]][col-1] == '.':
                                temp_board[piece[0]][col-1] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                col -= 1
                            elif temp_board[piece[0]][col-1] in 'bB$' and col - 2>=0 and temp_board[piece[0]][col-2] == '.' and not_captured:
                                temp_board[piece[0]][col-2] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[piece[0]][col-1] = '.'
                                captured_loc = (piece[0], col - 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                col -= 2
                            else:
                                break
                    elif raichu_move[1] == 0 and raichu_move[0] == 1:
                        row = piece[0]
                        while row < len(board) - 1:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row + 1][piece[1]] == '.':
                                temp_board[row + 1][piece[1]] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row += 1
                            elif temp_board[row + 1][piece[1]] in 'bB$' and row + 2< len(board) and temp_board[row + 2][piece[1]] == '.' and not_captured:
                                temp_board[row + 2][piece[1]] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row + 1][piece[1]] = '.'
                                captured_loc = (row + 1, piece[1])
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row += 2
                            else:
                                break
                    elif raichu_move[1] == 0 and raichu_move[0] == -1:
                        row = piece[0]
                        while row > 0:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row - 1][piece[1]] == '.':
                                temp_board[row - 1][piece[1]] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row -= 1
                            elif temp_board[row - 1][piece[1]] in 'bB$' and row - 2>= 0 and temp_board[row - 2][piece[1]] == '.' and not_captured:
                                temp_board[row - 2][piece[1]] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row - 1][piece[1]] = '.'
                                captured_loc = (row - 1, piece[1])
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row -= 2
                            else:
                                break
                    elif raichu_move[1] == 1 and raichu_move[0] == 1:
                        row = piece[0]
                        col = piece[1]
                        while row < len(board) - 1 and col < len(board[0]) - 1:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row + 1][col + 1] == '.':
                                temp_board[row + 1][col + 1] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row += 1
                                col += 1
                            elif temp_board[row + 1][col + 1] in 'bB$' and row + 2< len(board) and col + 2< len(board[0]) and temp_board[row + 2][col + 2] == '.' and not_captured:
                                temp_board[row + 2][col + 2] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row + 1][col + 1] = '.'
                                captured_loc =(row + 1, col + 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row += 2
                                col += 2
                            else:
                                break
                    elif raichu_move[1] == -1 and raichu_move[0] == -1:
                        row = piece[0]
                        col = piece[1]
                        while row > 0  and col > 0:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row - 1][col - 1] == '.':
                                temp_board[row - 1][col - 1] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row -= 1
                                col -= 1
                            elif temp_board[row - 1][col - 1] in 'bB$' and row - 2>=0 and col - 2>=0 and temp_board[row - 2][col - 2] == '.' and not_captured:
                                temp_board[row - 2][col - 2] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row - 1][col - 1] = '.'
                                captured_loc =(row - 1, col - 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row -= 2
                                col -= 2
                            else:
                                break
                    elif raichu_move[1] == 1 and raichu_move[0] == -1:
                        row = piece[0]
                        col = piece[1]
                        while row > 0 and col < len(board[0]) - 1:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row - 1][col + 1] == '.':
                                temp_board[row - 1][col + 1] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row -= 1
                                col += 1
                            elif temp_board[row - 1][col + 1] in 'bB$' and row - 2>=0 and col + 2< len(board[0]) and temp_board[row - 2][col + 2] == '.' and not_captured:
                                temp_board[row - 2][col + 2] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row - 1][col + 1] = '.'
                                captured_loc =(row - 1, col + 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row -= 2
                                col += 2
                            else:
                                break
                    elif raichu_move[1] == -1 and raichu_move[0] == 1:
                        row = piece[0]
                        col = piece[1]
                        while row < len(board) - 1 and col > 0:
                            temp_board = copy.deepcopy(board)
                            if temp_board[row + 1][col - 1] == '.':
                                temp_board[row + 1][col - 1] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                if captured_loc[0] != -1:
                                    temp_board[captured_loc[0]][captured_loc[1]] = "."
                                reg_valid_states.append(temp_board)
                                row += 1
                                col -= 1
                            elif temp_board[row + 1][col - 1] in 'bB$' and row + 2< len(board) and col - 2>=0 and temp_board[row + 2][col - 2] == '.' and not_captured:
                                temp_board[row + 2][col - 2] = '@'
                                temp_board[piece[0]][piece[1]] = '.'
                                temp_board[row + 1][col - 1] = '.'
                                captured_loc =(row + 1, col - 1)
                                not_captured = False
                                cap_valid_states.append(temp_board)
                                row += 2
                                col -= 2
                            else:
                                break
    #giving priority of capture moves
    return cap_valid_states + reg_valid_states


# Method to calculate best_move
def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #

    # Convert the string to 2D matrix
    board_matrix = convert_board(board, N)

    # setting player piece
    is_black = True
    if player == 'w':
        is_black = False

    # getting successor boards
    succ_board = get_moves(board_matrix, is_black)
    max_value = -20000

    # Iterating each board
    for b in succ_board:

        # calling min_value to calculate aplha beta pruning
        alpha =  min_value(b, -20000, 20000, is_black, 4)
        if alpha >= max_value:
            max_value = alpha
            b = [''.join([str(c) for c in lst]) for lst in b]
            b = ''.join(b)
            # Yielding Board
            yield(b)
    

if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
     
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
