import numpy as np
import math
import time
from game import Game
from minimax import minimax, minValue, maxValue
from minimaxDepthLimit import minimaxDepth, minValueDepth, maxValueDepth
from alphabeta import alphaBeta, minValueAB, maxValueAB
from alphabetaDepthLimit import alphaBetaDepth, minValueABDepth, maxValueABDepth
from alphabetaHeuristic import alphaBetaDepthHeuristic, minValueABDepthHeuristic, maxValueABDepthHeuristic

from gui import getWinner
import random
random.seed(time.time())

if __name__ == "__main__":
    gameCount = 100000
    gameSize = 3
    maxDepth = 3

    heuristicWins = 0
    noHeuristicWins = 0
    ties = 0
    for i in range(gameCount):
        tictactoe = Game(gameSize)

        while not(tictactoe.isTerminal(tictactoe.board)):
        
            aiActionAB = alphaBetaDepthHeuristic(tictactoe, tictactoe.board, 1, 1, maxDepth)
            
            tictactoe.board = tictactoe.result(tictactoe.board, aiActionAB, 1)

            if (tictactoe.isTerminal(tictactoe.board)):
                break

            aiActionRand = random.choice(tictactoe.getActions(tictactoe.board))
            #aiActionAB = alphaBetaDepth(tictactoe, tictactoe.board, 2, 1, 5)
            
            tictactoe.board = tictactoe.result(tictactoe.board, aiActionRand, 2)

        winner = getWinner(tictactoe)
        if winner == 0:
            ties += 1
        elif winner == 1:
            heuristicWins += 1
        else:
            noHeuristicWins += 1

        #tictactoe.display()
        #print()
    
    print("Heuristic Wins:", heuristicWins)
    print("Random Wins:", noHeuristicWins)
    print("Ties:", ties)

    print("---------------------------------------------------")

    heuristicWins = 0
    noHeuristicWins = 0
    ties = 0
    for i in range(gameCount):
        tictactoe = Game(gameSize)

        while not(tictactoe.isTerminal(tictactoe.board)):
        
            aiActionAB = alphaBetaDepth(tictactoe, tictactoe.board, 1, 1, maxDepth)
            
            tictactoe.board = tictactoe.result(tictactoe.board, aiActionAB, 1)

            if (tictactoe.isTerminal(tictactoe.board)):
                break

            aiActionRand = random.choice(tictactoe.getActions(tictactoe.board))
            #aiActionAB = alphaBetaDepth(tictactoe, tictactoe.board, 2, 1, 5)
            
            tictactoe.board = tictactoe.result(tictactoe.board, aiActionRand, 2)

        winner = getWinner(tictactoe)
        if winner == 0:
            ties += 1
        elif winner == 1:
            heuristicWins += 1
        else:
            noHeuristicWins += 1

        #tictactoe.display()
        #print()
    
    print("No Heuristic Wins:", heuristicWins)
    print("Random Wins:", noHeuristicWins)
    print("Ties:", ties)