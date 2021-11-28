import tkinter as tk
from tkinter import *
from functools import partial
from tkinter import messagebox
import numpy as np

from game import Game
from minimax import minimax, minValue, maxValue
from minimaxDepthLimit import minimaxDepth, minValueDepth, maxValueDepth
from alphabeta import alphaBeta, minValueAB, maxValueAB
from alphabetaDepthLimit import alphaBetaDepth, minValueABDepth, maxValueABDepth
from alphabetaHeuristic import alphaBetaDepthHeuristic, minValueABDepthHeuristic, maxValueABDepthHeuristic

# globals
font = ("OCR A Extended", 40)
defaultDepth = 6
alphaBetaOption = True
heuristicOption = True

def getWinner(game):
    state = game.board
    # Check rows/cols
    for board in [state, np.transpose(state)]:
        for row in board:
            temp = set(row)
            if (len(temp)) == 1: # If row only has one symbol
                if not(row[0] == 0): # If row is not empty
                    return row[0] # Either filled with x's or o's

    # Check diagonals
    diagonal = [state[i][i] for i in range(game.size)]
    temp = set(diagonal)
    if (len(temp)) == 1: # If row only has one symbol
        if not(diagonal[0] == 0): # If row is not empty
            return diagonal[0] # Either filled with x's or o's

    diagonal = [state[game.size - 1 - i][i] for i in range(game.size)]
    temp = set(diagonal)
    if (len(temp)) == 1: # If row only has one symbol
        if not(diagonal[0] == 0): # If row is not empty
            return diagonal[0] # Either filled with x's or o's

    # Tie
    return 0

def checkGameEnd(gameboard, game):
    if game.isTerminal(game.board):
        winner = getWinner(game)
        if winner == 0:
            box = messagebox.showinfo("Tie", "Tie Game")
        elif winner == 1:
            box = messagebox.showinfo("Winner", "X Won")
        else:
            box = messagebox.showinfo("Winner", "O Won")
        gameboard.destroy()
        menu()
            
def placeMarker(gameboard, game, row, col, maxDepth):
    # Disable all buttons so player can't keep placing before AI makes its move
    for i in range(game.size):
        for j in range(game.size):
            buttons[i][j].config(state=DISABLED)

    # Player move
    game.board[row][col] = 1
    buttons[row][col].config(text="X")
    gameboard.update()

    # Check if game is over
    checkGameEnd(gameboard, game)

    # AI move
    l2.config(text="Thinking...")
    gameboard.update()
    aiAction = getAiAction(gameboard, game, 2, 1, maxDepth)
    l2.config(text="Computer : O")
    gameboard.update()
    game.board[aiAction[0]][aiAction[1]] = 2
    buttons[aiAction[0]][aiAction[1]].config(text="O")

    # Check if game is over
    checkGameEnd(gameboard, game)

    # Reenable buttons when it is player's turn again
    for i in range(game.size):
        for j in range(game.size):
            if game.board[i][j] == 0:
                buttons[i][j].config(state=ACTIVE)

def getAiAction(gameboard, game, player, currDepth, maxDepth):
    global heuristicOption
    global alphaBetaOption
    if alphaBetaOption:
        if heuristicOption:
            return alphaBetaDepthHeuristic(game, game.board, player, currDepth, maxDepth)
        return alphaBetaDepth(game, game.board, player, currDepth, maxDepth)
    else:
        return minimaxDepth(game, game.board, player, currDepth, maxDepth)

