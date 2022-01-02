# ASSIGNMENT 2

### Members:
#### Himanshu Himanshu - hhimansh@iu.edu
#### Aman Chaudhary - amanchau@iu.edu
#### Varsha Ravi Varma - varavi@iu.edu	
	   	


## PART 1:

Part 1 involves a modified checkers game with three kinds of pieces i.e., pichus, pikachus and raichus, of two different colors i.e., black and white.

### Observation:

It is a modified checkers game and therefore we are expected to use a minimax based algorithm. 

**State space:** Boards that being traversed in the game.

**Initial state:** Input board.

**Goal state:** The board with the best move which we can reach from the initial input board.

**Successor state:** The very next set of boards that can be achieved from the initial input board. 

**Utility/evaluation function:** (Number of AI pieces - Number of opponent pieces) * 500 + Number of AI pieces * 50.

### Approach and design decisions:

**Abstraction technique:** Alpha-beta pruning with definite depth (constrained alpha-beta pruning)

Initially we convert the board string into a two dimensional matrix. We find all the successor states and run alpha-beta pruning on each of the successor states to find the highest alpha value. We are setting max value as the alpha value when alpha value is greater than max value and we yield that board. We are implementing the alpha-beta pruning algorithm using depth equating to 4. We define a ‘get_move’ function in which we are finding all the moves, i.e., pichu, pikachu and raichu, for a given board.

### Challenges:

The main challenge was to find the utility function and depth upto which we have to run alpha-beta pruning to get the results within 10 seconds. Another challenge was constructing the ‘get_move’ function for the board.



## PART 2:

Problem in part 2 is based on the popular tetris game. The goal is to write a computer player for this game that scores as high as possible. 

### Observation:

The moves function which includes right, left, down, rotate and flip movements, and line clearing (score) function were  already given. 

**State space:** All the configurations that we can obtain by adjusting random pieces on the board.

**Initial state:** Empty quintris board.

**Goal state:** The maximum scoring board.

**Successor state:** The next board with the best block move.

**Utility/evaluation function:** (w1 * aggregate_height) + (w2 * bumpiness) + (w3 * number_of_holes) + (w4 * deepest_well) + (w5 * score).

### Approach and design decisions:

**Abstraction technique:** Genetic algorithm

We started by creating the following utility functions: 
1) Column height: Returns a list that includes the height value of each column. Using this function, we can calculate the aggregate height and maximum height. 
2) Bumpiness: Returns the sum of absolute height differences between the columns. 
3) Deepest well: Returns the maximum depth value
4) Number of holes: Returns the number of holes present in the board at that point of time.

We are implementing the genetic algorithm by assigning weights to these utility functions and also to the score function. We are calculating the heuristic value by multiplying the weights with their respective utility functions and returning the total heuristic value. We are now computing the best move by rotating the block piece and moving it to the left as much as we can. We then move the piece to the right by one column until we reach the quintris border and everytime we make this move, we calculate it is an optimal move. We then flip the piece and repeat the right movement process until the best move is found. 

We have generated a sample where we have generated random weights. We defined another function to compute the fitness of the sample. We have called the computer player class with the randomly generated weights and we have also generated a simple quintris object and called the start game function. Furthermore, we are adding the total score to the fitness of the sample taken. We have selected 10% of the population at random and then we are selecting two fittest candidates. We then do a crossover using both candidates with their respective weights. “ 'heightWeight': candidate1['fitness']* candidate1['heightWeight'] + candidate2['fitness']* candidate2['heightWeight'] “. 

We perform an offspring mutation where we are giving a small chance (5%) for the offspring to mutate. However, if the offspring does not mutate, it is adjusted by 0.2. We perform normalization on the weights of the sample. Once the number of offspring produced reaches a certain value of the original population size, some of the offspring are deleted and replaced forming the next generation of the population. 

For the main genetic function we have created a sample population and initialized the number of rounds. Next, we have appended the randomly generated candidates to the sample list. Then we computed the fitness of the sample. We have performed multiple iterations to select the best offspring. For this, we have called the pair_selection(), crossover() and offspring_mutation(). We then compute the fitness again and replace a portion of the total population with a new population. The weights with the greatest fit that are being generated by the genetic algorithm need to be replaced with the weights that we are passing initially in the quintris. 


### Challenges:

Firstly, finding the right approach to this problem placed us in a very confusing state. Furthermore, even though we did figure out what algorithm we will be using, finding the right weight values for the algorithm was yet another challenge. We also had a tough time figuring out how to store the generated weights. Another challenge was that we were not able to implement the animated version.



## PART 3:

Part 3 involves estimating the Naive Bayes parameters from the training dataset and then using those parameters to identify whether the reviews are fake or legitimate for 20 hotels in Chicago.

### Observation:

There are two text files to be analyzed, among which one contains training data and the other contains testing data. Using these files, we build and train a probability model that predicts whether a statement is true or false based on truth and deception statements given in the training dataset. 

### Approach and design decisions:

**Abstraction technique:** Bayes net

This is a classical classifier problem that involves classifying data with large datasets. To begin with, we read the training data file and use dictionaries of lists with keys corresponding to objects, labels, and classes, and values representing comments, categories of comments, and distinct categories. Three empty dictionaries have been created to store truthful and deceptive words and their counts. Also, we created a list of stop words such as "between", "but", "they", etc. Next, we assigned each label and comment into respective lists. In the following step, we calculated the prior that any comment would be truthful or deceptive. We iterate through each comment, clean it by removing punctuation and numbers and converting each character to lowercase. By splitting the comments into tokens, we check if the tokens are stop words then we skip that token. Tokens that already exist in the truthful/deceptive bag of words will be increased by one else the word will be added to the deceptive/truthful bag. We are removing words with fewer than 20 count values. Using both truthful and deceptive words, we are calculating the total cumulative frequency and probability of each word in both bags.  After reading the test data, we make a list of each comment. Every comment is iterated again, and punctuation and numbers are removed, along with each character being converted to lowercase. Then splitting comments into tokens . In our calculations, we use the initial probability of a comment being truthful or deceptive as the prior probability. We traverse through each token and check if it is a stop word then we skip otherwise check if it is present in the truthful/deceptive bag of words. If it is present, we are multiplying the probability of words given the comment is truthful. We repeat the same procedure for deceptive as well. We check for the greater probability, append that value to the list and return this list at the end.

### Challenges:

Increasing the accuracy of the model was the key challenge in this problem. Several techniques were used to overcome this challenge, including using log to get the probability and cleaning the data by removing figures, punctuation, etc. As a result, accuracy increased from 70% to 82.75 percent.



## References:

1) https://www.youtube.com/watch?v=ptUXxWumxfE
2) https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
3) https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.68.9918&rep=rep1&type=pdf
4) https://towardsdatascience.com/beating-the-world-record-in-tetris-gb-with-genetics-algorithm-6c0b2f5ace9b
