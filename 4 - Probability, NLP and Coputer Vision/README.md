# ASSIGNMENT 3

### Members:
#### Himanshu Himanshu - hhimansh@iu.edu
#### Aman Chaudhary - amanchau@iu.edu
#### Varsha Ravi Varma - varavi@iu.edu	
	   	


## PART 1:

Part 1 involves POS tagging in which the goal is to mark every word in a sentence with its part of speech (noun, verb, adjective, etc.)

### Observation:

There were 5 functions given in the skeleton code, i.e., posterior (which had if-else statements that calculates posterior probabilities for all 3 parts of the assignment), train, simplified (which was to return the predicted tags depending on simple bayesian network algorithm), hmm_viterbi (to return the predicted tags based viterbi) and complex_mcc (to return result based on mcc calculations). The utility and evaluation functions were given in the initial skeleton code.

### Approach and design decisions:

For the simple model, we have initialized the posterior probability as 1 for the ease of multiplication. We have then iterated through each label and word and found the tag and word at the ith index. We have then checked if the word is there in the word emission probability, it its present then we have checked the probability of the tag assigned to that word, and if it is not present or probability of tag of that word is 0 we have taken the probability as 0.000000001. If the posterior comes out to be 0 then we have set the posterior probability to 0.000000001 and then returned the log of the posterior probability.

For the HMM model, just like the Simple model, we have again initialized the posterior probability as 1 for the ease of multiplication and then iterated through each label and word and found the tag and word at the ith index. We have then checked if the word is there in the word emission probability, it its present then we have checked the probability of the tag assigned to that word, and if it is not present or probability of tag of that word is 0 we have taken the probability as 0.000000001. We have then multiplied the probability of tag I with the posterior probability. We have then multiplied each transition probability to compute the posterior probability. If the posterior comes out to be 0 then we have set the posterior probability to 0.000000001 and then returned the log of the posterior probability.

For the Complex model, just like the Simple model, we have again initialized the posterior probability as 1 for the ease of multiplication and then iterated through each label and word. We have set the emission probability as 0.000000001. If the word exists in word emit probability and its value is not 0 then we have set it. We have then set the transition probability from the current state to the next state which was initially set to 0.000000001. Similarly, we have then set the transition probability from the last state to the current state which was initially set to 0.000000001. Now if the index is 0 we have multiplied the transition probability from the current state to the next state with the emission probability and the tag probability of the current tag. If the index is N-1 we have multiplied the transition probability from the last state to the current state with the emission probability and the tag probability of the last tag otherwise we have multiplied the transition probability from the current state to the next state with the emission probability, tag probability of the last tag and the transition probability from the last state to the current state. If the posterior probability comes out to be 0, we have set it to 0.000000001. We have then returned the log of posterior probability.

For the training, we have initialized an empty dictionary for the tag probability. We have used tag as the key and the occurrence as the value. It will be a nested dictionary with key as tag and value as dictionary of tags as key and their transition probability as value. For the word emit probability, it will be a nested dictionary word as key and value as dictionary of tags as key and their probability to occur for a given word as value. Then we have set an initial probability dictionary with tag as key and probability of its occurrence first in sentence as key. We have then set the initial occurrence of a tag, if its already present we have increased it else initialized it. We have then iterated through each tag to set the transition of each tag in the sentence. If the current tag is present in the transition dictionary, we have increased the count by 1 otherwise initialized it to 1, else if the current tag is not present in the transition dictionary, we have initialized its initial dictionary and have set its value to 1. We have then iterated through each tag and increased the count by 1 if it exists otherwise initialized it to 1.

Then we have iterated through each word and set the count of tag for each word. If the word already exists in the word emission dictionary, and if tag exists for the word in the emission dictionary, then we have increased the count by 1 else initialized it to 1, else, we have re initialized the dictionary and have set the occurrence of tag to 1. We have then calculated the tag list and the total number of tags. We have then divided the tag probability with the count of tags and divided the init probability with total length of the data. We have then changed the count of the transition to the transition probability for each tag from ach tag. We have then changed the word emit probability dictionary which is probability of tag if a word is given from its count to probability.

