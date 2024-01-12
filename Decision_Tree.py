"""
Decision Tree Implementation

This script is my own implementation of a Decision Tree. It's created to enhance my understanding of how Decision Trees work. 

Credit: 
    Inspired by "Normalized Nerd" for foundational understanding.
    This implementation is an acknowledgement of the insights gained from their material, aiming to apply and solidify my knowledge of Decision Trees in a practical manner.


Note: This is an educational implementation and may not reflect the performance optimizations of professional machine learning libraries.
"""

import numpy as np
import pandas as pd


class Node(): 
    def __init__(self, feature_index = None, treshold = None, left = None, right = None, gain = None, value = None) -> None:
        #if node is a decision node (middle of the tree)
        self.feature_index  = feature_index
        self.treshold       = treshold
        self.left           = left
        self.right          = right
        self.gain           = gain

        #if node is a leaf node (end of the tree)
        self.value = value

class DecisionTree(): 
    def __init__(self, min_split, max_depth) -> None:
        #This is done to avoid overfitting
        self.min_split = min_split
        self.max_depth = max_depth

        #initialize the root node of the tree 
        #This is necessary to traverse through the tree
        self.root = None

    def buildTree(self, data, curr_depth = 0) -> Node: 
        """
        This assumes data is a pd dataset with the following properties: 
            Last column being the Y values (in this case the difficulty)
            All other columns contain the features (in this case word length, frequency of letters, etc...)
        """
        X,Y = data[:,:-1], data[:,-1]

        #This gives us the Number of samples (Number of games) and the Number of features (How many criteria we are judging our words by)
        num_samples, num_features = np.shape(X)

        #We now start building the tree recursively

        #check for stopping conditions
        if num_features > self.min_split and curr_depth < self.max_depth: 
             
            split_data = self.find_best_split(data, num_features)

            if split_data["info gain"] != 0: #if not leaf node
                #recur left and right
                left_tree  = self.buildTree(split_data["left data"], curr_depth + 1)
                right_tree = self.buildTree(split_data["right data"], curr_depth + 1)

                #return subTree
                return Node(split_data["feature_index"], split_data["treshold"], left_tree, right_tree, split_data["info gain"])
            
        value = self.get_leaf_value(Y)
        return Node(value=value)
    
    def find_best_split(self, data, num_features) -> dict: 
        """
        This functions finds the optimal possible split for the Decision Tree
        It performs most of the theoritical ideas behind Decision Trees
        
        Note: 
        In this case, I am using Gini index instead of Entropy in order to save computation cost (log can be expensive to compute        
        """

        #Note: Since max info gain is always a positive number, we could initiliaze it as -1
        max_info_gain = -float("inf")

        best_split = dict() 

        for feature_index in num_features: 
            #find all unique values for specific value
            feature_values = data[:,feature_index]
            possible_tresholds = np.unique(feature_values)

            #loop trough all possible tresholds to find the optimal one
            for treshold in possible_tresholds: 
                left, right = self.split(data, treshold)
                
                #check if children datasets are not null
                if left and right:
                    #value in this case represents the difficulty
                    values, left_values, right_values = data[:,-1], left[:,-1], right[:,-1]

                    info_gain = self.get_info_gain(values, left_values, right_values)

                    if info_gain > max_info_gain: 
                        best_split["info gain"]     = info_gain
                        best_split["left data"]     = left
                        best_split["right data"]    = right
                        best_split["treshold"]      = treshold
                        best_split["feature index"] = feature_index

                        max_info_gain = info_gain
        
        return best_split

                    
    def split(self, data, treshold): 
        left = [x for x in data if x <= treshold]
        right = [x for x in data if x > treshold]

        return left, right

    def get_info_gain(self, values, left_values, right_values) -> int: 
        
        weight_l = len(left_values) / len(values)
        weight_r = len(right_values) / len(values)

        #using gini coefficients to save computation cost, could've used entropy for similar results
        gain = self.gini(values) - self.gini(left_values)*weight_l - self.gini(right_values)*weight_r
    
        return gain 
    
    
    @staticmethod
    def gini(values): 
        #returns the different types in our values (here the difficulties)
        types = np.unique(values)

        # iterates through all types, then takes the squared value of the type_frequency/number_of_values
         
        squrd_probas = [(len([y == tp for y in values]) / len(values)) ** 2 for tp in types]

        return 1 - sum(squrd_probas)
    
    def get_leaf_value(self, values): 
        #returns the most common element in the leaf node
        return max(values, key = values.count)
    
    def fit(self, X, Y): 
        ''' This is used to train the tree'''
        dataset = np.concatenate((X,Y), axis=1)
        self.root = self.buildTree(dataset)

    def predict(self, X): 
        '''This is used after training the tree'''
        
        predictions = [self.make_predictions(x, self.root) for x in X]
        return predictions
    
    def make_predictions(self, x, node): 
        '''Follows the path of the tree recursively to make a prediction'''   

        if node.value: return node.value
        feature_value = x[node.feature_index]
        if feature_value <= node.treshold: 
            return self.make_predictions(x, node.left)
        else: 
            return self.make_predictions(x, node.right)

