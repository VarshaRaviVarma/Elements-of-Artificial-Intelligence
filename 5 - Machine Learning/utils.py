# utils.py: Utility file for implementing helpful utility functions used by the ML algorithms.
#
# Submitted by: [enter your full name here] -- [enter your IU username here]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

import numpy as np
import copy
import math

def euclidean_distance(x1, x2):
    """
    Computes and returns the Euclidean distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    #Calculating euclidean distance using the formula
    euc_dist = np.sqrt(np.sum(np.square(x2-x1)))
    #Returning the calculated euclidean distance
    return euc_dist

def manhattan_distance(x1, x2):
    """
    Computes and returns the Manhattan distance between two vectors.

    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    man_dist = 0
    #Calculating manhattan distance using the formula
    for i in range(len(x1)):
        man_dist += abs(x1[i] - x2[i])
    #Returning the calculated manhattan distance
    return man_dist

def identity(x, derivative = False):
    """
    Computes and returns the identity activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    #Calculating the number of rows
    l1 = len(x)
    #Calculating the number of column
    l2 = len(x[0])
    #Calculating and returning the identity equation value
    if(derivative == False):
        return x
    #Calculating and returning the identity derivative value
    else:
        return np.ones([l1, l2])

def sigmoid(x, derivative = False):
    """
    Computes and returns the sigmoid (logistic) activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    #Deep copying the x value into a temperory variable
    temp = copy.deepcopy(x)
    #Calculating the number of rows
    l1 = len(temp)
    #Calculating the number of column
    l2 = len(temp[0])
    #Calculating and returning the sigmoid equation value
    if(derivative == False):
        for i in range(l1):
            for j in range(l2):
                temp[i][j] = 1 / (1 + np.exp(-temp[i][j]))
        return temp
    #Calculating and returning the sigmoid derivative value
    else:
        return sigmoid(x) * (1 - sigmoid(x))

def tanh(x, derivative = False):
    """
    Computes and returns the hyperbolic tangent activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    #Calculating and returning the tanh equation value
    if(derivative == False):
      return np.tanh(x)
    #Calculating and returning the tanh derivative value
    else:
        return 1 - (tanh(x) ** 2)

def relu(x, derivative = False):
    """
    Computes and returns the rectified linear unit activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.

    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    #Deep copying the x value into a temperory variable
    temp = copy.deepcopy(x)
    #Calculating the number of rows
    l1 = len(temp)
    #Calculating the number of column
    l2 = len(temp[0])
    #Calculating and returning the relu equation value
    if(derivative == False):
        for i in range(l1):
            for j in range(l2):
                if(x[i][j]<0):
                    temp[i][j] = 0
        return temp
    #Calculating and returning the relu derivative value
    else:
        for i in range(l1):
            for j in range(l2):
                if(x[i][j]<0):
                    temp[i][j] = 0
                elif(x[i][j]>=0):
                    temp[i][j] = 1
        return temp

def softmax(x, derivative = False):
    x = np.clip(x, -1e100, 1e100)
    if not derivative:
        c = np.max(x, axis = 1, keepdims = True)
        return np.exp(x - c - np.log(np.sum(np.exp(x - c), axis = 1, keepdims = True)))
    else:
        return softmax(x) * (1 - softmax(x))

def cross_entropy(y, p):
    """
    Computes and returns the cross-entropy loss, defined as the negative log-likelihood of a logistic model that returns
    p probabilities for its true class labels y.

    Args:
        y:
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.o
        p:
            A numpy array of shape (n_samples, n_outputs) representing the predicted probabilities from the softmax
            output activation function.
    """
    a = 0
    #Iterating through each row and column of y
    for i in range(len(y)):
        for j in range(len(y[0])):
            #Implementing cross entropy formula
            a += (y[i][j] * (math.log2(p[i][j])))
    #Returning the calculated cross entropy value
    return a

def one_hot_encoding(y):
    """
    Converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot
    encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the
    original data.

    Args:
        y: A numpy array of shape (n_samples,) representing the target class values for each sample in the input data.

    Returns:
        A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the input
        data. n_outputs is equal to the number of unique categorical class values in the numpy array y.
    """
    #Maintaing a list that contains all the unique categories
    y1 = list(set(y))
    #Maintaing a list that stores all the index value of y
    y_index = []
    #Maintaing a list that holds the value 1 for the belonging category
    y_index_sort = []
    #Appending the index value of y into y_index
    for i in range(len(y1)):
        y_index.append(i)
    #Forming a nested list that holds the category value for each value in y
    for i in range(len(y)):
        #Deep copying the y_index value into a temperory variable
        temp = copy.deepcopy(y_index)
        #Loop to iterate through temp variable of y_index
        for j in range(len(y1)):
            #Checking which category each element of y belongs to in y1
            if(y[i] == y1[j]):
                #If y belongs to the y1 category, we set the value at that index to 1
                temp[j] = 1
            #Checking if the element of y does not belong to the y1 category
            if(y[i] != y1[j]):
                #If y does not belongs to the y1 category, we set the value at that index to 0
                temp[j] = 0
        #Appending the temp list that holds the category value of 1 to y_index_sort
        y_index_sort.append(temp)
    #Returning the categorial value based nested list
    return y_index_sort