def drawBoard(gameboard, game, maxDepth):
    global buttons
    buttons = [[] for i in range(game.size)]

    for i in range(game.size):
        for j in range(game.size):
            mm = partial(placeMarker, gameboard, game, i, j, maxDepth)
            buttons[i].append(
                Button(
                gameboard, command=mm, font=("OCR A Extended", 40))
            )
            buttons[i][j].grid(row=i+3, column=j, sticky="NSWE")
            gameboard.grid_columnconfigure(j, weight=1)
            gameboard.grid_rowconfigure(i+3, weight=1)

    for i in range(game.size):
        for j in range(game.size):
            buttons[i][j].config(state=DISABLED)

    firstTurnAI = np.random.randint(0,2)
    if firstTurnAI:
        l2.config(text="Thinking...")
        gameboard.update()
        aiAction = getAiAction(gameboard, game, 2, 1, maxDepth)
        l2.config(text="Computer : O")
        gameboard.update()
        game.board[aiAction[0]][aiAction[1]] = 2
        buttons[aiAction[0]][aiAction[1]].config(text="O")

    for i in range(game.size):
        for j in range(game.size):
            buttons[i][j].config(state=ACTIVE)

    gameboard.mainloop()

def playerVsAI(gameboard, size, maxDepth):
    gameboard.destroy()
    gameboard = Tk()
    gameboard.geometry("1080x720")
    gameboard.title("Tic Tac Toe")
    global l1
    global l2
    tictactoe = Game(size)
    l1 = Button(gameboard, text="Player : X", font=("OCR A Extended", 20), state = DISABLED)
    l2 = Button(gameboard, text = "Computer : O",
                state = DISABLED, font=("OCR A Extended", 20))
    l1.grid(row=1, columnspan=tictactoe.size, sticky="NSWE")
    l2.grid(row = 2, columnspan=tictactoe.size, sticky="NSWE")

    gameboard.grid_rowconfigure(1, weight=1)
    gameboard.grid_rowconfigure(2, weight=1)

    drawBoard(gameboard, tictactoe, maxDepth)

def AIVsAI(gameboard, size, maxDepth):
    gameboard.destroy()
    gameboard = Tk()
    gameboard.geometry("1080x720")
    gameboard.title("Tic Tac Toe")
    game = Game(size)
    global l1
    global l2
    l1 = Button(gameboard, text="Computer 1 : X", font=("OCR A Extended", 20), state = DISABLED)
    l2 = Button(gameboard, text = "Computer 2 : O",
                state = DISABLED, font=("OCR A Extended", 20))
    l1.grid(row=1, columnspan=game.size, sticky="NSWE")
    l2.grid(row = 2, columnspan=game.size, sticky="NSWE")

    gameboard.grid_rowconfigure(1, weight=1)
    gameboard.grid_rowconfigure(2, weight=1)

    global buttons
    buttons = [[] for i in range(game.size)]

    for i in range(game.size):
        for j in range(game.size):
            buttons[i].append(
                Button(
                gameboard, font=("OCR A Extended", 40), state=DISABLED)
            )
            buttons[i][j].grid(row=i+3, column=j, sticky="NSWE")
            gameboard.grid_columnconfigure(j, weight=1)
            gameboard.grid_rowconfigure(i+3, weight=1)
    
    gameboard.update()
    while True:
        # AI move
        l1.config(text="Thinking...")
        gameboard.update()
        aiAction = getAiAction(gameboard, game, 1, 1, maxDepth)
        l1.config(text="Computer 1: X")
        gameboard.update()
        game.board[aiAction[0]][aiAction[1]] = 1
        buttons[aiAction[0]][aiAction[1]].config(text="X")
        gameboard.update()

        # Check if game is over
        checkGameEnd(gameboard, game)

        # AI move
        l2.config(text="Thinking...")
        gameboard.update()
        aiAction = getAiAction(gameboard, game, 2, 1, maxDepth)
        l2.config(text="Computer 2: O")
        gameboard.update()
        game.board[aiAction[0]][aiAction[1]] = 2
        buttons[aiAction[0]][aiAction[1]].config(text="O")
        gameboard.update()

        # Check if game is over
        checkGameEnd(gameboard, game)

