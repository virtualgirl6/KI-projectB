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



    def trainAndTune2(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        bestWeights = {}
        bestAccuracy = None
        for c in Cgrid:
            weights = self.weights.copy()
            for n in range(self.max_iterations):
                for i, datum in enumerate(trainingData):
                    # Try to guess the label
                    bestScore = None
                    bestY = None
                    for y in self.legalLabels:
                        score = datum * weights[y]
                        if score > bestScore or bestScore is None:
                            bestScore = score
                            bestY = y

                    actualY = trainingLabels[i]
                    if bestY != actualY:
                        # Wrong guess, update weights
                        f = datum.copy()
                        tau = min(c, ((weights[bestY] - weights[actualY]) * f + 1.0) / (2.0 * (f * f)))
                        f.divideAll(1.0 / tau)

                        weights[actualY] = weights[actualY] + f
                        weights[bestY] = weights[bestY] - f

            # Check the accuracy associated with this c
            correct = 0
            guesses = self.classify(validationData)
            for i, guess in enumerate(guesses):
                correct += (validationLabels[i] == guess and 1.0 or 0.0)
            accuracy = correct / len(guesses)

            if accuracy > bestAccuracy or bestAccuracy is None:
                bestAccuracy = accuracy
                bestWeights = weights

        self.weights = bestWeights

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"

        trainWeights = self.weights
        bestWeights = {}
        bestAccuracy = None
        c = Cgrid[2]
        for i in range(self.max_iterations):
            for j in range(len(trainingData)):

                datum = trainingData[j]
                vector = util.Counter()

                for label in self.legalLabels:
                    vector[label] = trainWeights[label] * datum #score

                wy = trainWeights[vector.argMax()]
                wyp = trainWeights[trainingLabels[j]]

                tau = min(c,((wyp - wy) * datum + 1.0) / ( 2 * (datum * datum)))

                tempDatum = datum.copy()

                for d in tempDatum:
                    tempDatum[d] *= tau

                if wy != wyp:
                    wyp += tempDatum
                    wy -= tempDatum

        correct = 0
        guesses = self.classify(validationData)
        for i, guess in enumerate(guesses):
            correct += (validationLabels[i] == guess and 1.0 or 0.0)
        accuracy = correct / len(guesses)

        if accuracy > bestAccuracy or bestAccuracy is None:
            bestAccuracy = accuracy
            bestWeights = trainWeights

        self.weights = bestWeights







    def trainAndTune1(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()



        for iteration in range (self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for c in Cgrid:
                for i in range(len(trainingData)):
                    datum = trainingData[i]
                    #print(datum)
                    vectors = util.Counter()

                    for label in self.legalLabels:
                        vectors[label] = self.weights[label] * datum
                        #print(self.legalLabels)

                        wy = self.weights[trainingLabels[i]] #= datum
                        wyprime = self.weights[vectors.argMax()]

                        tau = ((wyprime - wy) * datum + 1) / ( 2 * (datum * datum))

                        if (tau < c):
                            if wy != wyprime: #?
                                tau = 1
                                datum.divideAll(1.0 / tau)
                                wy = wy +  datum
                                wyprime = wyprime -  datum
                                print(wy)
                                print(wyprime)
                # max C ophalen
                #datum is counter, moeten value gebruiken? oid
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
