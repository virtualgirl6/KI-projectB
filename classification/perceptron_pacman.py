# perceptron_pacman.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation for apprenticeship learning
import util
from perceptron import PerceptronClassifier
from pacman import GameState

PRINT = True


class PerceptronClassifierPacman(PerceptronClassifier):
    def __init__(self, legalLabels, maxIterations):
        PerceptronClassifier.__init__(self, legalLabels, maxIterations)
        self.weights = util.Counter()

    def classify(self, data ):
        """
        Data contains a list of (datum, legal moves)
        
        Datum is a Counter representing the features of each GameState.
        legalMoves is a list of legal moves for that GameState.
        """
        guesses = []
        for datum, legalMoves in data:
            vectors = util.Counter()
            for l in legalMoves:
                vectors[l] = self.weights * datum[l] #changed from datum to datum[l]
            guesses.append(vectors.argMax())
        return guesses


    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        """
        The training loop for the perceptron_pacman passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        """
        self.features = trainingData[0][0]['Stop'].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.

        # The model is updated max_iteration times for each iteration in range of max_iterations we go through the training data
        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(trainingData)):

                #split the training data in datum and legalmoves so we can update the weight vector
                datum, legalMoves = trainingData[i]
                vectors = util.Counter()

                # Compute updated weight vector using the curren training datum for each move using the weights * datum[move]
                for move in legalMoves:
                    vectors[move] = self.weights * datum[move]
                
                # Update self.weights if the current learned output label does not match the correct label
                if vectors.argMax() != trainingLabels[i]:
                    self.weights += datum[trainingLabels[i]]
                    self.weights -= datum[vectors.argMax()]