Now moving to the simplified method, if the word is not present in the word emit prob dictionary, we will continue and go to the next iteration. If the word exists, we will initially take the max prob tag as ‘noun’ and set it to 0. No, we have iterated through each word in the word emit prob dictionary for that word, we have found the probability of occurrence of that tag by multiplying emit prob of that tag with the occurrence probability of the tag. If this probability is greater than the max probability, then we have set the tag as maximum probable tag and the maximum probability as the current probability. We have appended the max prob tag to the predicted tag list.

For HMM Viterbi, we have initialized an empty V table to maintain what is the highest probability to reach that state from the previous state. We have also initialized an empty which table to maintain from which previous state we can reach that state with highest probability. We have then found the V table probability for index word as index 0 for each word. Next we have iterated through each tag in the tag list and used the init probability with emit probability to calculate the probability of index 0 in the V table. Next we have found the best tag from the previous state and max probability by which we can reach a particular tag for the word at index i by multiplying probability of each tag from previous state and multiplying it by transition probability and finding the max of it. Initially we have set the tag to ’noun’ and the probability to -1. We then iterate through every key in the V table and finding the value of N-1 index if its greater than probability initially set as -1. WE have returned the predicted tag by finding the predicted tag for index i using the which table with backtracking.

For MCMC, we have written a generator function which we will use for the MCMC method. We have iterated through each tag of the list, if the word exists in the emit prob dictionary we have found its probability from there, we have then calculated transition probabilities from current state to next and previous state to current state. These probabilities are then appended, depending on different location. The sum of all these probabilities is calculated. We have then calculated the cumulative sum. Next, we have used this generator for calling MCMC.

### Challenges:

The main challenge was to understand the entire concept of MCMC and apply it in our code. We also had a difficult time while trying to increase the accuracy of our code.

### Results:

So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct:
		   
0. Ground truth:       100.00%              100.00%
1. Simple:              92.72%               42.05%
2. HMM:                 94.30%               50.25%
3. Complex:             92.90%               43.15%



## PART 2:

Part 2 involves creating code that tries to find the two boundaries, i.e., air-ice and ice-rock in a given sonar image. We’ll make some assumptions to make this possible.

### Observation:

There were 3 functions given in the skeleton code, i. E., draw_boundary (draws the boundary line in the image depending on the color assigned by us), draw_asterisk (draws asterisk on the 2 points x1y1 and x2y2 in which one is located in the air-ice boundary and the other is located in the ice-rock boundary) and write_output_image (function calls draw_boundary and draws boundaries of different colors for simple, viterbi and viterbi_feedback). 
Image can be read in different pixels with different edge weights where edge weight is how dark a pixel is. 

### Approach and design decisions:

**Assumption:** The air-ice boundary will present in the top 25% part of the image.

A function named compute_simple is defined that computes boundaries through a simple bayesian model. In this function we iterate through each column to find the point of boundaries using a for loop. In the for loop, we find out the edge strength and its total length and convert it to probability values. We find the max edge and probability index. We also find the edge with the max probability which is at least 10 pixels below air-ice boundary and append it to the ice-rock list. This function returns both airice_simple and icerock_simple lists.

We defined a compute_viterbi_split function that calculates boundaries using viterbi. Another function we defined is the compute_viterbi that splits edge strength list to airice list. 

In the compute_viterbi_split function, we calculate the boundaries using viterbi. We find the number of rows and columns of edge strength and also feedback, initialise V_table and which_table, calculate the sum of all edge strength and convert that to probability. Then we append the emission probability to V_table and all the rows to which table. We then iterate through each column of the image in which we again calculate the emission probability and also iterate through each row and calculate the standard deviation to find normal distribution about the row and find the transition probabilities. We initialise the list for backtracking the viterbi table to return the result and find the point row for N-1 column. We again iterate through every column from last and append value point from which_table to list. We return the ice_viterbi value.

