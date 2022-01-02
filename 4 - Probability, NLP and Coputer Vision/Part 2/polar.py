#!/usr/local/bin/python3
#
# Authors: Himanshu Himanshu(hhimansh), Varsha Ravi Varma(varavi), Aman Chaudhary(amanchau)
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#
# Reference for Viterbi Implemenattion: Professor David Crandall implementation from class exercise

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import copy
import math

# calculate "Edge strength map" of an image                                                                                                                                      
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [ (pt[0]+dx, pt[1]+dy) for dx in range(-3, 4) for dy in range(-2, 3) if dx == 0 or dy == 0 or abs(dx) == abs(dy) ]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors 
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = draw_boundary(image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)

# This algorithm is for computing boundries through simple method baysian model
def compute_simple(edge_strength):

    # Taking two arrays for finding boundries
    airice_simple = []
    icerock_simple = []

    # Iterating through each col to find the point of boundaries
    for col in range(len(edge_strength[0])):

        # finding edge strength of each row in each column
        emission_prob = [row[col] for row in edge_strength]

        # finding total sum of edge strength in a col
        sum_edge_strength = sum(emission_prob)

        # converting the edge strength of row in a col to probability
        emission_prob = [value/sum_edge_strength for value in emission_prob]

        # finding the max edge in a col Taking assumption that air-ice boundary is in first quarter of image
        max_edge = max(emission_prob[:int(0.25*len(emission_prob))])

        # Finding the max probability index and appending it to airice list
        index_max_edge = emission_prob.index(max_edge)
        airice_simple.append(index_max_edge)

        # Finding the edge with max probability which is atleast 10 pixels  below air-ice boundary and appending it to ice_rock list
        max_edge = max(emission_prob[index_max_edge+10:])
        index_max_edge = emission_prob.index(max_edge)
        icerock_simple.append(index_max_edge)

    # returning both the list as tupple
    return (airice_simple, icerock_simple)

# Method for calculating boundaries using viterbi
# Reference for Viterbi Implemenattion: Professor David Crandall implementation from class exercise
def compute_viterbi_split(edge_strength):

    # Getting Number of cols
    N = len(edge_strength[0])

    # Getting Number of rows
    M = len(edge_strength) 

    # Initialising V_table and which_table
    V_table_ice = []
    which_table_ice = [] 

    # getting edge strength of each row for column 0
    emission_prob = [row[0] + 1 for row in edge_strength]

    # Calculating the sum of all edge strength
    sum_edge_strength = sum(emission_prob)

    #converting edge strength to probability
    emission_prob = [math.log10(value/sum_edge_strength) for value in emission_prob]

    # appending emission prob to V_table for col 0
    V_table_ice.append(copy.deepcopy(emission_prob))

    # appending all rows to which_table
    which_table_ice.append([i for i in range(len(edge_strength))])

    # Iterating through each col in image
    for col in range(1, N):

        # Intitalising temp V_table and which table
        temp_V_table_ice = []
        temp_which_table_ice = []

        # finding edge strength of each row in the column
        emission_prob = [row[col] + 1 for row in edge_strength]

        # finding sum of edge strength
        sum_edge_strength = sum(emission_prob)

        ## converting edge strength to probability
        emission_prob = [math.log10(value/sum_edge_strength) for value in emission_prob]

        # Iterating through each row
        for row in range(M):

            # Caculating standard deviation to find normal distribution about row and finding the transition probability
            sd = 0
            for i in range(M):
                sd += (i - row) ** 2
            sd = sd / M
            sd = math.sqrt(sd)
            transition_prob =[]
            for i in range(M):
                transition_prob.append(abs(i - row)/sd)
            init = 1/(math.sqrt(2*math.pi) * sd)     
            for i in range(M):
                transition_prob[i] = math.log10(init * math.exp(-0.5 * ( transition_prob[i]**2)))

            # calculating the temp_which and temp_V value and appending it to temp_V and temp_which table  
            temp_which_ice, temp_V_ice = max([(i, V_table_ice[col - 1][i] + transition_prob[i]) for i in range(M)], key = lambda l:l[1])
            temp_V_ice = temp_V_ice + emission_prob[row]
            temp_V_table_ice.append(temp_V_ice)
            temp_which_table_ice.append(temp_which_ice)

        # Appending temp_V and temp_which table to V_table and which_table
        V_table_ice.append(copy.deepcopy(temp_V_table_ice))
        which_table_ice.append(copy.deepcopy(temp_which_table_ice))

    # initialising list for backtracking viterbi table to return the result
    ice_viterbi = [0] * N

    # finding point row for N-1 column
    ice_viterbi[N-1] = V_table_ice[N-1].index(max(V_table_ice[N-1]))

    # Iterating through every column from last and appending value point from which table to list
    for i in range(N-2, -1, -1):
        ice_viterbi[i] = which_table_ice[i+1][ice_viterbi[i+1]]

    # Returning list of final point
    return ice_viterbi
    
# Method for spliting Edge strength list to airice list with same assumption that air ice boundary is in upper 25% of image
def compute_viterbi(edge_strength):

    # finding no of rows pixels in image
    M = len(edge_strength) 

    # Calling viterbi for air_ice boundaries by splitting
    airice_hmm = compute_viterbi_split(edge_strength[:int(0.25*M)])

    # Calling viterbi for ice_rock boundaries by splitting according to min pixel of airice
    min_airice = min(airice_hmm)
    edge_strength_icerock = copy.deepcopy(edge_strength)
    edge_strength_icerock = edge_strength_icerock[min_airice + 10:].tolist()
    for col in range(len(airice_hmm)):
        if airice_hmm[col] == min_airice:
            continue
        for row in range(airice_hmm[col] - min_airice):
            edge_strength_icerock[row][col] = 0
    
    # Calling viterbi for ice_rock boundaries by splitting
    icerock_hmm = compute_viterbi_split(edge_strength_icerock)

    # Adding rows which was removed because of split
    icerock_hmm = [value + min_airice + 10 for value in icerock_hmm]

    # Returning both boundaries
    return (airice_hmm, icerock_hmm)

