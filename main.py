
import random
from tkinter import*
from tkinter.constants import DISABLED, NORMAL
from functools import partial

class BotTile:
    def __init__(self, value, _x, _y):
        self.value = value
        self._x = _x
        self._y = _y


winX = []
winY = []
board = []

#Print board with evaluated values
def printMatrix(matrix):
    for y in range(len(matrix)):
        s = ""
        for x in range(len(matrix)):
            s += str(matrix[y][x]) + ", "
        print(s + "\n")





def PlayerTurn(buttonY, buttonX):
    print(str(buttonY) + ", " + str(buttonX))
    if board[buttonY][buttonX].cget('text') == "":
        board[buttonY][buttonX].config(text="X")
        window.update()
        if CheckWinner("X"):
            EndGame("X")
        elif CheckBoardStatus():
            EndGame("T")
        else:
            BotTurn()

#Check for winner
def DeeperCheck(startY, startX, symbol, symbolCount, yDirection, xDirection):
    #Check surrounding tiles
    if symbolCount == 1:
        for y in range(-1, 2):
            for x in range(-1, 2):
                if not(x == 0 and y == 0):
                    #Check if coordinates are still inbound
                    if (startX + x >= 0) and (startY + y >= 0) and (startX + x < len(board)) and (startY + y < len(board)):
                        if board[startY + y][startX + x].cget('text') == symbol:
                            if DeeperCheck(startY + y, startX + x, symbol, symbolCount + 1, y, x):
                                return True
        return False
    else:
        if (startX + xDirection >= 0) and (startY + yDirection >= 0) and (startX + xDirection < len(board)) and (startY + yDirection < len(board)):
            if board[startY + yDirection][startX + xDirection].cget('text') == symbol:
                if (symbolCount + 1 < streakToWin):
                    return DeeperCheck(startY + yDirection, startX + xDirection, symbol, symbolCount + 1, yDirection, xDirection)
                else:
                    SetWinTiles(startX, xDirection, startY, yDirection)
                    return True
            else:
                return False
    return False

def BotTurn():
    tempBoard = []
    for y in range(len(board)):
        a = []
        for x in range(len(board)):
            a.append(int(0))
        tempBoard.append(a)
    #Add weight of own tiles
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x].cget('text') == "":
                tempBoard[y][x] += botPositionReevaluate(BotEvaluateTiles(y,x, 0, "O", 0,0))
            else:
                tempBoard[y][x] = 0
    #Add weight of enemy tiles
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x].cget('text') == "":
                tempBoard[y][x] += BotEvaluateTiles(y,x, 0, "X", 0,0) ** 3
            else:
                tempBoard[y][x] = 0
    printMatrix(tempBoard)

    #Find tiles with best values
    listOfBestTiles = []
    listOfBestTiles.append(BotTile(0,0,0))
    for y in range(len(board)):
        for x in range(len(board)):
            if tempBoard[y][x] > listOfBestTiles[0].value:
                listOfBestTiles.clear()
                listOfBestTiles.append(BotTile(tempBoard[y][x], x, y))
            elif tempBoard[y][x] == listOfBestTiles[0].value:
                listOfBestTiles.append(BotTile(tempBoard[y][x], x, y))

    tileChosen = listOfBestTiles[random.randrange(0, len(listOfBestTiles))]
    board[tileChosen._y][tileChosen._x].config(text= "O")
    print("Took tile: " + str(tileChosen._y) + ", " + str(tileChosen._x))

    if CheckWinner("O"):
        EndGame("O")
    elif CheckBoardStatus():
        EndGame("T")

def BotEvaluateTiles(startY, startX, symbolCount, symbol, yDirection, xDirection):
    #Check surrounding tiles
    if symbolCount == 0:
        tileScore = 0
        for y in range(-1, 2):
            for x in range(-1, 2):
                if not(x == 0 and y == 0):
                    #Check if coordinates are still inbound
                    if (startX + x >= 0) and (startY + y >= 0) and (startX + x < len(board)) and (startY + y < len(board)):
                        if board[startY + y][startX + x].cget('text') == symbol:
                            tempScore =  BotEvaluateTiles(startY + y, startX + x, symbolCount + 1, symbol, y, x)
                            if tempScore > tileScore:
                                tileScore = tempScore
        return tileScore
    else:
        if (startX + xDirection >= 0) and (startY + yDirection >= 0) and (startX + xDirection < len(board)) and (startY + yDirection < len(board)):
            if board[startY + yDirection][startX + xDirection].cget('text') == symbol:
                return BotEvaluateTiles(startY + yDirection, startX + xDirection, symbolCount + 1, symbol, yDirection, xDirection)
            else:
                return int(symbolCount)
        else:
            return int(symbolCount)