In the compute_feedback_split function, we calculate the boundaries using viterbi with feedback. We find the number of rows and columns of edge strength and also feedback, initialise V_table and which_table, calculate the sum of all edge strength and convert that to probability. Then we append the emission probability to V_table and all the rows to which table. We then iterate through each column of the image in which we again calculate the emission probability and also iterate through each row and calculate the standard deviation to find normal distribution about the row and find the transition probabilities. We check if we are in the same column as the feedback column then we set the transition probability of feedback rock as 1 and all others as 0. We initialise the list for backtracking the viterbi table to return the result and find the point row for N-1 column. We again iterate through every column from last and append value point from which_table to list. We return the ice_viterbi value.

In the compute_feedback function, we split edge strength list to article list with the same assumption that airice boundary is in the upper 25% of image. In this function, we find the number of row pixels in the image and call the viterbi function for air_ice boundaries by splitting. We also call the viterbi function for ice_rock boundaries by splitting and converting feedback accordingly. We add the rows which were removed during the split and return both airice_hmm and icerock_hmm boundaries.

### Challenges:

Figuring out the necessary assumptions required to solve this problem was difficult.



## PART 3:

Part 3 involves reading an image and figuring out the characters in that image. This is called OCR (Optical Character Recognition). 

### Observation:

There were 2 functions given in the skeleton code, i.e., load_letters and load_training_letters that convert the characters in training and testing images into star patterns. We used these patterns to compare the trained images and test images to obtain the result.

### Approach and design decisions:

We have used a grid match function to match the grid of characters. For this we have iterated through each row of the grids and cols of grid matching every character in that if it’s a match, we have checked if it’s a start (‘*’) or space (‘ ‘) by increasing the variables separately.

For the compute emission function, we have calculated the total pixels. We have then iterated through each index of character in test letters and through each character in the training letter. Then we have called the grid match function on the test letters and train letter grid to calculate the space and star matches. Total unmatched is the difference between the total pixels and matched pixels. Then we have assigned different weights to different probabilities to reduce the noise. Going forward, we have multiplied all the probabilities for each pixel and adding it to the probabilities as they are calculated in log. Then we have set the emit probability of the character at index i.

Next for the train function, we have read all the lines. If the initial word is not present in the initial probability dictionary, it initializes it. We have then increased the count of the initial probability by 1. If the character is not present in the character probability dictionary, it initializes it. We have then increased the character count by 1. We have then looped through each character of the line and found the transition counts for each character and count of each character. Then we have calculated the total sum of characters and converted each character count to its probability. If the character was not present, the probability is set to -inf. Then we have calculated the total sum of initial characters and converted each character count to its probability. If the character was not present, the probability is set to -inf. At last, we have converted the number of transitions to transition probability for each character, if it’s not present, set it to -inf.

For the simplified method, we have iterated through each index in the image. We have set the best character as space and the best probability as minimum value. Then we have found the char and prob of that character and their emission probability dictionary for index i of sentence. We have then found the final probability, if the final probability is greater than best probability, then we have swapped it with the current probability and the current character. We have then appended this best char to the predicted output.

For HMM, we have initialized a V table and which table of size N which is the number of characters. We have then iterated through each character and setting its probability for 0 index in V table and 0 index in each character. We have then iterated through each index of character in image and through each independent character and found the which table and V table for each character and i index which is the most probable character from which we can come to this character with what probability. We have then multiplied the emission probability of that char at i index and added in case of log. We have then initialized an empty list of size N and the best probability as -inf. We have then iterated through each character on the final index finding the best suitable character for the last index based on the probability stored in V table. Then we have iterated through each index of image from last and found the best char from which through which we can reach the character. We have returned the characters by joining them.

**Assumption:** We have assigned different arbitrary weights to character match probability.



### Challenges:

Finding the emission probability was quite difficult in this problem. 



## References:

1) https://github.com/ajcse1/Part-of-Speech-Tagger/blob/master/pos_solver.py 
2) Professor David Crandall’s viterbi implementation from class exercise
3) https://www.ijrte.org/wp-content/uploads/papers/v7i4s2/Es2046017519.pdf
4) https://bihe-edu.github.io/OCR/
5) Discussion with Rohan Joseph (rohajose@iu.edu)
