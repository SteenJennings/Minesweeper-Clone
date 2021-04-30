The following instructions and rules apply to minesweeper.py

Tile Guide:
	"_" = Hidden Tile (can be selected for a valid move - watch out for bombs!)
	"0" = No Neighboring Bombs
	"1" = Any Number >= 1 (represents the number of bombs in the immediate vicinity)
	"F" = Flagged Cell
	"B" = Bomb (Hopefully you're seeing this because you won)

Step 1: run the file by typing into the terminal, within the folder (python3 minesweeper.py)

Step 2: You will be prompted to first enter the number of rows on your game board. This accepts a positive integer input.

Step 3: You will then be prompter to enter the number of columns. This accepts a positive integer input.

Step 4: You will declare the number of bombs to be on your board. This will need to be less than rows x columns, and a positive integer. This has validation built in.

Step 5: During the game, you will be prompted to make moves. The format of the move input is variable, if you just want to flip a tile simply enter two comma separated values withing 
the range of the map. Example input "1,1" or "1, 1" qoutes not needed. 

Step 6: To place a flag during the game, you will need to specify the tile and add a comma separated zero after. Example: "5,5,0:" quotes not needed. This will place an F on that tile if it's not already
been revealed, or if it does not already have a flag.

NOTE - It is zero based meaning that user input of 0,0 will flip the top left tile. This also means that in a 16x16 game grid, the bottom left corner represents 15,15 as an input.

Step 7: You will keep playing the game as normal until a loss or a win. In the event of either, you will see the full board and get a message letting you know the outcome. To play again, you will need to
re-run the program and select a new board!