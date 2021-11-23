import numpy as np
import time
from minimax import minimax, minValue, maxValue
from minimaxDepthLimit import minimaxDepth, minValueDepth, maxValueDepth
from alphabeta import alphaBeta, minValueAB, maxValueAB
from alphabetaDepthLimit import alphaBetaDepth, minValueABDepth, maxValueABDepth
from alphabetaHeuristic import alphaBetaDepthHeuristic, minValueABDepthHeuristic, maxValueABDepthHeuristic

class Game:
    def __init__(self, size):
        self.board = np.zeros([size, size])
        self.size = size
    
    def checkMove(self, row, col):
    #Returns false if move is out of bounds
        if row < 0 or row >= self.size:
            return False
        if col < 0 or col >= self.size:
            return False
        return True
    
    def display(self):
        n = self.size
        for i in range(n):
            for j in range(n):
                if self.board[i][j] == 0:
                    print("_", end=' ')
                elif self.board[i][j] == 1:
                    print("O", end=' ')
                else:
                     print("X", end=' ')               
            print() 
    
    def isTerminal(self, state):
        return self.checkRowsCols(state) or self.checkDiagonals(state) or self.checkFull(state)
    
    def checkValues(self, list):
        temp = set(list)
        if (len(temp)) == 1: # If row only has one symbol
            if not(list[0] == 0): # If row is not empty
                return True # Either filled with x's or o's

    def checkRowsCols(self, state):
        # Check rows in self.board and cols using transpose
        for board in [state, np.transpose(state)]:
            for row in board:
                if self.checkValues(row):
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

    def utility(self, state, player):
        # Row/Col filled
        for board in [state, np.transpose(state)]:
            for row in board:
                if self.checkValues(row):
                    if (row[0] == player):
                        return 100
                    else:
                        return -100
        
        # Diagonal filled
        diagonal1 = [state[i][i] for i in range(self.size)]
        diagonal2 = [state[self.size - 1 - i][i] for i in range(self.size)]
        if self.checkValues(diagonal1):
            if (diagonal1[0] == player):
                return 100
            else:
                return -100
        elif self.checkValues(diagonal2):
            if (diagonal2[0] == player):
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

    def heuristic(self, state, player):
        # number of possible winning rows/cols/diagonals
        oppositePlayers = {1:2, 2:1}
        possibleWins = 0
        for board in [state, np.transpose(state)]:
            for row in board:
                if oppositePlayers[player] not in row:
                    possibleWins += 1

        diagonal1 = [state[i][i] for i in range(self.size)]
        diagonal2 = [state[self.size - 1 - i][i] for i in range(self.size)]
        if oppositePlayers[player] not in diagonal1:
            possibleWins += 1
        if oppositePlayers[player] not in diagonal2:
            possibleWins += 1
        
        return possibleWins

if __name__ == "__main__":
    tictactoe = Game(3)
    print("Initial Board:\n", tictactoe.board)
    print()
    print("Initial Board with X's and O's:")
    tictactoe.display()
    validMove = False

    while not(tictactoe.isTerminal(tictactoe.board)):
        validMove = False
        start = time.time()
        aiAction = minimax(tictactoe, tictactoe.board, 1)
        print("Time Taken (No Pruning):", time.time() - start)

        start = time.time()
        aiActionAB = alphaBeta(tictactoe, tictactoe.board, 1)
        print("Time Taken (Pruning):", time.time() - start)
        
        print(aiAction)
        print(aiActionAB)
        #tictactoe.board = tictactoe.result(tictactoe.board, aiAction, 1)
        tictactoe.board = tictactoe.result(tictactoe.board, aiActionAB, 1)

        if (tictactoe.isTerminal(tictactoe.board)):
            break

        print("Current Board:\n", tictactoe.board)
        print()
        print("Current Board:")
        tictactoe.display()
        print()
        
        while not(validMove):
            playerRow = int(input("Enter row:"))
            playerCol = int(input("Enter col:"))
            validMove = tictactoe.checkMove(playerRow, playerCol)
            if (validMove == False):
                print("Invalid move!")

        playerMove = (playerRow, playerCol)
        print("Player Move:", playerMove)
        tictactoe.board = tictactoe.result(tictactoe.board, playerMove, 2)
        print("Current Board:\n", tictactoe.board)
        print()
        print("Current Board:")
        tictactoe.display()
        print()


    print("Final Board:\n", tictactoe.board)
    print()
    print("Final Board:")
    tictactoe.display()