def botPositionReevaluate(score):
    match score:
        case 3:
            return 500
        case 4:
            return 50000
        case _:
            return score

def SetWinTiles(startX, xDirection, startY, yDirection):
    startX += xDirection
    startY += yDirection
    
    xDirection *= -1
    yDirection *= -1
    print("Start y: " + str(startY) + ", start x: " + str(startX))

    for i in range(streakToWin):
        board[startY][startX].config(bg = "red" )
        startX += xDirection
        startY += yDirection

def CheckWinner(symbol):
    for y in range(len(board)):
        for x in range(len(board)):
            if (board[y][x].cget('text') == symbol):
                if DeeperCheck(y, x, symbol, 1, 0, 0):
                    return True

#Rows/columns in line needed to win
def SetWinStreak(rcount):
    global streakToWin
    if rcount < 5:
        streakToWin = 3
    elif rcount >= 5 and rcount <= 8:
        streakToWin = 4
    elif rcount > 8 and rcount < 12:
        streakToWin = 5
    else:
        streakToWin = rcount / 2

#Check if board is full
def CheckBoardStatus():
    for y in range(len(board)):
        for x in range(len(board)):
            if (board[y][x].cget('text') == ""):
                return False
    return True

def InitializeBoard(size):
    global rowcount, board
    if size == -100:
        try:
            rowcount = int(customSizeEntry.get())
        except ValueError:
            return
    else:
        rowcount = size
    SetWinStreak(rowcount)
    customSizeLable.destroy()
    customSizeEntry.destroy()
    customSizeButton.destroy()
    sizeLabel.destroy()
    sizeButton1.destroy()
    sizeButton2.destroy()
    sizeButton3.destroy()
    for y in range(rowcount):
        a = []
        for x in range(rowcount):
            b = Button(window, text="", width=5, height=2, font='Arial, 16 bold', command=partial(PlayerTurn, y, x))
            b.grid(row = y, column = x)
            a.append(b)
        board.append(a)
    window.title("TicTacToe")
    if random.randrange(0, 2) == 1:
        BotTurn()

def EndGame(symbol): 
    for y in range(len(board)):
        for x in range(len(board)):
            board[y][x]['state'] = DISABLED
    
    winText =""
    if symbol == "T":
        winText = "Tie"
    else:
        winText = symbol + " Won!"
    print(winText)
    global winLabel
    global restartButton
    winLabel = Label(window, text=winText)
    restartButton = Button(window, text ="Restart", command=Restart)
    row = len(board)
    winLabel.grid(row = row, column = 0)
    restartButton.grid(row = row, column = 1)

def Restart():
    for y in range(len(board)):
        for x in range(len(board)):
            board[y][x].destroy()
    board.clear()
    winLabel.destroy()
    restartButton.destroy()
    window.update()
    StartGame()


def StartGame():
    global customSizeLable
    global customSizeEntry
    global customSizeButton
    global sizeLabel
    global sizeButton1
    global sizeButton2
    global sizeButton3

    sizeLabel = Label(window, text= "Set size of the board ")
    sizeButton1 = Button(window, text = "3", command=partial(InitializeBoard, 3))
    sizeButton2 = Button(window, text = "5", command=partial(InitializeBoard, 5))
    sizeButton3 = Button(window, text = "10", command=partial(InitializeBoard, 10))

    customSizeLable = Label(window, text="Give custom board size ")
    customSizeEntry = Entry(window)
    customSizeButton = Button(window, text = "Submit", command=partial(InitializeBoard, -100))

    sizeLabel.grid(row = 0, column =0)
    sizeButton1.grid(row = 0, column = 1)
    sizeButton2.grid(row = 0, column = 2)
    sizeButton3.grid(row = 0, column = 3)

    customSizeLable.grid(row = 1, column = 0)
    customSizeEntry.grid(row = 1, column = 1)
    customSizeButton.grid(row = 1, column= 2)


window = Tk()

StartGame()

window.mainloop()


#Todo
#Skaalatuvua ikkunas