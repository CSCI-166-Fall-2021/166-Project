import tkinter as tk
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy

from game import Game, minimax, maxValue, minValue

def placeMarker(gameboard, game, row, col):
    # Create checkValidMove function in game.py
    # Maybe makeMove function that calls checkValid?
    for i in range(game.size):
        for j in range(game.size):
            buttons[i][j].config(state=DISABLED)

    game.board[row][col] = 2
    buttons[row][col].config(text="X")

    gameboard.update()

    aiAction = minimax(game, game.board)

    game.board[aiAction[0]][aiAction[1]] = 1
    buttons[aiAction[0]][aiAction[1]].config(text="O")

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