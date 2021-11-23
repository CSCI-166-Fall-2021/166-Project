import math
def minimax(game, state, player):   
    (value, move) = maxValue(game, state, player)
    return move

def maxValue(game, state, player):
    # Check if board is in terminal state
    if game.isTerminal(state):
        return (game.utility(state, player), None)
    
    value = -math.inf # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValue(game, game.result(state, a, player), player)
        if v2 > value:
            value = v2
            move = a 
    return (value, move)

def minValue(game, state, player):
    oppositePlayers = {1:2, 2:1}
    #Checks if board is in terminal state
    if game.isTerminal(state):
        return (game.utility(state, player), None)

    actions = game.getActions(state)
    move = actions[0]
    value = math.inf # value = infinity
    for a in actions:
        v2, a2 = maxValue(game, game.result(state, a, oppositePlayers[player]), player)
        if v2 < value:
            value = v2
            move = a
    return (value, move)   