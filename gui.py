import tkinter as tk
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy
import numpy as np

from game import Game, minimax, maxValue, minValue

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

def placeMarker(gameboard, game, row, col):
    # Create checkValidMove function in game.py
    # Maybe makeMove function that calls checkValid?
    for i in range(game.size):
        for j in range(game.size):
            buttons[i][j].config(state=DISABLED)

    game.board[row][col] = 2
    buttons[row][col].config(text="X")
    gameboard.update()

    # Check terminal
    if game.isTerminal(game.board):
        winner = getWinner(game)
        gameboard.destroy()
        if winner == 0:
            box = messagebox.showinfo("Tie", "Tie Game")
        elif winner == 1:
            box = messagebox.showinfo("Winner", "O won")
        else:
            box = messagebox.showinfo("Winner", "X won")

    aiAction = minimax(game, game.board)

    game.board[aiAction[0]][aiAction[1]] = 1
    buttons[aiAction[0]][aiAction[1]].config(text="O")

    if game.isTerminal(game.board):
        winner = getWinner(game)
        gameboard.destroy()
        if winner == 0:
            box = messagebox.showinfo("Tie", "Tie Game")
        elif winner == 1:
            box = messagebox.showinfo("Winner", "X won")
        else:
            box = messagebox.showinfo("Winner", "O won")

    for i in range(game.size):
        for j in range(game.size):
            if game.board[i][j] == 0:
                buttons[i][j].config(state=ACTIVE)


def drawBoard(gameboard, game):
    global buttons
    buttons = [[] for i in range(game.size)]

    for i in range(game.size):
        for j in range(game.size):
            mm = partial(placeMarker, gameboard, game, i, j)
            buttons[i].append(
                Button(
                gameboard, command=mm)
            )
            buttons[i][j].grid(row=i+3, column=j, sticky="NSWE")
            gameboard.grid_columnconfigure(j, weight=1)
            gameboard.grid_rowconfigure(i+3, weight=1)

    while True:
        #print(game.board)
        gameboard.update_idletasks()
        gameboard.update()
    #gameboard.mainloop()

def playerVsAI(gameboard):
    gameboard.destroy()
    gameboard = Tk()
    gameboard.geometry("1080x720")
    gameboard.title("Tic Tac Toe")
    l1 = Button(gameboard, text="Player : X")
    l1.grid(row=1, columnspan=3, sticky="NSWE")
    l2 = Button(gameboard, text = "Computer : O",
                state = DISABLED)
    l2.grid(row = 2, columnspan=3, sticky="NSWE")

    gameboard.grid_rowconfigure(1, weight=1)
    gameboard.grid_rowconfigure(2, weight=1)

    tictactoe = Game(3)
    drawBoard(gameboard, tictactoe)

if __name__ == "__main__":
    menu = Tk()
    menu.geometry("1080x720")
    menu.title("Tic Tac Toe")
    pvai = partial(playerVsAI, menu)

    head = Button(menu, text = "Tic-Tac-Toe",
                activeforeground = 'blue',
                activebackground = "blue", bg = "blue",
                fg = "white", font = 'helvetica')
    
    B1 = Button(menu, text = "Player vs. AI", command = pvai,
                activeforeground = 'red',
                activebackground = "yellow", bg = "red",
                fg = "white", font = 'summer')
    
    B2 = Button(menu, text = "AI vs. AI", command = pvai,
                activeforeground = 'red',
                activebackground = "yellow", bg = "red",
                fg = "white", font = 'summer')
    
    menu.grid_columnconfigure(1, weight=1)
    menu.grid_rowconfigure(1, weight=1)
    menu.grid_rowconfigure(2, weight=5)
    menu.grid_rowconfigure(3, weight=5)
    head.grid(row=1, column=1, sticky="NSWE")
    B1.grid(row=2, column=1, sticky="NSWE")
    B2.grid(row=3, column=1, sticky="NSWE")

    menu.mainloop()