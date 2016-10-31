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
        "*** YOUR CODE HERE ***"
        distancesToGhosts = [manhattanDistance(ghostState.configuration.getPosition(), newPos) for ghostState in newGhostStates]
        fooddistances = []
        foodnum = 0
        score = 0
        for i in range(newFood.width):
          for j in range(newFood.height):
            if(newFood[i][j]):
              foodnum+=1
              fooddistances.append(manhattanDistance((i,j),newPos))
        if foodnum==0:
            score = 100000
        else:
          if newScaredTimes[0]>0:
            score = 100000-foodnum-min(fooddistances)-2*min(distancesToGhosts)
          else:
            if min(distancesToGhosts)<5:
              score = 50*min(distancesToGhosts)-min(fooddistances)-foodnum*3
            else:
              score = 10000-foodnum*100-min(fooddistances)
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    distancesToGhosts = [manhattanDistance(ghostState.configuration.getPosition(), newPos) for ghostState in newGhostStates]
    fooddistances = []
    foodnum = 0
    score = 0
    for i in range(newFood.width):
      for j in range(newFood.height):
        if(newFood[i][j]):
          foodnum+=1
          fooddistances.append(manhattanDistance((i,j),newPos))
    if foodnum==0:
        score = 100000
    else:
      if newScaredTimes[0]>0:
        score = 100000-foodnum-min(fooddistances)-2*min(distancesToGhosts)
      else:
        if min(distancesToGhosts)<5:
          score = 50*min(distancesToGhosts)-min(fooddistances)-foodnum*3
        else:
          score = 10000-foodnum*100-min(fooddistances)
    return score
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

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def mmax(self, gameState, depth, curdepth):
      globmax = -100000
      if depth==curdepth:
        return self.evaluationFunction(gameState)
      legalMoves = gameState.getLegalActions(0)
      if len(legalMoves)==0:
        return self.evaluationFunction(gameState)
      for action in legalMoves:
        cur = self.mmin(gameState.generateSuccessor(0,action), self.depth, curdepth, range(gameState.getNumAgents())[1:])
        if cur > globmax:
          globmax = cur
      return globmax
    def mmin(self, gameState, depth, curdepth, toevaluate):
      globmin = 100000
      if len(toevaluate)==1:
        legalMoves = gameState.getLegalActions(toevaluate[0])
        if len(legalMoves)==0:
          return self.evaluationFunction(gameState)
        for action in legalMoves:
         cur = self.mmax(gameState.generateSuccessor(toevaluate[0],action), self.depth, curdepth+1)
         if cur < globmin:
          globmin = cur
        return globmin
      else:
        legalMoves = gameState.getLegalActions(toevaluate[0])
        if len(legalMoves)==0:
          return self.evaluationFunction(gameState)
        for action in legalMoves:
          cur = self.mmin(gameState.generateSuccessor(toevaluate[0],action), self.depth, curdepth, toevaluate[1:])
          if cur<globmin:
            globmin = cur
        return globmin

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
      # Collect legal moves and successor states
      legalMoves = gameState.getLegalActions()
      # Choose one of the best actions
      scores = [self.mmin(gameState.generateSuccessor(0,action), self.depth, 0, range(gameState.getNumAgents())[1:]) for action in legalMoves]
      bestScore = max(scores)
      bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
      chosenIndex = random.choice(bestIndices) # Pick randomly among the best
      return legalMoves[chosenIndex]

