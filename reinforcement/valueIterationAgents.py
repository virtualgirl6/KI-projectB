# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)[((0, 1), 0.0), ((0, 2), 1.0)] lijst met node waarnaartoe + kans er te komen.
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        
        # initalization; creates a MDP, discount factor, number of itarations and a Counter dictionary in which all values are 0 by default.
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() 

        #for the specified number of iterations in self.iterations we:
        # first copy the values in tempValues so we can access the old values while updating the new values
        # for each statein the model we:
        #   check if its a terminal state(if so value = 0)
        #   Else update the value according to V_k+1(state) =  T(state,action,nextState) * (R(state,actionnextState) + discount * V_k(nextState))
        for i in range(self.iterations):
            tempValues = self.values.copy()
            for state in mdp.getStates():
                if not mdp.isTerminal(state):
                    tempMaxAction = util.Counter()
                    for action in mdp.getPossibleActions(state):
                        for nextState, prob in mdp.getTransitionStatesAndProbs(state, action):
                            tempMaxAction[action] += prob * (mdp.getReward(state, action, nextState) + self.discount * self.values[nextState]) 
                    tempValues[state] = tempMaxAction[tempMaxAction.argMax()]      
                else:
                    tempValues[state] = 0
            self.values = tempValues

 

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        # self.values stores the values for each state we can simply acces it by looking it up in the Counter
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # compute the Q-value where Q(state,action) = max_a{sum_nextStates T(state,action,nextState) * (R(state,action,nextState) + discount * V_k(nextState))}
        # note: if self.mdp.getTransitionStatesAndProbs(state, action) is empty, then Qvalue = 0
        Qvalue = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            Qvalue += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
        return Qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #returns the best action available
        #in the case the state is a terminal state this is None
        #else we compute the Qvalues for the available actions and return the action which correspondes with the highest Qvalue
        if self.mdp.isTerminal(state):
            return None 
        else:
            tempMaxAction = util.Counter()
            for action in self.mdp.getPossibleActions(state):
                for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    tempMaxAction[action] += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState]) 
            return tempMaxAction.argMax() 

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
