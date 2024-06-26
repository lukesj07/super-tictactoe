from tkinter import *

# TODO: cleanup, try to optimize/modularize code (especially is_game_won + is_bgame_won)

class Space: # the definition for each 'space' object
    def __init__(self, xin, yin):
        self.label = Label(clickCanvas)
        self._val = ''
        self._x = xin
        self._y = yin

    @property
    def value(self):
        return self._val

    @value.setter
    def value(self, newval):
        self.label.place(x = self._x, y = self._y)
        match newval:
            case 'o':
                self.label.configure(image = smallCircle)
            case 'O':
                self.label.configure(image = bigCircle)
            case 'x':
                self.label.configure(image = smallCross)
            case 'X':
                self.label.configure(image = bigCross)
            case '':
                self.label.configure(image = '')
                self.label.place_forget()
        self._val = newval

def handle_click(event): # method called when the canvas is clicked
    # create vars for the position of the click relative to the canvas
    x = event.x
    y = event.y

    # pull the external turn/lastSpace vars
    global turn
    global lastSpace

    # ensures what_space returns a valid value
    if what_space(x, y) == None:
        return
    
    # make a local reference to what space was clicked
    currSpace = squares[what_game(x, y)][what_space(x, y)]
   
    # check that it is a valid space to be played on
    if currSpace.value == '' and (what_game(x, y) == lastSpace or lastSpace == None):
        ##START OF TURN##
        # change the value of the space based off the turn
        match turn:
            case 0:
                currSpace.value = 'o'
            case 1:
                currSpace.value = 'x'
        turn = not turn
        
        # check if the game played on has been won
        match is_game_won(squares[what_game(x, y)]):
            case 'x':
                for i in range(9):
                    squares[what_game(x, y)][i].value = ''
                squares[what_game(x, y)][0].value = 'X'
            case 'o':
                for i in range(9):
                    squares[what_game(x, y)][i].value = ''
                squares[what_game(x, y)][0].value = 'O'
        
        # check if the whole game has been won
        is_bgame_won()

        #set lastSpace up for next turn
        lastSpace = what_space(x, y)

        if not lastSpace == None: # to avoid None being used as an index
            # set lastSpace to None if game to be played in next is full/has been won
            if squares[lastSpace][0].value == 'O' or squares[lastSpace][0].value == 'X' or is_game_full(squares[lastSpace]):
                lastSpace = None

def is_game_full(currSquare): # returns whether the spaces in a game have been filled or not
    flag = True
    for i in range(9):
        if currSquare[i].value == '':
            flag = False
    return flag

def is_game_won(currSquare): # returns if currSquare has been won, and by who
    for i in range(8):
        match i:
            case 0:
                line = currSquare[0].value + currSquare[1].value + currSquare[2].value
            case 1:
                line = currSquare[3].value + currSquare[4].value + currSquare[5].value
            case 2:
                line = currSquare[6].value + currSquare[7].value + currSquare[8].value
            case 3:
                line = currSquare[0].value + currSquare[3].value + currSquare[6].value
            case 4:
                line = currSquare[1].value + currSquare[4].value + currSquare[7].value
            case 5:
                line = currSquare[2].value + currSquare[5].value + currSquare[8].value
            case 6:
                line = currSquare[0].value + currSquare[4].value + currSquare[8].value
            case 7:
                line = currSquare[2].value + currSquare[4].value + currSquare[6].value

        if line == 'xxx':
            return 'x'
        if line == 'ooo':
            return 'o'
    return

def is_bgame_won(): # checks if the whole game has been won
    for i in range(8):
        match i:
            case 0:
                line = squares[0][0].value + squares[1][0].value + squares[2][0].value
            case 1:
                line = squares[3][0].value + squares[4][0].value + squares[5][0].value
            case 2:
                line = squares[6][0].value + squares[7][0].value + squares[8][0].value
            case 3:
                line = squares[0][0].value + squares[3][0].value + squares[6][0].value
            case 4:
                line = squares[1][0].value + squares[4][0].value + squares[7][0].value
            case 5:
                line = squares[2][0].value + squares[5][0].value + squares[8][0].value
            case 6:
                line = squares[0][0].value + squares[4][0].value + squares[8][0].value
            case 7:
                line = squares[2][0].value + squares[4][0].value + squares[6][0].value
        if line == 'XXX':
            print("X's win!")
            exit() #Add Tkinter message
        if line == 'OOO':
            print("O's win!")
            exit()


def what_game(x, y): # returns index of what big 'square' is being played
    column = (x-13)//107
    row = (y-13)//107
    return (row*3)+column

def big_row(y):
    return (y-13)//107

def big_col(x):
    return (x-13)//107

def what_space(x, y): # returns index of what space is being played within a game
    if x < 13 or y < 13 or x > 327 or y > 327:
        return

    relY = y - big_row(y)*107 - 13
    relX = x - big_col(x)*107 - 13

    yCoord = relY // 32
    xCoord = relX // 32
    
    if 0 <= (yCoord*3)+xCoord <= 8:
        return (yCoord*3)+xCoord
    else:
        return

# initialize vars
turn = 1
lastSpace = None

# set up tkinter window
root = Tk()
root.title("Ultimate TicTacToe")
root.wm_geometry("%dx%d+%d+%d" % (340, 340, 0, 0))

# get images
bg = PhotoImage(file = "ultimate-tic-tac-toe12-01.png")
bigCircle = PhotoImage(file = "tttcircle_big.png")
smallCircle = PhotoImage(file = "tttcircle_small.png")
bigCross = PhotoImage(file = "tttcross_big.png")
smallCross = PhotoImage(file = "tttcross_small.png")

# make clickable canvas
clickCanvas = Canvas(root, width = 340, height = 340)
clickCanvas.pack()
clickCanvas.bind("<Button-1>", handle_click)
clickCanvas.create_image(0, 0, anchor=NW, image=bg)

# set up 2 dimensional array of Space objects in the format: squares[BigSquareIndex][SpaceIndex]
squares = []
for bsquarenum in range(9):
    nwcornerx = 13+((bsquarenum % 3)*107)
    nwcornery = 13+((bsquarenum // 3)*107)

    spaces = []
    for ssquarenum in range(9):
        spaces.append(Space(((ssquarenum%3)*33)+nwcornerx, ((ssquarenum//3)*33)+nwcornery))
        #32 (size of squares)+ 1 spacer
    squares.append(spaces)

# open the window
root.mainloop()
