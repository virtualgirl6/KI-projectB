# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())            
    """
    from util import Stack

    # On initialization creates stack for the open list, 
    # a set for seen states 
    # and list which will contain the actions corresponding to the state it belongs to.
    dfsStack = Stack() 
    geheugen = set()
    actions = []



    # We add the startstate to the memory and push the neighbouring states,
    # as a (state, action) tuple on the dfsStack, ready to be processed.
    geheugen.add(problem.getStartState())
    for node in problem.getSuccessors(problem.getStartState()):
        dfsStack.push((node, actions[:]))                            

    # While the dfsStack is not empty:
    #   - we will pop a state from the stack
    #   - add it to the memory 
    #   - add the corresponding direction the the action list of the state being processed
    #   - check if the current state is a goal state, if so return the action list
    #   - add the succesor nodes to the dfsStack if we havent seen them yet
    # if the stack is empty and we havent found the goals state returns None
    while not dfsStack.isEmpty():
        current_Node = dfsStack.pop()
        geheugen.add(current_Node[0][0]) 
        current_Node[1].append(current_Node[0][1]) 
        
        if problem.isGoalState(current_Node[0][0]): 
            return current_Node[1]                 

        for x in problem.getSuccessors(current_Node[0][0]):
            if x[0] not in geheugen:
                dfsStack.push((x, current_Node[1][:]))

    return None

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    from util import Queue

    # On initialization creates Queue for the open list,
    # a set for seen states
    # and list which will contain the actions corresponding to the state it belongs to.
    bfsQueue = Queue()
    geheugen = set()
    actions = []

    # We add the startstate to the memory and push the neighbouring states
    # as a (state, action) tuple on the bfsQueue and adding them to the memory.
    geheugen.add(problem.getStartState())
    for node in problem.getSuccessors(problem.getStartState()):
        geheugen.add(node[0])
        bfsQueue.push((node, actions[:]))

    # While the bfsQueue is not empty:
    #   - we will pop a state from the Queue
    #   - add the corresponding direction the the action list of the state being processed
    #   - check if the current state is a goal state, if so return the action list
    #   - add the succesor nodes to the bfsQueue if we havent seen them yet
    #   - and add it to the memory 
    # if the queue is empty and we havent found the goals state returns None
    while not bfsQueue.isEmpty():
        current_Node = bfsQueue.pop()
        current_Node[1].append(current_Node[0][1])

        if problem.isGoalState(current_Node[0][0]):
            return current_Node[1]

        for x in problem.getSuccessors(current_Node[0][0]):
            if x[0] not in geheugen:
                geheugen.add(x[0])
                bfsQueue.push((x, current_Node[1][:]))
    return None


def uniformCostSearch(problem):
    """Search the node of least total cost first.
    """
    from util import PriorityQueue

    # On initialization creates PriorityQueue for the open list, 
    # a dictionary where we keep track of the seen states and the cost for reaching the states
    # and list which will contain the actions corresponding to the state it belongs to.
    ucsQueue = PriorityQueue()
    geheugen = dict()
    actions = []

    # Set the cost of the startstate to 0
    # for each succesor state we:
    #   - push the state in the uscQueue based on the cost to reach it
    #   - add the node to the memory with the corresponding cost
    geheugen[problem.getStartState()] = 0
    for node in problem.getSuccessors(problem.getStartState()):
        ucsQueue.push((node, actions[:]), node[2])
        geheugen[node[0]] = node[2]
    
    # While the uscQueue is not empty:
    #   - we will pop a state from the Queue
    #   - add the corresponding direction the the action list of the state being processed
    #   - check if the current state is a goal state, if so return the action list
    #   - for the succesor states:
    #       - compute the cost to reach the state
    #       - if we havent seen the state yet add it to the memory
    #       - else if the succesor we are looking at is cheaper to reach via this path then update the memory
    # if the queue is empty and we havent found the goals state returns None
    while not ucsQueue.isEmpty():
        current_Node = ucsQueue.pop()
        current_Node[1].append(current_Node[0][1])

        if problem.isGoalState(current_Node[0][0]):
            return current_Node[1]

        for node in problem.getSuccessors(current_Node[0][0]):
            costSoFar = geheugen[current_Node[0][0]] + node[2]
            if node[0] not in (geheugen):
                ucsQueue.push((node, current_Node[1][:]), costSoFar)
                geheugen[node[0]] = costSoFar
            elif geheugen[node[0]] > costSoFar:
                ucsQueue.push((node, current_Node[1][:]), costSoFar)
                geheugen[node[0]] = costSoFar
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    from util import PriorityQueue

    # On initialization creates PriorityQueue for the open list, 
    # a dictionary where we keep track of the seen states and the cost for reaching the states
    # and list which will contain the actions corresponding to the state it belongs to.
    aStarQueue = PriorityQueue()
    geheugen = dict()
    actions = []

    # Set the cost of the startstate to 0
    # for each succesor state we:
    #   - push the state in the aStarQueue based on the cost to reach it but this time with the added heuristic costs
    #   - add the node to the memory with the corresponding cost
    geheugen[problem.getStartState()] = 0
    for node in problem.getSuccessors(problem.getStartState()):
        aStarQueue.push((node, actions[:]), node[2] + heuristic(node[0], problem) )
        geheugen[node[0]] = node[2]


    # While the aStarQueue is not empty:
    #   - we will pop a state from the Queue
    #   - add the corresponding direction the the action list of the state being processed
    #   - check if the current state is a goal state, if so return the action list
    #   - for the succesor states:
    #       - compute the cost to reach the state
    #       - if we havent seen the state yet add it to the memory and push it in the queue based on cost(=pathcosts + heuristic)
    #       - else if the succesor we are looking at is cheaper to reach via this path then update the memory and push it on the queue
    # if the queue is empty and we havent found the goals state returns None
    while not aStarQueue.isEmpty():
        current_Node = aStarQueue.pop()
        current_Node[1].append(current_Node[0][1])

        if problem.isGoalState(current_Node[0][0]):
            return current_Node[1]

        for node in problem.getSuccessors(current_Node[0][0]):
            costSoFar = geheugen[current_Node[0][0]] + node[2]
            if node[0] not in (geheugen):
                aStarQueue.push((node, current_Node[1][:]), costSoFar + heuristic(node[0], problem))
                geheugen[node[0]] = costSoFar 
            elif geheugen[node[0]] > costSoFar:
                aStarQueue.push((node, current_Node[1][:]), costSoFar + heuristic(node[0], problem))
                geheugen[node[0]] = costSoFar 
    return None



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
