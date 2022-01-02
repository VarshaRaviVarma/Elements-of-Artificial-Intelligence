# k_nearest_neighbors.py: Machine learning implementation of a K-Nearest Neighbors classifier from scratch.
#
# Submitted by: [enter your full name here] -- [enter your IU username here]
#
# Based on skeleton code by CSCI-B 551 Fall 2021 Course Staff

import numpy as np
from utils import euclidean_distance, manhattan_distance
import copy


class KNearestNeighbors:
    """
    A class representing the machine learning implementation of a K-Nearest Neighbors classifier from scratch.

    Attributes:
        n_neighbors
            An integer representing the number of neighbors a sample is compared with when predicting target class
            values.

        weights
            A string representing the weight function used when predicting target class values. The possible options are
            {'uniform', 'distance'}.

        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model and
            predicting target class values.

        _y
            A numpy array of shape (n_samples,) representing the true class values for each sample in the input data
            used when fitting the model and predicting target class values.

        _distance
            An attribute representing which distance metric is used to calculate distances between samples. This is set
            when creating the object to either the euclidean_distance or manhattan_distance functions defined in
            utils.py based on what argument is passed into the metric parameter of the class.

    Methods:
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.

        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model.
    """

    def __init__(self, n_neighbors = 5, weights = 'uniform', metric = 'l2'):
        # Check if the provided arguments are valid
        if weights not in ['uniform', 'distance'] or metric not in ['l1', 'l2'] or not isinstance(n_neighbors, int):
            raise ValueError('The provided class parameter arguments are not recognized.')

        # Define and setup the attributes for the KNearestNeighbors model object
        self.n_neighbors = n_neighbors
        self.weights = weights
        self._X = None
        self._y = None
        self._distance = euclidean_distance if metric == 'l2' else manhattan_distance

    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.

        Returns:
            None.
        """
        self._X = X
        self._y = y

    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.

        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.

        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        #Initializing empty lists to store distance, category and prdicted value of y
        dist = []
        category = []
        predicted_y = []

        #Iterating through each point in test data
        for i in range(len(X)):
            #Iterating through each point in training data
            for j in range(len(self._X)):
                #Appending the distance from each point in the training data
                dist.append(self._distance(X[i],self._X[j]))

            temp = copy.deepcopy(dist)
            #Sorting the distance
            dist.sort()

            #Iterating through distance array upto n neighbors (n neighbors being the number of neighbors we want to compare and calculate the category)
            for k in range(0, self.n_neighbors):
                #Finding the index value of data in the original list
                index = temp.index(dist[k])
                #Finding category of the point from the training data and appending into the list
                category.append(self._y[index])

            #Storing all the unique categories in a set
            category_set = set(category)
            max_occ = 0
            index = -1
            
            #Checking if the weight type is uniform
            if(self.weights == 'uniform'):
                #Iterating through the each category
                for k in category_set:
                    #Counting the occurance of each category
                    cat_count = category.count(k)
                    #Checking and updating the max occuring category
                    if(max_occ < cat_count):
                        max_occ = cat_count
                        index = k
            #If the weight type is distance
            else:
                #Iterating through the each category
                for k in category_set:
                    cat_count = 0
                    #Iterating through the distance list upto n neighbors
                    for l in range(self.n_neighbors):
                        if(category[l]==k):
                            cat_count += 1/dist[l]
                    #Checking and updating the max occuring category
                    if(max_occ < cat_count):
                        max_occ = cat_count
                        index = k
            #Appending the predicted y's index value
            predicted_y.append(index)   
            #Re-initializing distance and category to empty lists     
            dist = []
            category = []
        #Returning the predicted y value
        return predicted_y
        
