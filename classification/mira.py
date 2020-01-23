# mira.py
# -------
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


# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)


    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """

        bestWeight = {}
        bestAccuracy = 0
        #print("max iter: ", self.max_iterations, "len trainingdata: ", len(trainingData))
        for c in Cgrid:
            tempWeight = self.weights.copy()
            tempAccuracy = 0

            for i in range(self.max_iterations):
                for j in range(len(trainingData)):

                    datum = trainingData[j]
                    vector = util.Counter()

                    for label in self.legalLabels:
                        vector[label] = tempWeight[label] * datum 

                    
                    wy = tempWeight[vector.argMax()]
                    wyp = tempWeight[trainingLabels[j]]

                    tau = min(c,((wyp - wy) * datum + 1.0) / ( 2 * (datum * datum)))

                    tempDatum = datum.copy()

                    for d in tempDatum:
                        tempDatum[d] *= tau

                    if vector.argMax() != trainingLabels[j]:
                        tempWeight[trainingLabels[j]] += tempDatum
                        tempWeight[vector.argMax()] -= tempDatum
            #hier nieuwe weight getraind
            
            guesses = self.classifyGivenWeight(validationData, tempWeight)
            correct = [guesses[i] == validationLabels[i] for i in range(len(validationLabels))].count(True)
            #print(" hier gaat het om: ", 100.0 * correct / len(validationLabels))
            tempAccuracy = 100.0 * correct / len(validationLabels)
            print("c: ", c, "tempAcc: ", tempAccuracy, " bestAcc: ", bestAccuracy)
            if tempAccuracy > bestAccuracy:
                bestAccuracy = tempAccuracy
                bestWeight = tempWeight

        self.weights = bestWeight

    def classifyGivenWeight(self, data, givenWeight ):
        """
        Classifies each datum for a given weight, used to compare differenct weights with eachother
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = givenWeight[l] * datum
            guesses.append(vectors.argMax())
        return guesses

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses

    def findHighWeightFeatures(self, label):
        """
        Returns a list of the 100 features with the greatest weight for some label
        """
        featuresWeights = self.weights[label].sortedKeys()[:100]
        return featuresWeights
