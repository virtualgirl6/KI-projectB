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
    -
    Start: (5, 5)
    Is the start a goal? False
    Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    successor: (nextState, action, cost)
    """
    "*** YOUR CODE HERE ***"

    from util import Stack

    dfsStack = Stack()
    geheugen = set()
    actions = []
    costs = 0

    #pusht de buren van de startstate, door deze eerst te pushen krijg je niet een 'loze' startstate in de actions list
    # daarnaast is (node, actions) een tuple waarbij actions een lijst met tot dan toe ondernomen stappen
    geheugen.add(problem.getStartState())
    for node in problem.getSuccessors(problem.getStartState()):
        dfsStack.push((node, actions[:]))

    #Zolang niet leeg worden een voor een de nodes gecheckt
    while not dfsStack.isEmpty():
        current_Node = dfsStack.pop()
        geheugen.add(current_Node[0][0])  #add node in geheugen nadat deze gepopt wordt (closed list) hierdoor wordt voorkomen dat je telkens een stap terug doet
        #print(current_Node[0][0])
        current_Node[1].append(current_Node[0][1]) # hier voeg je de richting toe waarin pacman loopt
        #print(current_Node[1])

        if problem.isGoalState(current_Node[0][0]): # als goal state --> stop
            #print(len(current_Node[1]))
            return current_Node[1]                  # nu hoeft simpelweg de actions hoe we in de node terecht gekomen zijn gereturnt te worden

        for x in problem.getSuccessors(current_Node[0][0]):
            if x[0] not in geheugen:
                dfsStack.push((x, current_Node[1][:]))

    return "No path available"


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from util import Queue
    bfsQueue = Queue()
    geheugen = set()
    actions = []
    costs = 0

    geheugen.add(problem.getStartState())
    for node in problem.getSuccessors(problem.getStartState()):
        geheugen.add(node[0])
        bfsQueue.push((node, actions[:]))


    while not bfsQueue.isEmpty():

        current_Node = bfsQueue.pop()


        current_Node[1].append(current_Node[0][1])

        if problem.isGoalState(current_Node[0][0]):
            return current_Node[1]


        for x in problem.getSuccessors(current_Node[0][0]):
            if x[0] not in geheugen:
                geheugen.add(x[0])
                bfsQueue.push((x, current_Node[1][:]))


    return "No path available"



def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    from util import PriorityQueue
    ucsQueue = PriorityQueue()
    geheugen = dict()
    actions = []

    geheugen[problem.getStartState()] = 0
    for node in problem.getSuccessors(problem.getStartState()):
        ucsQueue.push((node, actions[:]), node[2])
        geheugen[node[0]] = node[2]

    while not ucsQueue.isEmpty():

        current_Node = ucsQueue.pop()
        print(current_Node)
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

    return "No path available"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    from util import PriorityQueue
    aStarQueue = PriorityQueue()
    geheugen = dict()
    actions = []

    geheugen[problem.getStartState()] = 0
    for node in problem.getSuccessors(problem.getStartState()):
        aStarQueue.push((node, actions[:]), node[2] + heuristic(node[0], problem) )
        geheugen[node[0]] = node[2]

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

    return "No path available"

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