def size(menu, choice, maxDepth):
    menu.destroy()
    menu = Tk()
    menu.geometry("1080x720")
    menu.title("Tic Tac Toe")
    if choice == 0:
        pvai3 = partial(playerVsAI, menu, 3, maxDepth)
        pvai4 = partial(playerVsAI, menu, 4, maxDepth)
        pvai5 = partial(playerVsAI, menu, 5, maxDepth)
        pvai = partial(inputSize, menu, choice, maxDepth)
    else:
        pvai3 = partial(AIVsAI, menu, 3, maxDepth)
        pvai4 = partial(AIVsAI, menu, 4, maxDepth)
        pvai5 = partial(AIVsAI, menu, 5, maxDepth)
        pvai = partial(inputSize, menu, choice, maxDepth)

    head = Button(menu, text = "Size",
                activeforeground = 'blue',
                activebackground = "silver", bg = "white",
                fg = "black", font = ("OCR A Extended", 40), state=DISABLED)
    
    B1 = Button(menu, text = "3x3", command = pvai3,
                activeforeground = 'red',
                activebackground = "silver", bg = "white",
                fg = "black", font = ("OCR A Extended", 20))

    B2 = Button(menu, text = "4x4", command = pvai4,
                activeforeground = 'red',
                activebackground = "silver", bg = "white",
                fg = "black", font = ("OCR A Extended", 20))            
    
    B3 = Button(menu, text = "5x5", command = pvai5,
                activeforeground = 'red',
                activebackground = "silver", bg = "white",
                fg = "black", font = ("OCR A Extended", 20))
    
    B4 = Button(menu, text = "Input Size", command = pvai,
                activeforeground = 'red',
                activebackground = "silver", bg = "white",
                fg = "black", font = ("OCR A Extended", 20))
    
    menu.grid_columnconfigure(1, weight=1)
    menu.grid_rowconfigure(1, weight=1)
    menu.grid_rowconfigure(2, weight=5)
    menu.grid_rowconfigure(3, weight=5)
    menu.grid_rowconfigure(4, weight=5)
    menu.grid_rowconfigure(5, weight=5)


    head.grid(row=1, column=1, sticky="NSWE")
    B1.grid(row=2, column=1, sticky="NSWE")
    B2.grid(row=3, column=1, sticky="NSWE")
    B3.grid(row=4, column=1, sticky="NSWE")
    B4.grid(row=5, column=1, sticky="NSWE")

def inputSize(menu, choice, maxDepth):
    newRoot = Tk()
    newRoot.geometry("400x600")
    textEntry = tk.Entry(newRoot)
    textEntry.grid(row=1, column=1, sticky="NESW")

    def start():
        size = int(textEntry.get())
        newRoot.destroy()
        if choice == 0:
            playerVsAI(menu, size, maxDepth)
        else:
            AIVsAI(menu, size, maxDepth)

    button1 = tk.Button(newRoot, text='Input Size', command=start)
    button1.grid(row=2, column=1, sticky="NESW")

    newRoot.grid_rowconfigure(1, weight=1)
    newRoot.grid_rowconfigure(2, weight=1)
    newRoot.grid_columnconfigure(1, weight=1)
    newRoot.mainloop()