# Method for calculating boundaries using viterbi with feedbacks
# Reference for Viterbi Implemenattion: Professor David Crandall implementation from class exercise
def compute_feedback_split(edge_strength, feedback):


    # Getting Number of cols
    N = len(edge_strength[0])

    # Getting Number of rows
    M = len(edge_strength)  
    
    # Finding row in feedback
    feedback_row = feedback[0]

    # finding column in feedback
    feedback_col = feedback[1]

    # Initialising V_table and which_table    
    V_table_ice = []
    which_table_ice = [] 

    
    # getting edge strength of each row for column 0
    emission_prob = [row[0] + 1 for row in edge_strength]

    # Calculating the sum of all edge strength
    sum_edge_strength = sum(emission_prob)

    #converting edge strength to probability
    emission_prob = [math.log10(value/sum_edge_strength) for value in emission_prob]

    # appending emission prob to V_table for col 0
    V_table_ice.append(copy.deepcopy(emission_prob))

    # appending all rows to which_table
    which_table_ice.append([i for i in range(len(edge_strength))])

    # Iterating through each col in image
    for col in range(1, N):

        # Intitalising temp V_table and which table
        temp_V_table_ice = []
        temp_which_table_ice = []

        # finding edge strength of each row in the column
        emission_prob = [row[col] + 1 for row in edge_strength]

        # finding sum of edge strength
        sum_edge_strength = sum(emission_prob)

        ## converting edge strength to probability
        emission_prob = [math.log10(value/sum_edge_strength) for value in emission_prob]

        # Iterating through each row
        for row in range(M):

             # Caculating standard deviation to find normal distribution about row and finding the transition probability
            sd = 0
            for i in range(M):
                sd += (i - row) ** 2
            sd = sd / M
            sd = math.sqrt(sd)
            transition_prob =[]
            for i in range(M):
                transition_prob.append(abs(i - row)/sd)
            init = 1/(math.sqrt(2*math.pi) * sd)     
            for i in range(M):
                transition_prob[i] = math.log10(init * math.exp(-0.5 * ( transition_prob[i]**2)))

            # if we are in same column as feedback column setting transition probability of feedback rock as 1 and all other 0
            if col == feedback_col:
                transition_prob = [0] * M
                transition_prob[feedback_row] = 1

            # calculating the temp_which and temp_V value and appending it to temp_V and temp_which table 
            temp_which_ice, temp_V_ice = max([(i, V_table_ice[col - 1][i] + transition_prob[i]) for i in range(M)], key = lambda l:l[1])
            temp_V_ice = temp_V_ice + emission_prob[row]
            temp_V_table_ice.append(temp_V_ice)
            temp_which_table_ice.append(temp_which_ice)
        
        # Appending temp_V and temp_which table to V_table and which_table
        V_table_ice.append(copy.deepcopy(temp_V_table_ice))
        which_table_ice.append(copy.deepcopy(temp_which_table_ice))

    
    # initialising list for backtracking viterbi table to return the result
    ice_viterbi = [0] * N

    # finding point row for N-1 column
    ice_viterbi[N-1] = V_table_ice[N-1].index(max(V_table_ice[N-1]))

    # Iterating through every column from last and appending value point from which table to list
    for i in range(N-2, -1, -1):
        ice_viterbi[i] = which_table_ice[i+1][ice_viterbi[i+1]]

    # Returning list of final point
    return ice_viterbi

# Method for spliting Edge strength list to airice list with same assumption that air ice boundary is in upper 25% of image
def compute_feedback(edge_strength, gt_airice, gt_icerock):

   # finding no of rows pixels in image
    M = len(edge_strength) 

    # Calling viterbi for air_ice boundaries by splitting 
    airice_hmm = compute_feedback_split(edge_strength[:int(0.25*M)], gt_airice)

    # Calling viterbi for ice_rock boundaries by splitting according to min pixel of airice and converting feedback accordingly
    min_airice = min(airice_hmm)
    edge_strength_icerock = copy.deepcopy(edge_strength)
    edge_strength_icerock = edge_strength_icerock[min_airice + 10:].tolist()
    gt_icerock[0] = gt_icerock[0] - (min_airice + 10)
    for col in range(len(airice_hmm)):
        if airice_hmm[col] == min_airice:
            continue
        for row in range(airice_hmm[col] - min_airice):
            edge_strength_icerock[row][col] = 0

    # Calling viterbi for ice_rock boundaries by splitting
    icerock_hmm = compute_feedback_split(edge_strength_icerock, gt_icerock)

    # Adding rows which was removed because of split
    icerock_hmm = [value + min_airice + 10 for value in icerock_hmm]
    
    # Returning both boundaries
    return (airice_hmm, icerock_hmm)

# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception("Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")
    input_filename = sys.argv[1]
    gt_airice = [ int(i) for i in sys.argv[2:4] ]
    gt_icerock = [ int(i) for i in sys.argv[4:6] ]

    # load in image 
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))
    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength = edge_strength(input_image)
    #print(edge_strength)
    imageio.imwrite('edges.png', uint8(255 * edge_strength / (amax(edge_strength))))

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.
    airice_simple, icerock_simple = compute_simple(edge_strength)
    airice_hmm, icerock_hmm = compute_viterbi(edge_strength)
    airice_feedback, icerock_feedback =  compute_feedback(edge_strength, gt_airice, gt_airice)
    
    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
