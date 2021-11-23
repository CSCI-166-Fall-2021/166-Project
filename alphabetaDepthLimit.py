import math
def alphaBetaDepth(game, state, player, currDepth, maxDepth):
    (value, move) = maxValueABDepth(game, state, player, -math.inf, math.inf, currDepth, maxDepth)
    return move

def maxValueABDepth(game, state, player, alpha, beta, currDepth, maxDepth):
    # Check if board is in terminal state or maximum depth reached
    if game.isTerminal(state) or currDepth == maxDepth:
        return (game.utility(state, player), None)
    
    value = -math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValueABDepth(game, game.result(state, a, player), player, alpha, beta, currDepth+1, maxDepth)
        if v2 > value:
            value = v2
            move = a
            alpha = max(alpha, value)
        if value >= beta:
            return (value, move)
    return (value, move)

def minValueABDepth(game, state, player, alpha, beta, currDepth, maxDepth):
    oppositePlayers = {1:2, 2:1}
    # Check if board is in terminal state or maximum depth reached
    if game.isTerminal(state) or currDepth == maxDepth:
        return (game.utility(state, player), None)
    
    value = math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = maxValueABDepth(game, game.result(state, a, oppositePlayers[player]), player, alpha, beta, currDepth+1, maxDepth)
        if v2 < value:
            value = v2
            move = a
            beta = min(beta, value)
        if value <= alpha:
            return (value, move)
    return (value, move)