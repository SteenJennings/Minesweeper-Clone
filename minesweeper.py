from collections import deque
import random

class Cell():
    """This contains the data held at the cell level, it is used for validating moves and checking/revealing cell content"""
    def __init__(self, cols, rows):
        self.mine = False
        self.flag = False
        self.nearmines = 0
        self.show = False
        
class Game():
    """This is the meat of the game, contains all methods to run the game and validate solutions"""
    def __init__(self, cols=16, rows=16, mines=40):
        self.cols = cols
        self.rows = rows
        self.numMines = mines
        self.gameState = "Unfinished"
        self.hiddenCells = rows*cols  #used to tell if the game is over (hidden = bombs, no moves left)
        self.board = []
        self.mines = []

        # creates the board and a cell object for each location
        for r in range(self.rows):
            self.board.append([])
            for c in range(self.cols):
                self.board[r].append(Cell(r, c))

        # creates the mines and disperses them randomly based on mine input
        while len(self.mines) < self.numMines:
            # generate random coordinates within the grid range
            bomb_cell = [random.randrange(self.rows), random.randrange(self.cols)]
            if self.board[bomb_cell[0]][bomb_cell[1]].mine == False:
                self.board[bomb_cell[0]][bomb_cell[1]].mine = True
                self.mines.append(bomb_cell)
    
        #checks every non-mine cell and determines its neighbor count
        for r in range(self.rows):
            for c in range(self.cols):
                numMines = 0
                if self.board[r][c].mine == False:
                    if r > 0:
                        #checks above
                        if self.board[r-1][c].mine == True:
                            numMines += 1
                    if c > 0:
                        #checks to the left
                        if self.board[r][c-1].mine == True:
                            numMines += 1
                    if r < (self.rows - 1):
                        #checks below
                        if self.board[r+1][c].mine == True:
                            numMines += 1
                    if c < (self.cols - 1):
                        #checks to the right
                        if self.board[r][c+1].mine == True:
                            numMines += 1
                    if c < (self.cols - 1) and r < (self.rows - 1):
                        #checks to the lower right
                        if self.board[r+1][c+1].mine == True:
                            numMines += 1
                    if r > 0 and c > 0:
                        #checks to the upper left
                        if self.board[r-1][c-1].mine == True:
                            numMines += 1
                    if r > 0 and c < (self.cols - 1):
                        #checks to the upper right
                        if self.board[r-1][c+1].mine == True:
                            numMines += 1
                    if r < (self.rows - 1) and c > 0:
                        #checks to the lower left
                        if self.board[r+1][c-1].mine == True:
                            numMines += 1
                self.board[r][c].nearmines = numMines
    
    #places a flag cell, makes sure that there is not already a flag. Another validator checks to make sure the tile isn't already visible.
    def placeFlag(self, row, column):
        if self.board[row][column].flag == True:
            print("That tile already has a flag")
        else:
            self.board[row][column].flag = True
            self.printBoard()
    
    #this is the driving force behind the program, this will use other class methods to algorithmically perform a BFS to traverse the neighbors
    #until it runs into neighbors that are near a bomb, revealing all tiles that meet the criteria along the way
    def revealBFS(self, row, column):
        q = deque([(row,column)])
        #tracks our board to see if a cell has already been visited with a value of 1
        bfsChecked = [[0 for i in range(self.cols)] for j in range(self.rows)]
        
        while q:
            #splits the coords into row,column 
            row, column = q.popleft()
            # column = q.popleft()

            #reveal the tile after counting 
            self.board[row][column].show = True
            self.hiddenCells -= 1
            
            #if we don't have a neighboring mine we continue searching the neighbors of our current location
            if self.board[row][column].nearmines == 0:
                possibleNeighbors = [(row, column+1), (row, column-1),(row+1, column), (row-1, column),
                    (row+1, column-1), (row-1, column-1), (row+1, column+1), (row-1, column+1)]
                for r, c in possibleNeighbors:
                    #cheks to see if the neighbor is in play
                    if (0 <= r < self.rows and 0 <= c < self.cols):
                        #checks to see if the neighbor is already showing, or has already been checked this search
                        if self.board[r][c].show == False and bfsChecked[r][c] == 0:
                            #we append the coordinates to search if the criteria has been meet
                            q.append((r,c))
                            #we add them to our visited tracker because if it's in the dequeue we will check it
                            bfsChecked[r][c] = 1
                    
            
    def validateInput(self, coords):
        #checks to make sure we didn't get more that 3 inputs or less than 2
        if not (2 <= len(coords) <= 3):
            print("Invalid input: see the example input in the prompt")
            return False
        #checks to make sure the flag call was made using a 0
        elif len(coords) == 3 and coords[2] != 0:
            print("Invalid input: see the example input in the prompt")
            return False
        #checks to make sure that a flag isn't being placed on a visible tile
        elif ((0 <= coords[0] < self.rows) and (0 <= coords[1] <= self.cols)) and len(coords) == 3:
            if self.board[coords[0]][coords[1]].show == True:
                print("This tile has already been revealed")
                return False
            return True
        #checks to make sure that we haven't placed a valid move on a bomb, updates gamestate if so
        elif ((0 <= coords[0] < self.rows) and (0 <= coords[1] <= self.cols)) and len(coords) != 3:
            if self.board[coords[0]][coords[1]].mine == True:
                self.gameState = "Mine"
                return False
            #checks for a useless move
            elif self.board[coords[0]][coords[1]].show == True:
                print("This tile has already been revealed")
                return False
            elif self.board[coords[0]][coords[1]].show == False:
                return True
        print("Invalid input: see the example input in the prompt")
        return False
            
    def makeMove(self):
        #loops the user to keep entering inputs and provides input guidance
        while self.gameState == "Unfinished":
            coords = [int(x) for x in(input("Enter the row, then the column of the move [include 0 for flag like '1, 1, 0']: ").split(","))]
            #uses our validation tool
            if self.validateInput(coords) != True:
                continue
            #places a flag and reprompts if we have been passed a flag move
            elif len(coords) == 3:
                self.placeFlag(coords[0],coords[1])
                continue
            #reveals tiles
            self.revealBFS(coords[0],coords[1])
            if self.hiddenCells == self.numMines:
                self.gameState = "Won"
            else:
                self.printBoard()
        self.gameOver()
            
    def gameOver(self):
        #if we triggered a mine, we lose 
        if self.gameState == "Mine":
            print("You stepped on a mine! Start the program over to try again!")
        else:
            print("Congrats, you're a winner!")
        self.revealBoard()
        self.printBoard()
    
    def revealBoard(self):
        #reveals the board for the final print screen
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c].show = True
        
    def printBoard(self):
        #creates a temp board of the class items to print to the console
        board_print = [[" " for i in range(self.cols)] for j in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                #checks to see if the cell has been revealed, if not prints an _
                if self.board[r][c].show != True and self.board[r][c].flag != True:
                    board_print[r][c] = "_"
                #checks if there is a flag that has been placed
                elif self.board[r][c].flag == True and self.board[r][c].show != True:
                    board_print[r][c] = "F"
                elif self.board[r][c].mine == True:
                    board_print[r][c] = "B"
                else:
                    board_print[r][c] = str(self.board[r][c].nearmines)
        for row in board_print:
            print(row)
                                    

# User Game Start Logic
print("Welcome to MineSweeper! Please Set up the board below. [Note: A standard game consists 16 rows, 16 columns, 40 mines]")
r = int(input("Enter the number of rows: "))
c = int(input("Enter the number of columns: ")) 
mineValidator = False
while mineValidator == False:    
    mines = int(input("Enter the number of mines on the game board: "))
    if mines < r*c:
        mineValidator = True
    else:
        print("Thats too many bombs, leave at least 1 non-bomb tile!")
    
game = Game(r,c,mines)
game.printBoard()
print("The game is 0 based indexed, so entering '0, 0' will flip the upper left most tile")
print("To play: Enter the row, then the column of the tile you want to flip to place a flag include a 0 [formatted like '6, 7' for row 6, column 7 or '6, 7, 0' for a flag there]")
#coords = [int(x) for x in(input("Enter the row, then the column of the tile you want to flip to place a flag include a 0 [formatted like '6, 7' for row 6, column 7 or '6, 7, 0' for a flag there]: ").split(","))]
game.makeMove()