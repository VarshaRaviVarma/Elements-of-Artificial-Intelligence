#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Himanshu Himanshu(hhimansh), Varsha Ravi Varma(varavi), Aman Chaudhary(amanchau)
#
# (based on skeleton code by D. Crandall, Oct 2020)
#
# Reference for Viterbi Implemenattion: Professor David Crandall implementation from class exercise
# Reference: https://www.ijrte.org/wp-content/uploads/papers/v7i4s2/Es2046017519.pdf
# Reference: https://bihe-edu.github.io/OCR/

from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

# Training letters to be used anywhere in the code
TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

# Taking min value of probability as -inf
min_val = float('-inf')

# Initialising initial probability, character probability, emission probability and transition probability 
# dictionaries to used anywhere in code
init_prob = {}
char_prob = {}
emit_prob = {}
trans_prob = {}

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

# Function to match grids of characters
def grid_match(grid1, grid2):

    # initialising space and star matches variable
    space_matches = 0
    star_matches = 0

    # Iterating through each row of grids and cols of grid and matching every 
    # character in that if its a match checking if its star or space and increasing variable respectively
    for i in range(len(grid1)):
        for j in range(len(grid1[i])):
            if grid1[i][j] == grid2[i][j]:
                if grid1[i][j] == " ":
                    space_matches += 1
                else:
                    star_matches += 1
    
    # Returning number of both matches
    return (space_matches, star_matches)

# This function is to compute emission probability 
def compute_emission():    

    # Finding total pixels of characters
    total_pixels = CHARACTER_WIDTH * CHARACTER_HEIGHT

    #  Iterating through each index of character in test letters
    for i in range(len(test_letters)):

        # Iteration through each character in training letter
        for train_letter, train_letter_grid in iter(train_letters.items()):

            # finding star and space pixel match
            (space_matches, star_matches) = grid_match(test_letters[i], train_letter_grid)

            # finding no of unmatch pixels
            unmmatch = total_pixels - (space_matches + star_matches)

            # Assigning different weights to different probabilities to reduce noise
            space_match_prob = 0.25 * space_matches/total_pixels
            star_match_prob = 1.5 * star_matches/total_pixels
            unmatch_prob = 0.000005 * unmmatch/total_pixels

            # Muliplying all probabilities for each pixel in case adding because probailities are in log 
            prob = 0
            if space_match_prob != 0:
                prob +=  space_matches * math.log10(space_match_prob)
            if star_match_prob != 0 :
                prob += star_matches * math.log10(star_match_prob)
            if unmatch_prob !=0 :
                prob += unmmatch * math.log10(unmatch_prob)

            # Setting emit probability of character at i index
            if i in emit_prob:
                emit_prob[i][train_letter] =  prob
            else:
                emit_prob[i] = {}
                emit_prob[i][train_letter] =  prob
    
# Method to train the model or finding probabilities 
def train(train_txt_fname):

    # Reading a text file
    file = open(train_txt_fname, 'r')

    # for all the line in
    for line in file:   

        # if initial word is not present in the initial probability dictionary its initialises it 
        if line[0] not in init_prob:
            init_prob[line[0]] = 0

        # Inceasing count of iniitial probability
        init_prob[line[0]] += 1

        # if character is not in character probability list initialising it
        if line[0] not in char_prob:
            char_prob[line[0]] = 0
        
        # increasing character count by 1
        char_prob[line[0]] += 1

        # Looping through each character of line and findind transition counts for each character and count of each character
        for i in range(1, len(line)):
            if line[i] == '\n':
                continue
            if line[i] not in char_prob:
                char_prob[line[i]] = 0
            char_prob[line[i]] += 1
            if line[i-1] in trans_prob:
                if line[i] not in trans_prob[line[i-1]]:
                    trans_prob[line[i-1]][line[i]] = 0
                trans_prob[line[i-1]][line[i]] += 1
            else:
                trans_prob[line[i-1]] = {}
                trans_prob[line[i-1]][line[i]] = 1

    # Total sum of characters
    sum_char = sum(char_prob.values())

    # converting each character count to its probability
    for char in char_prob:
        char_prob[char] = math.log10(char_prob[char] / sum_char)
    
    # if any character was not in character probability setting it to -inf
    for char in TRAIN_LETTERS:
        if char not in char_prob:
            init_prob[char] = min_val

    # Total sum of initial characters
    sum_init_prob = sum(init_prob.values())

    # Converting each count to probability
    for char in init_prob:
        init_prob[char] = math.log10(init_prob[char] / sum_init_prob)

    # if any character was not in initial character probability setting it to -inf
    for char in TRAIN_LETTERS:
        if char not in init_prob:
            init_prob[char] = min_val

    # Converting number of transition to transition probability for each caharacter if not present in list setting in to -inf
    for char in trans_prob:
        sum_char = sum(trans_prob[char].values())
        for key in trans_prob[char]:
            trans_prob[char][key] = math.log10(trans_prob[char][key] / sum_char)
        for key in TRAIN_LETTERS:
            if key not in trans_prob[char]:
                trans_prob[char][key] = min_val
  