class AlphaBetaAgent(MultiAgentSearchAgent):
    def mmax(self, gameState, depth, curdepth, alpha, beta):
      globmax = -100000
      if depth==curdepth:
        return self.evaluationFunction(gameState)
      legalMoves = gameState.getLegalActions(0)
      if len(legalMoves)==0:
        return self.evaluationFunction(gameState)
      for action in legalMoves:
        cur = self.mmin(gameState.generateSuccessor(0,action), self.depth, curdepth, range(gameState.getNumAgents())[1:], alpha, beta)
        if cur > globmax:
          globmax = cur
        if globmax > beta:
          return globmax
        if globmax > alpha:
          alpha = globmax
      return globmax
    def mmin(self, gameState, depth, curdepth, toevaluate, alpha, beta):
      globmin = 100000
      if len(toevaluate)==1:
        legalMoves = gameState.getLegalActions(toevaluate[0])
        if len(legalMoves)==0:
          return self.evaluationFunction(gameState)
        for action in legalMoves:
          cur = self.mmax(gameState.generateSuccessor(toevaluate[0],action), self.depth, curdepth+1, alpha, beta)
          if cur < globmin:
            globmin = cur
          if globmin < alpha:
            return globmin
          if globmin < beta:
            beta = globmin
        return globmin
      else:
        legalMoves = gameState.getLegalActions(toevaluate[0])
        if len(legalMoves)==0:
          return self.evaluationFunction(gameState)
        for action in legalMoves:
          cur = self.mmin(gameState.generateSuccessor(toevaluate[0],action), self.depth, curdepth, toevaluate[1:], alpha, beta)
          if cur<globmin:
            globmin = cur
          if globmin < alpha:
            return globmin
          if globmin < beta:
            beta = globmin
        return globmin
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
      alpha = -100000
      beta = 100000
      curdepth = 0
      depth = self.depth
      globmax = -100000
      if depth==curdepth:
        return self.evaluationFunction(gameState)
      legalMoves = gameState.getLegalActions(0)
      if len(legalMoves)==0:
        return self.evaluationFunction(gameState)
      totake = legalMoves[0]
      for action in legalMoves:
        cur = self.mmin(gameState.generateSuccessor(0,action), self.depth, curdepth, range(gameState.getNumAgents())[1:], alpha, beta)
        if cur > globmax:
          globmax = cur
          totake = action
        if globmax > beta:
          return globmax
        if globmax > alpha:
          alpha = globmax
      return totake

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def mmax(self, gameState, depth, curdepth):
      globmax = -100000
      if depth==curdepth:
        return self.evaluationFunction(gameState)
      legalMoves = gameState.getLegalActions(0)
      if len(legalMoves)==0:
        return self.evaluationFunction(gameState)
      for action in legalMoves:
        cur = self.mmin(gameState.generateSuccessor(0,action), self.depth, curdepth, range(gameState.getNumAgents())[1:])
        if cur > globmax:
          globmax = cur
      return globmax
    def mmin(self, gameState, depth, curdepth, toevaluate):
      globmin = 100000
      if len(toevaluate)==1:
        legalMoves = gameState.getLegalActions(toevaluate[0])
        if len(legalMoves)==0:
          return self.evaluationFunction(gameState)
        total = 0
        number = 0
        for action in legalMoves:
         total += self.mmax(gameState.generateSuccessor(toevaluate[0],action), self.depth, curdepth+1)
         number+=1
        return total/number
      else:
        legalMoves = gameState.getLegalActions(toevaluate[0])
        if len(legalMoves)==0:
          return self.evaluationFunction(gameState)
        total = 0
        number = 0
        for action in legalMoves:
          total += self.mmin(gameState.generateSuccessor(toevaluate[0],action), self.depth, curdepth, toevaluate[1:])
          number += 1
        return total/number
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # Choose one of the best actions
        scores = [self.mmin(gameState.generateSuccessor(0,action), self.depth, 0, range(gameState.getNumAgents())[1:]) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        return legalMoves[chosenIndex]
caneat = False
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    global caneat
    newPos = currentGameState.getPacmanPosition()
    (x,y) = newPos
    if (x in {7,8,9,10,11,12}) and (y in {4,5}):
      return -99999999
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    distancesToGhosts = [manhattanDistance(ghostState.configuration.getPosition(), newPos) for ghostState in newGhostStates]
    fooddistances = []
    foodnum = 0
    score = 0
    for i in range(newFood.width):
      for j in range(newFood.height):
        if(newFood[i][j]):
          foodnum+=1
          fooddistances.append(manhattanDistance((i,j),newPos))
    if foodnum==0:
        score = 999999999999
    else:
      if newScaredTimes[0]>0:
        if min(distancesToGhosts)<=2:
          caneat = True
        score = 1000000-foodnum-min(fooddistances)-10*min(distancesToGhosts)
      else:
        if caneat == True:
          caneat = False
          return 999000000
        if min(distancesToGhosts)<3:
          score = 50*min(distancesToGhosts)-min(fooddistances)-foodnum*3
        else:
          score = 10000-foodnum*100-min(fooddistances)
    return score

    
# Abbreviation
better = betterEvaluationFunction