def settingsMenu(menuWindow):
    global font
    menuWindow.destroy()
    settings = Tk()
    settings.geometry("1080x720")
    settings.title("Settings")

    # depth limit - +/-
    def lowerDepth():
        global defaultDepth
        defaultDepth -= 1
        currDepth.config(text=defaultDepth)
    def raiseDepth():
        global defaultDepth
        defaultDepth += 1
        currDepth.config(text=defaultDepth)

    depth = Button(settings, text="Depth Limit", state=DISABLED, font=font)
    minusDepth = Button(settings, text="-", font=font, command=lowerDepth)
    currDepth = Button(settings, text=defaultDepth, font=font)
    plusDepth = Button(settings, text="+", font=font, command=raiseDepth)

    depth.grid(row=1, column=1, sticky="NESW")
    minusDepth.grid(row=1, column=2, columnspan=2, sticky="NSEW")
    currDepth.grid(row=1, column=4, columnspan=2, sticky="NSEW")
    plusDepth.grid(row=1, column=6, columnspan=2, sticky="NSEW")

    # alpha beta - ON/OFF
    def alphaBetaOn():
        global alphaBetaOption, ABOn, ABOff
        alphaBetaOption = True
        ABOn.config(state=DISABLED)
        ABOff.config(state=ACTIVE)
    def alphaBetaOff():
        global alphaBetaOption, ABOn, ABOff
        alphaBetaOption = False
        ABOff.config(state=DISABLED)
        ABOn.config(state=ACTIVE)

    global ABOn, ABOff
    ABButton = Button(settings, text="Alpha-Beta Pruning", state=DISABLED, font=font)
    ABOn = Button(settings, text="ON", state=DISABLED, font=font, command=alphaBetaOn)
    ABOff = Button(settings, text="OFF", font=font, command=alphaBetaOff)

    ABButton.grid(row=2, column=1, sticky="NSEW")
    ABOn.grid(row=2, column=2, columnspan=3, sticky="NSEW")
    ABOff.grid(row=2, column=5, columnspan=3, sticky="NSEW")

    # heuristic? - ON/OFF
    def heuristicOn():
        global heuristicOption, heuristicON, heuristicOFF
        heuristicOption = True
        heuristicON.config(state=DISABLED)
        heuristicOFF.config(state=ACTIVE)
    def heuristicOff():
        global heuristicOption, heuristicON, heuristicOFF
        heuristicOption = False
        heuristicON.config(state=ACTIVE)
        heuristicOFF.config(state=DISABLED)

    global heuristicON, heuristicOFF
    heuristicButton = Button(settings, text="Heuristic", state=DISABLED, font=font)
    heuristicON = Button(settings, text="ON", state=DISABLED, font=font, command=heuristicOn)
    heuristicOFF = Button(settings, text="OFF", font=font, command=heuristicOff)

    heuristicButton.grid(row=3, column=1, sticky="NSEW")
    heuristicON.grid(row=3, column=2, columnspan=3, sticky="NSEW")
    heuristicOFF.grid(row=3, column=5, columnspan=3, sticky="NSEW")

    # back to menu
    def backToMenu():
        settings.destroy()
        menu()
    menuButton = Button(settings, text="Back to Menu", font=font, command=backToMenu)
    menuButton.grid(row=4, column=1, columnspan=7, sticky="NSEW")

    # row/col configure
    for i in range(1, 5):
        settings.grid_rowconfigure(i, weight=1, uniform="foo")
    settings.grid_columnconfigure(1, weight=10, uniform="foo")
    for i in range(2, 8):
        settings.grid_columnconfigure(i, weight=1, uniform="foo")

    settings.mainloop()

def menu():
    menu = Tk()
    menu.geometry("1080x720")
    menu.title("Tic Tac Toe")

    global defaultDepth, font

    pvai = partial(size, menu, 0, defaultDepth)
    avai = partial(size, menu, 1, defaultDepth)
    sett = partial(settingsMenu, menu)

    head = Button(menu, text = "Tic-Tac-Toe",
                activeforeground = 'blue',
                activebackground = "silver", bg = "white",
                fg = "black", font = font, state=DISABLED)
    
    B1 = Button(menu, text = "Player vs. AI", command = pvai,
                activeforeground = 'red',
                activebackground = "silver", bg = "white",
                fg = "black", font = font)
    
    B2 = Button(menu, text = "AI vs. AI", command = avai,
                activeforeground = 'red',
                activebackground = "silver", bg = "white",
                fg = "black", font = font)
    
    B3 = Button(menu, text = "Settings", command = sett,
                activeforeground = 'red',
                activebackground = "silver", bg = "gray",
                fg = "black", font = font)
    
    menu.grid_columnconfigure(1, weight=1)
    menu.grid_rowconfigure(1, weight=1)
    menu.grid_rowconfigure(2, weight=5)
    menu.grid_rowconfigure(3, weight=5)
    menu.grid_rowconfigure(4, weight=5)
    head.grid(row=1, column=1, sticky="NSWE")
    B1.grid(row=2, column=1, sticky="NSWE")
    B2.grid(row=3, column=1, sticky="NSWE")
    B3.grid(row=4, column=1, sticky="NSWE")

    menu.mainloop()

if __name__ == "__main__":
    menu()