# Method to find letters of image using simple bayes net algorithm
def simplified(test_letters):

    # Initialising list for appending predicted 
    predicted_output = []

    # iterating through each indeex in image
    for i in range(len(test_letters)):

        # setting best character as space and best probability as min_value which is -inf
        best_char = " "
        best_prob = min_val

        # finding char and prob of that char in emission probability dictionary for index i of sentence
        for char, prob in iter(emit_prob[i].items()):

            # finding final probability of particular character by multiplying its emission probality to its occurance probability
            curr_prob = prob + char_prob[char]

            # if final probability is greater than best probability then changing best probability to that and best character 
            # to current character
            if curr_prob > best_prob:
                best_char = char 
                best_prob = curr_prob
        
        # appending best character to the list
        predicted_output.append(best_char)
    
    # returning Characters by joining them
    return ''.join(predicted_output)

# Method to find letters of image using simple hmm model
# Reference for Viterbi Implemenattion: Professor David Crandall implementation from class exercise
def hmm(test_letters):

    # Finding all characters that are allowed
    char_list = list(TRAIN_LETTERS)  

    # Find no of charcters in Test image
    N = len(test_letters)

    # Initialising empty V_table and which_table 
    V_table = {}
    which_table = {}

    # Initailising V_table and which_table for each independent character and no of characters
    for char in char_list:
        V_table[char] = [0] * N
        which_table[char] = [0] * N

    # Iterating through each char and setting its probability for 0 index in V_table 0 index of each character
    for char in char_list:
        V_table[char][0] = emit_prob[0][char] + init_prob[char]

    # Iterating through each index of character in image
    for i in range(1,N):

        # Iterating through each independent char
        for char in char_list:

            # Finding which table and V table for each char at i index which is the most probale character from which which 
            # we can come to this character with what probability
            (which_table[char][i], V_table[char][i]) =  max( [ (s0, V_table[s0][i-1] + trans_prob[s0][char]) for s0 in char_list ], key=lambda l:l[1] )
            
            # Multiplying emiison probability of that char at i index here we are adding because we have taken probailities in log
            V_table[char][i] = V_table[char][i] + emit_prob[i][char]

    # Making a prdecited list of N Characters
    predicted_output = [""] * N

    # Seeting best probability as -inf
    prob = float('-inf')

    # Iterating through each char on final index finding best suitable charcater for last index based on probaility stored in V_table
    for char in V_table:
        if V_table[char][N - 1] >= prob:
            prob  = V_table[char][N - 1]
            predicted_output[N - 1] = char

    # Iterating through each index of Image from last and finding best char from which through which we can reach that character
    for i in range(N-2, -1, -1):
        predicted_output[i] = which_table[predicted_output[i+1]][i+1]
    
    # returning Characters by joining them 
    return ''.join(predicted_output)

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

train(train_txt_fname)
compute_emission()


## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!

# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
# print("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
# print("\n".join([ r for r in test_letters[2] ]))



# The final two lines of your output should look something like this:
print("Simple: " + simplified(test_letters))
print("   HMM: " + hmm(test_letters)) 
