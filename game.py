import numpy as np
import math
import random

class Game:
    def __init__(self, size):
        self.board = np.zeros([size, size])
        self.size = size
    
    def isTerminal(self, state):
        return self.checkRowsCols(state) or self.checkDiagonals(state) or self.checkFull(state)
    
    def checkValues(self, list):
        temp = set(list)
        if (len(temp)) == 1: # If row only has one symbol
            if not(list[0] == 0): # If row is not empty
                return True # Either filled with x's or o's
        return None

    def checkRowsCols(self, state):
        # Check rows in self.board and cols using transpose
        for board in [state, np.transpose(state)]:
            for row in board:
                if self.checkValues(row) == True:
                    return True
        return False

    # Check if one of the diagonals is filled up
    def checkDiagonals(self, state):
        # Top left to bottom right
        # (0,0), (1,1), ..., (n-1, n-1)
        diagonal1 = [state[i][i] for i in range(self.size)]

        # Bottom left to top right
        # (2,0), (1,1), (0,2)
        # i-1, j+1
        diagonal2 = [state[self.size - 1 - i][i] for i in range(self.size)]

        return self.checkValues(diagonal1) or self.checkValues(diagonal2)

    def checkFull(self, state):
        return not(0 in state)
            
    #Returns possible action for player
    def getActions(self, state):
        # Check if (i, j) is a 0
        possibleActions = [(i, j) for i in range(self.size) for j in range(self.size) if state[i][j] == 0]
        
        #Return actions here 
        return possibleActions

    def utility(self, state):
        # Row/Col filled
        for board in [state, np.transpose(state)]:
            for row in board:
                if self.checkValues(row):
                    if (row[0] == 1):
                        return 100
                    else:
                        return -100
        
        # Diagonal filled
        diagonal1 = [state[i][i] for i in range(self.size)]
        diagonal2 = [state[self.size - 1 - i][i] for i in range(self.size)]
        if self.checkValues(diagonal1):
            if (diagonal1[0] == 1):
                return 100
            else:
                return -100
        elif self.checkValues(diagonal2):
            if (diagonal2[0] == 1):
                return 100
            else:
                return -100

        # Tie
        return 0

    def result(self, state, action, player):
        newState = state.copy()
        (i, j) = action
        newState[i][j] = player
        return newState

def minimax(game, state):
    player = 1     
    #player <- game.To-Move(state)
    #value, move <Max-Value(game, state)
    #return move
    (value, move) = maxValue(game, state)
    return move

def maxValue(game, state):
    #Checks if board is in terminal state
    if game.isTerminal(state):
        #print("terminal")
        return (game.utility(state), None)
    
    value = -math.inf       # value = -infinty
    actions = game.getActions(state)
    move = actions[0]
    #find best move for AI
    for a in actions:
        v2, a2 = minValue(game, game.result(state, a, 1))
        if v2 > value:
            value = v2
            move = a
    #returns 
    return (value, move)

def minValue(game, state):
    #Checks if board is in terminal stpyate
    if game.isTerminal(state):
        return (game.utility(state), None)

    actions = game.getActions(state)
    move = actions[0]
    value = math.inf   # value = infinity
    for a in actions:
        v2, a2 = maxValue(game, game.result(state, a, 2))
        if v2 < value:
            value = v2
            move = a
    #returns 
    return (value, move)   

if __name__ == "__main__":
    tictactoe = Game(4)
    print("Initial Board:\n", tictactoe.board)
    tictactoe.board = np.array([[1,1,2,1],
    [0,1,1,0],
    [2,0,1,0],
    [0,0,0,0]])
    print("Initial Board:\n", tictactoe.board)
    
    while not(tictactoe.isTerminal(tictactoe.board)):
        aiAction = minimax(tictactoe, tictactoe.board)
        print(aiAction)
        tictactoe.board = tictactoe.result(tictactoe.board, aiAction, 1)

        if (tictactoe.isTerminal(tictactoe.board)):
            break

        print("Current Board:\n", tictactoe.board)
        
        playerRow = int(input("Enter row:"))
        playerCol = int(input("Enter col:"))

        playerMove = (playerRow, playerCol)
        print("Player Move:", playerMove)
        tictactoe.board = tictactoe.result(tictactoe.board, playerMove, 2)
        print("Current Board:\n", tictactoe.board)

    print("Final Board:\n", tictactoe.board)