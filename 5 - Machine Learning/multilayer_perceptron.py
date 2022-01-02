# multilayer_perceptron.py: Machine learning implementation of a Multilayer Perceptron classifier from scratch.
#
# Submitted by: [enter your full name here] -- [enter your IU username here]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

import numpy as np
from utils import identity, sigmoid, tanh, relu, softmax, cross_entropy, one_hot_encoding


class MultilayerPerceptron:
    """
    A class representing the machine learning implementation of a Multilayer Perceptron classifier from scratch.

    Attributes:
        n_hidden
            An integer representing the number of neurons in the one hidden layer of the neural network.

        hidden_activation
            A string representing the activation function of the hidden layer. The possible options are
            {'identity', 'sigmoid', 'tanh', 'relu'}.

        n_iterations
            An integer representing the number of gradient descent iterations performed by the fit(X, y) method.

        learning_rate
            A float representing the learning rate used when updating neural network weights during gradient descent.

        _output_activation
            An attribute representing the activation function of the output layer. This is set to the softmax function
            defined in utils.py.

        _loss_function
            An attribute representing the loss function used to compute the loss for each iteration. This is set to the
            cross_entropy function defined in utils.py.

        _loss_history
            A Python list of floats representing the history of the loss function for every 20 iterations that the
            algorithm runs for. The first index of the list is the loss function computed at iteration 0, the second
            index is the loss function computed at iteration 20, and so on and so forth. Once all the iterations are
            complete, the _loss_history list should have length n_iterations / 20.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model. This
            is set in the _initialize(X, y) method.

        _y
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.

        _h_weights
            A numpy array of shape (n_features, n_hidden) representing the weights applied between the input layer
            features and the hidden layer neurons.

        _h_bias
            A numpy array of shape (1, n_hidden) representing the weights applied between the input layer bias term
            and the hidden layer neurons.

        _o_weights
            A numpy array of shape (n_hidden, n_outputs) representing the weights applied between the hidden layer
            neurons and the output layer neurons.

        _o_bias
            A numpy array of shape (1, n_outputs) representing the weights applied between the hidden layer bias term
            neuron and the output layer neurons.

    Methods:
        _initialize(X, y)
            Function called at the beginning of fit(X, y) that performs one-hot encoding for the target class values and
            initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_hidden = 16, hidden_activation = 'sigmoid', n_iterations = 1000, learning_rate = 0.01):
        # Create a dictionary linking the hidden_activation strings to the functions defined in utils.py
        activation_functions = {'identity': identity, 'sigmoid': sigmoid, 'tanh': tanh, 'relu': relu}

        # Check if the provided arguments are valid
        if not isinstance(n_hidden, int) \
                or hidden_activation not in activation_functions \
                or not isinstance(n_iterations, int) \
                or not isinstance(learning_rate, float):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the MultilayerPerceptron model object
        self.n_hidden = n_hidden
        self.hidden_activation = activation_functions[hidden_activation]
        self.n_iterations = n_iterations
        self.learning_rate = learning_rate
        self._output_activation = softmax
        self._loss_function = cross_entropy
        self._loss_history = []
        self._X = None
        self._y = None
        self._h_weights = None
        self._h_bias = None
        self._o_weights = None
        self._o_bias = None

    def _initialize(self, X, y):
        """
        Function called at the beginning of fit(X, y) that performs one hot encoding for the target class values and
        initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._y = one_hot_encoding(y)

        #Initializing random weights and bias for input and output layers
        self._h_weights = np.random.random((len(X[0]), self.n_hidden))
        self._h_bias = np.random.random((1 * self.n_hidden))
        self._o_weights = np.random.random((self.n_hidden, len(self._y[0]), ))
        self._o_bias = np.random.random((1, len(self._y[0])))

        np.random.seed(42)

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y and stores the cross-entropy loss every 20
        iterations.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._initialize(X, y)

        #Iterating through given number of iteration value
        for i in range(self.n_iterations):

            #Initializing a matrix that stores the product of X and h_weights matrices
            matrix_1 = np.dot(self._X, self._h_weights)
            #Adding h_bias to the above matrix
            matrix_1 += self._h_bias

            #Applying activation function of the hidden layer
            matrix_2 = self.hidden_activation(matrix_1)
            #Initializing a matrix that stores the product of matrix_2 and o_weights matrices
            matrix_2 = np.dot(matrix_2, self._o_weights)
            #Adding o_bias to the above matrix
            matrix_2 += self._o_bias

            #Using the gradient descent formulas to calculate backpropagation errors for o_weights and o_bias
            dZ2 = matrix_2 - self._y
            dW2 = (1/len(self._X[0])) * (np.dot(self.hidden_activation(matrix_1).T, dZ2))
            db2 = (1/len(self._X[0])) * (np.sum(dZ2, axis = 0, keepdims = True))

            #Adjusting weight and bias of otput layer according to weight and bias error
            self._o_weights -= (dW2 * self.learning_rate)
            self._o_bias -= (db2 * self.learning_rate)

            #Calculation on loss history after every 20 iterations
            if i%20 == 0:
                self._loss_history.append(self._loss_function(self._output_activation(matrix_2), self._y))

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        max_prob = []

        for i in range(len(X)):
            #Initializing a matrix that stores the product of X and h_weights matrices
            matrix_1 = np.dot(self._X, self._h_weights)
            #Adding h_bias to the above matrix
            matrix_1 += self._h_bias

            #Applying activation function of the hidden layer
            matrix_2 = self.hidden_activation(matrix_1)
            #Initializing a matrix that stores the product of matrix_2 and o_weights matrices
            matrix_2 = np.dot(matrix_2, self._o_weights)
            #Adding o_bias to the above matrix
            matrix_2 += self._o_bias

            #Turning the output to positive probabilities by applying output layer activation function i.e. softmax 
            probs = self._output_activation(matrix_2)
            max_prob.append(np.argmax(probs))

        #Returning the maximum probabilty calculated
        return max_prob
