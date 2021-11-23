import math
def alphaBeta(game, state, player):
    (value, move) = maxValueAB(game, state, player, -math.inf, math.inf)
    return move

def maxValueAB(game, state, player, alpha, beta):
    #Checks if board is in terminal state
    if game.isTerminal(state):
        return (game.utility(state, player), None)
    
    value = -math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValueAB(game, game.result(state, a, player), player, alpha, beta)
        if v2 > value:
            value = v2
            move = a
            alpha = max([alpha, value])
        if value >= beta:
            return (value, move)
    #returns 
    return (value, move)

def minValueAB(game, state, player, alpha, beta):
    oppositePlayers = {1:2, 2:1}
    #Checks if board is in terminal state
    if game.isTerminal(state):
        return (game.utility(state, player), None)
    
    value = math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = maxValueAB(game, game.result(state, a, oppositePlayers[player]), player, alpha, beta)
        if v2 < value:
            value = v2
            move = a
            beta = min([beta, value])
        if value <= alpha:
            return (value, move)
    #returns 
    return (value, move)