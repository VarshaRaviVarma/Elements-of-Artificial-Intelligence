# ASSIGNMENT 3

#### Name: Varsha Ravi Varma 
#### Mail ID: varavi@iu.edu	
#### IU ID: 2000751388
	   	


## PART 1:

Part 1 involves implementation of a k-nearest neighbors classifier from scratch.

### Observation:

There were 4 functions given in the skeleton code that we had to modify and implement the k-nearest neighbors classifier algorithm. The four functions are as follows:

Utility functions:

euclidean_distance - to calculate the euclidean distance between x1 and x2 which are two points in the given data.
manhattan_distance - to calculate the manhattan distance between x1 and x2 which are two points in the given data.

Main program functions:

fit - fits the model to the provided data matrix x and targets y.
predict - predicts the output of the given problem using the fitted classifier model.

### Approach and design decisions:

Firstly, I implemented the formula that calculates the euclidean and manhattan distance and returns the calculated value in their respective utility functions. Implementing the fit function for this problem was simple as I only had to assign x and y values in the following manner: self._x = x and self._y = y

Now for the most important function for this part of the assignment was the predict function. In this function, I initialize empty lists to store distance, category and predicted value of y. Then iterate through each point in test data and train data while appending the distance from each point in the training data. I sort the distance list that can be used to find the shortest distances. Then I iterate through the distance array upto n neighbors. I find the index value of data in the original list and find the category of the point from the training data and append that into the list. Sort all the unique categories in a set. Then check if the weight type is uniform, iterate through each category, count the occurrence of each category and update the max occurring category. If the weight is not uniform but is distance, then again iterate through each category, iterate through the distance list, check and update the max occurring category. Append all the predicted values of y and initialize distance and category lists to an empty list. Finally, return the predicted y.

### Challenges:

The main challenge was figuring out ways to increase the predicted accuracy of the code.



## PART 2:

Part 2 involves implementing a feedforward fully-connected multilayer perceptron classifier with one hidden layer from scratch.

### Observation:

There were 9 functions given in the skeleton code that I have to modify and implement a feedforward fully-connected multilayer perceptron classifier. Given functions are as follows:

Utility functions:

identity - computes and returns the identity activation function.
sigmoid - computes and returns the sigmoid activation function. 
tanh - computes and returns the tanh activation function.
relu - computes and returns the relu activation function.
cross_entropy - computes and returns the cross entropy value.
one_hot_encoding - converts a vector of categorical class values into a one-hot numeric array.

Main functions:

initialize - performs one-hot encoding.
fit - fits the to the provided data matrix x and targets y.
predict - predicts and returns the predicted output using the fitted classifier model.

### Approach and design decisions:

Firstly, I implemented the formula that calculates the activation functions and returns the calculated values for identity, sigmoid, tanh and relu. In the cross entropy function, I iterate through each row and column of y, calculate the cross entropy value using the formula and return that value. In one_hot_encoding, I initialize the list to hold the unique categories, store all the index values of y, etc. I append the index value of y, form a nested list that holds the category value for each value in y as 1. Append the temporary list that holds the category value of 1s and 0s to the nested list. Return the categorial value base nested list that holds the value 1 in the index of y that belongs to its specific category.

Now for the main functions in the initialize function, I initialize random weights and bias for the input and output layers as given in the skeleton code’s description. In the fit function, iterate through a given number of iteration values, initialize a matrix that stores the product value of X and h_weights and add that matrix with h_bias. Apply the activation function of the hidden layer and store it in the second matrix. The same has to be repeated again for the second matrix that holds the product value of that matrix and o_weights and then add o_bias to the same matrix. Using the gradient descent formulas to calculate the backpropagation errors for o_weights and o_bias. Then adjust the weight and bias of the output layer according to weight and bias error values.  Calculate loss history after every 20 iterations.

In the predict function, perform len(X) number of iterations and redo the matrix_1 and matrix_2 calculations that were performed in the fit function. Then turn the output to positive probabilities by applying the output layer activation function which is softmax. Return the maximum calculated probability.

### Challenges:

Implementing the fit function that gives optimal good accuracy results was a huge challenge. Finding implementation of backpropagation for this program very difficult.



## References:

1) https://towardsdatascience.com/activation-functions-neural-networks-1cbd9f8d91d6
2) https://www.dropbox.com/s/nfv5w68c6ocvjqf/0-2.pdf?dl=0 
