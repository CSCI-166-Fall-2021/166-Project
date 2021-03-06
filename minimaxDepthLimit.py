import math
def minimaxDepth(game, state, player, currDepth, maxDepth):   
    (value, move) = maxValueDepth(game, state, player, currDepth, maxDepth)
    return move

def maxValueDepth(game, state, player, currDepth, maxDepth):
    # Check if board is in terminal state or maximum search depth reached
    if game.isTerminal(state) or currDepth == maxDepth:
        return (game.utility(state, player), None)
    
    value = -math.inf # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValueDepth(game, game.result(state, a, player), player, currDepth+1, maxDepth)
        if v2 > value:
            value = v2
            move = a
    return (value, move)

def minValueDepth(game, state, player, currDepth, maxDepth):
    oppositePlayers = {1:2, 2:1}
    #Checks if board is in terminal state or maximum search depth reached
    if game.isTerminal(state) or currDepth == maxDepth:
        return (game.utility(state, player), None)

    actions = game.getActions(state)
    move = actions[0]
    value = math.inf   # value = infinity
    for a in actions:
        v2, a2 = maxValueDepth(game, game.result(state, a, oppositePlayers[player]), player, currDepth+1, maxDepth)
        if v2 < value:
            value = v2
            move = a 
    return (value, move) 