# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        """
        print("successorGameState: {0}".format(successorGameState))
        print("newPos: {0}".format(newPos))
        print("newFood: {0}".format(newFood))
        print("newGhostStates: {0}".format(newGhostStates))
        print("newScaredTimes: {0}".format(newScaredTimes))
        print("action: {0}".format(action))
        """
        FOOD_WEIGHT = 1000
        GHOST_WEIGHT = 100000
        new_food_list = newFood.asList()
        food_distance_list = []
        ghost_position_list = []
        ghost_distance_list = []
        
        if currentGameState.getPacmanPosition() == newPos:
          return -999999

        for ghost in newGhostStates:
          ghost_position = ghost.getPosition()
          ghost_position_list.append(ghost_position)

        for food in new_food_list:
          food_distance_list.append(manhattanDistance(food, newPos))
        
        for ghost in ghost_position_list:
          ghost_distance_list.append(manhattanDistance(ghost, newPos))

        for distance in ghost_distance_list:
          if distance < 2:
            return -999999
          if len(food_distance_list) == 0:
            return 999999

        number_of_food_remaining = len(food_distance_list)
        sum_of_food_distances = sum(food_distance_list)
        """
        print("sum of food distances: {0}".format(sum_of_food_distances))
        print("len of food distance list: {0}".format(number_of_food_remaining))
        """

        eval = FOOD_WEIGHT/sum_of_food_distances + GHOST_WEIGHT/number_of_food_remaining
        #print("eval: {0}".format(eval))
        
        return eval

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


#NOEMI
class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        #start at pacman agent (0) at the first depth
        depth = 1
        agent = 0
        (action, val) = self.value(gameState, depth, agent)

        return action
 
    #helper function for max_value() and min_value()
    def nextAgent(self, gameState, agent):
      if agent == (gameState.getNumAgents() - 1): # all enemy has played, pacman has yet to go
        return 0 #return index of pacman
      else: #return index of next agent
        return 1 + agent
      
    #helper function for max_value() and min_value()
    def nextDepth(self, depth, agent):
      if agent == 0: #agent is pacman again 
        return depth + 1
      else:
        return depth

    #main recursive function
    def value(self, state, depth, current_agent):
  
      #base case 
      if depth > self.depth or state.isWin() or state.isLose():
        #print "value and pre establised depth are the same"
        value = self.evaluationFunction(state)
        return (None, value) #no future action at the leaf node 

      #recursive case
      if current_agent == 0: #pacman is playing
        return self.max_value(state, depth, current_agent)
      else:
        return self.min_value(state, depth, current_agent)
    
    #helper recursive function
    def max_value(self, state, depth, current_agent):
      bestValue = -99999
      bestAction = None

      #find best successor with highest value and return its action
      for action in state.getLegalActions(current_agent):
        successorState = state.generateSuccessor(current_agent, action)

        #call recursive function
        next_agent = self.nextAgent(state, current_agent)
        next_depth = self.nextDepth(depth, next_agent)
        (successorAction, successorValue) = self.value(successorState, next_depth, next_agent )

        #compare and choose next max
        if successorValue > bestValue:
          bestValue = successorValue
          bestAction = action #successorAction
    
      return (bestAction, bestValue)

    #helper recursive function
    def min_value(self, state, depth, current_agent):
      bestValue = 99999
      bestAction = None

      #find best successor with highest value and return its action
      for action in state.getLegalActions(current_agent):
        successorState = state.generateSuccessor(current_agent, action)

        #call recursive function
        next_agent = self.nextAgent(state, current_agent)
        next_depth = self.nextDepth(depth, next_agent)
        (successorAction, successorValue) = self.value(successorState, next_depth, next_agent )

        #compare and choose next min
        if successorValue < bestValue:
          bestValue = successorValue
          bestAction = action #successorAction
    
      return (bestAction, bestValue)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        #start at pacman agent (0) at the first depth
        depth = 1
        agent = 0
        alpha = -99999 #max's best option 
        beta = 99999   #min's best option
        (action, val, a, b) = self.value(gameState, depth, agent, alpha, beta)

        return action
 
    #helper function for max_value() and min_value()
    def nextAgent(self, gameState, agent):
      if agent == (gameState.getNumAgents() - 1): # all enemy has played, pacman has yet to go
        return 0 #return index of pacman
      else: #return index of next agent
        return 1 + agent
      
    #helper function for max_value() and min_value()
    def nextDepth(self, depth, agent):
      if agent == 0: #agent is pacman again 
        return depth + 1
      else:
        return depth

    #main recursive function
    def value(self, state, depth, current_agent, alpha, beta):

      #base case 
      if depth > self.depth or state.isWin() or state.isLose():
        value = self.evaluationFunction(state)
        return (None, value, -99999, 99999) 
        #no future action at the leaf node, no numbers for alpha or beta

      #recursive case
      if current_agent == 0: #pacman is playing
        return self.max_value(state, depth, current_agent, alpha, beta)
      else:
        return self.min_value(state, depth, current_agent, alpha, beta)
    
    #helper recursive function
    def max_value(self, state, depth, current_agent, alpha, beta):
      bestValue = -99999
      bestAction = None

      #find best successor with highest value and return its action
      for action in state.getLegalActions(current_agent):
        successorState = state.generateSuccessor(current_agent, action)

        #call recursive function
        next_agent = self.nextAgent(state, current_agent)
        next_depth = self.nextDepth(depth, next_agent)
        (successorAction, successorValue, successorAlpha, successorBeta) = self.value(successorState, next_depth, next_agent, alpha, beta )

        #compare and choose next max
        
        if successorValue > bestValue:
          bestValue = successorValue
          bestAction = action

        """
        v = max(v, value(successor, alpha, beta))
        if v >= beta return v
        alpha = max(alpha, v)
        
        bestValue = max(bestValue, successorValue, alpha, beta)
        if bestValue > beta:
          return (bestAction, bestValue, alpha, beta)
        
        alpha = max(alpha, bestValue)
        """
        #check against beta value 
        if bestValue > beta:
          return (bestAction, bestValue, alpha, beta)
        
        #uptate best alpha value 
        alpha = max(bestValue, alpha)

      return (bestAction, bestValue, alpha, beta)

    #helper recursive function
    def min_value(self, state, depth, current_agent, alpha, beta):
      bestValue = 99999
      bestAction = None

      #find best successor with highest value and return its action
      for action in state.getLegalActions(current_agent):
        successorState = state.generateSuccessor(current_agent, action)

        #call recursive function
        next_agent = self.nextAgent(state, current_agent)
        next_depth = self.nextDepth(depth, next_agent)
        (successorAction, successorValue, successorAlpha, successorBeta) = self.value(successorState, next_depth, next_agent, alpha, beta )

        #compare and choose next min
        if successorValue < bestValue:
          bestValue = successorValue
          bestAction = action 

        #check against alpha value
        if bestValue < alpha:
          return (bestAction, bestValue, alpha, beta)

        #uptate the best beta value
        beta = min(bestValue, beta)
    
      return (bestAction, bestValue, alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

