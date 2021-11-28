import numpy as np
import math
import time
from game import Game
from minimax import minimax, minValue, maxValue
from minimaxDepthLimit import minimaxDepth, minValueDepth, maxValueDepth
from alphabeta import alphaBeta, minValueAB, maxValueAB
from alphabetaDepthLimit import alphaBetaDepth, minValueABDepth, maxValueABDepth
from alphabetaHeuristic import alphaBetaDepthHeuristic, minValueABDepthHeuristic, maxValueABDepthHeuristic

global se
se = 0

def minimaxSE(game, state, player):   
    (value, move) = maxValueSE(game, state, player)
    return move

def maxValueSE(game, state, player):
    # Check if board is in terminal state
    if game.isTerminal(state):
        global se
        se += 1
        return (game.utility(state, player), None)
    
    value = -math.inf # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValueSE(game, game.result(state, a, player), player)
        if v2 > value:
            value = v2
            move = a 
    return (value, move)

def minValueSE(game, state, player):
    oppositePlayers = {1:2, 2:1}
    #Checks if board is in terminal state
    if game.isTerminal(state):
        global se
        se += 1
        return (game.utility(state, player), None)

    actions = game.getActions(state)
    move = actions[0]
    value = math.inf # value = infinity
    for a in actions:
        v2, a2 = maxValueSE(game, game.result(state, a, oppositePlayers[player]), player)
        if v2 < value:
            value = v2
            move = a
    return (value, move)

def alphaBetaSE(game, state, player):
    (value, move) = maxValueABSE(game, state, player, -math.inf, math.inf)
    return move

def maxValueABSE(game, state, player, alpha, beta):
    # Check if board is in terminal state
    if game.isTerminal(state):
        global se
        se += 1
        return (game.utility(state, player), None)
    
    value = -math.inf # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValueABSE(game, game.result(state, a, player), player, alpha, beta)
        if v2 > value:
            value = v2
            move = a
            alpha = max(alpha, value)
        if value >= beta:
            return (value, move)
    return (value, move)

def minValueABSE(game, state, player, alpha, beta):
    oppositePlayers = {1:2, 2:1}
    # Check if board is in terminal state
    if game.isTerminal(state):
        global se
        se += 1
        return (game.utility(state, player), None)
    
    value = math.inf # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = maxValueABSE(game, game.result(state, a, oppositePlayers[player]), player, alpha, beta)
        if v2 < value:
            value = v2
            move = a
            beta = min(beta, value)
        if value <= alpha:
            return (value, move)
    return (value, move)

def minimaxDepthSE(game, state, player, currDepth, maxDepth):   
    (value, move) = maxValueDepthSE(game, state, player, currDepth, maxDepth)
    return move

def maxValueDepthSE(game, state, player, currDepth, maxDepth):
    # Check if board is in terminal state or maximum search depth reached
    if game.isTerminal(state) or currDepth == maxDepth:
        global se
        se += 1
        return (game.utility(state, player), None)
    
    value = -math.inf # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValueDepthSE(game, game.result(state, a, player), player, currDepth+1, maxDepth)
        if v2 > value:
            value = v2
            move = a
    return (value, move)

def minValueDepthSE(game, state, player, currDepth, maxDepth):
    oppositePlayers = {1:2, 2:1}
    #Checks if board is in terminal state or maximum search depth reached
    if game.isTerminal(state) or currDepth == maxDepth:
        global se
        se += 1
        return (game.utility(state, player), None)

    actions = game.getActions(state)
    move = actions[0]
    value = math.inf   # value = infinity
    for a in actions:
        v2, a2 = maxValueDepthSE(game, game.result(state, a, oppositePlayers[player]), player, currDepth+1, maxDepth)
        if v2 < value:
            value = v2
            move = a 
    return (value, move) 

def alphaBetaDepthSE(game, state, player, currDepth, maxDepth):
    (value, move) = maxValueABDepthSE(game, state, player, -math.inf, math.inf, currDepth, maxDepth)
    return move

def maxValueABDepthSE(game, state, player, alpha, beta, currDepth, maxDepth):
    # Check if board is in terminal state or maximum depth reached
    if game.isTerminal(state) or currDepth == maxDepth:
        global se
        se += 1
        return (game.utility(state, player), None)
    
    value = -math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValueABDepthSE(game, game.result(state, a, player), player, alpha, beta, currDepth+1, maxDepth)
        if v2 > value:
            value = v2
            move = a
            alpha = max(alpha, value)
        if value >= beta:
            return (value, move)
    return (value, move)

def minValueABDepthSE(game, state, player, alpha, beta, currDepth, maxDepth):
    oppositePlayers = {1:2, 2:1}
    # Check if board is in terminal state or maximum depth reached
    if game.isTerminal(state) or currDepth == maxDepth:
        global se
        se += 1
        return (game.utility(state, player), None)
    
    value = math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = maxValueABDepthSE(game, game.result(state, a, oppositePlayers[player]), player, alpha, beta, currDepth+1, maxDepth)
        if v2 < value:
            value = v2
            move = a
            beta = min(beta, value)
        if value <= alpha:
            return (value, move)
    return (value, move)

if __name__ == "__main__":
    sizes = [2,3,4,5]
    depths = [2,3,4,5,6,7]

    # minimax vs alpha beta (time & states explored)
    # - 2x2 
    # - 3x3
    # - 4x4
    # - 5x5
    for size in sizes:
        print("Size", size)
        # minimax
        se = 0
        tictactoe = Game(size)
        print("Minimax")
        if size < 4:
            start = time.perf_counter()
            aiAction = minimaxSE(tictactoe, tictactoe.board, 1)
            print("Time Taken (No Pruning):", time.perf_counter() - start)
            print("States Explored (No Pruning):", se)
        else:
            print("Takes way too long")

        # alpha beta
        print("Alpha Beta")
        se = 0
        if size < 4:
            start = time.perf_counter()
            aiActionAB = alphaBetaSE(tictactoe, tictactoe.board, 1)
            print("Time Taken (Pruning):", time.perf_counter() - start)
            print("States Explored (Pruning):", se)
        else:
            print("Takes way too long")

        print("---------------------------------------")
        # depth limit
        for depth in depths:
            print("Depth", depth)
            # minimax depth
            print("Minimax Depth")
            se = 0
            start = time.perf_counter()
            aiActionAB = minimaxDepthSE(tictactoe, tictactoe.board, 1, 1, depth)
            print("Time Taken (No Pruning):", time.perf_counter() - start)
            print("States Explored (No Pruning):", se)

            # alpha beta depth
            print("Alpha Beta Depth")
            se = 0
            start = time.perf_counter()
            aiActionAB = alphaBetaDepthSE(tictactoe, tictactoe.board, 1, 1, depth)
            print("Time Taken (Pruning):", time.perf_counter() - start)
            print("States Explored (Pruning):", se)
            print("---------------------------------------")
        
        print("================================================")

    # no heuristic vs heuristic (win game or not)

