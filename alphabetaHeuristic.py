import math
def alphaBetaDepthHeuristic(game, state, player, currDepth, maxDepth):
    (value, move) = maxValueABDepthHeuristic(game, state, player, -math.inf, math.inf, currDepth, maxDepth)
    return move

def maxValueABDepthHeuristic(game, state, player, alpha, beta, currDepth, maxDepth):
    #Checks if board is in terminal state
    if game.isTerminal(state):
        return (game.utility(state, player), None)
    if currDepth == maxDepth:
        return (game.heuristic(state, player), None)
    
    value = -math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValueABDepthHeuristic(game, game.result(state, a, player), player, alpha, beta, currDepth+1, maxDepth)
        if v2 > value:
            value = v2
            move = a
            alpha = max([alpha, value])
        if value >= beta:
            return (value, move)
    #returns 
    return (value, move)

def minValueABDepthHeuristic(game, state, player, alpha, beta, currDepth, maxDepth):
    oppositePlayers = {1:2, 2:1}
    #Checks if board is in terminal state
    if game.isTerminal(state):
        return (game.utility(state, player), None)
    if currDepth == maxDepth:
        return (game.heuristic(state, player), None)
    
    value = math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = maxValueABDepthHeuristic(game, game.result(state, a, oppositePlayers[player]), player, alpha, beta, currDepth+1, maxDepth)
        if v2 < value:
            value = v2
            move = a
            beta = min([beta, value])
        if value <= alpha:
            return (value, move)
    #returns 
    return (value, move)
