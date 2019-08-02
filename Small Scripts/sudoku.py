"""
Taylor Barmak

Program will create a valid 9x9 sudoku before asking the user for a difficulty level.
The higher the difficulty level, the more numbers that will be removed.
After creating the final sudoku, it will be exported to an excel file.
"""
# Imports
import pandas as pd
import numpy as np
import random

# Boxes is a dictionary to store the coordinates of the cells inside each 3x3 box in the sudoku
boxes = {}

# Boxes are numbered 0 through 8
for a in range(9):
    boxes[a] = [] # The key will be the number and its corresponding value is a list of tuples of the cells in that box
    y = (a//3) * 3
    x = (a % 3) * 3
    for c in range(x, x + 3):
        for d in range(y, y + 3):
            boxes[a].append((c, d))

complete = False # Boolean variable to keep track of if a valid board has been created
attempts_exceeded = False # Boolean variable to see if it got stuck
attemps = 0 # Number of times it has attempted to put a number in a cell that hasn't worked

# While a board has not been made
while not complete:
    print("Trying another board...")
    # The board starts out as a 9x9 grid of 0s
    board = np.zeros((9, 9), dtype=int)
    # Reset the number of attempts
    attempts = 0
    attempts_exceeded = False

    # Go through each of the rows
    for row in range(9):
        if attempts_exceeded:
            break
        # Go through each of the columns
        for column in range(9):
            row_col_satisfied = False # Condition met if the number is not already in the row or column
            box_satisfied = True # Condition met if the number is not already in the box
            num = random.randint(1, 9) # Generate a random number from 1 to 9
            attempts = 1

            # While the number has not satisfied the sudoku conditions
            while (not row_col_satisfied or not box_satisfied) and attempts < 100:
                attempts += 1

                # Generate a random number from 1 to 9
                num = random.randint(1, 9)
                row_col_satisfied = False
                box_satisfied = True

                # Check if it has satisfied the row and column conditions
                if num not in board[row] and num not in board[:, column]:
                    row_col_satisfied = True
                # Determine which box the cell is in and check if it has met the box condition
                for key in boxes.keys():
                    if (row, column) in boxes[key]:
                        box = key
                for cell in range(9):
                    if num == board[boxes[box][cell][0]][boxes[box][cell][1]]:
                        box_satisfied = False

            # If the last box has been filled out, the sudoku is complete
            if row == 8 and column == 8:
                complete = True

            # If the sudoku gets in a position where there isn't a number that works, start all over again
            if attempts >= 100:
                attempts_exceeded = True
                break

            # Set the cell to the number
            board[row][column] = num

print("Board Created!")

# Have the user indicate their desired difficulty
while True:
    try:
        difficulty = int(input("Enter your desired difficulty (1 - 9): "))
        break
    except:
        pass

# Convert the board to a list
board_final = []
for row in board:
    board_final.append(list(row))

# Randomly remove values from the sudoku with a probability determined by the desired difficulty
for a in range(9):
    for b in range(9):
        num = random.randint(0, 100)
        if num < difficulty * 8:
            board_final[a][b] = ''

# Convert to a DataFrame and export to Excel
board_final = pd.DataFrame(board_final)
board_final.to_excel("sudoku.xlsx", index = None, header=False)
