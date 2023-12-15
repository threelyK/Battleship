
import numpy as np
import random
import json
import typing

ship_hp_value = {
    'Aircraft_Carrier': 5,
    'Battleship': 4,
    'Cruiser': 3,
    'Submarine': 3,
    'Destroyer': 2
}


def initialise_board(size: int = 10) -> list[list[None]]:
    """
    :type size: int
    :rtype: list[list[list[None]]]
    :param size: Size of rows and columns for the dimensions of the board
    :return: Returns the board with the inserted dimensions and each square containing 'None' value
    """

    board = []
    row_contents = []
    for i in range(size):
        row_contents.append(None)
    for j in range(size):
        board.append(row_contents.copy())
    return board


def create_battleships(filename: typing.Text = None) -> dict:
    """
    :type filename: typing.Text
    :rtype: dict
    :param filename: Name of the '.txt' file containing a dictionary in the form 'ship_name': hit_points
    :return: Returns the dictionary read from the '.txt' file
    """

    # Default battleship fleet if no other file is used to determine the fleet
    ships = {
        'Destroyer': 2,  # Destroyer
        'Submarine': 3,  # Submarine
        'Cruiser': 3,  # Cruiser
        'Battleship': 4,  # Battleship
        'Aircraft_Carrier': 5  # Aircraft Carrier
    }

    if filename is not None:
        with open(filename) as file:
            ships = eval(file.read())

    return ships


def place_battleships(board, ships, algorithm='simple'):
    # Using a numpy array allows me to slice the board to check if spaces are free
    board = np.array(board)
    match algorithm:
        case 'simple':
            row = 0
            for ship in ships:
                for column in range(ships.get(ship)):
                    board[row, column] = ship
                row += 1

        case 'random':
            # Loop through each ship in the list
            for ship in ships:
                not_placed = True
                ship_len = ships.get(ship)
                while not_placed:
                    # Randomly pick the orientation is vertical or horizontal
                    vertical = random.choice([True, False])
                    index_boundary = len(board) - 1
                    # Randomly pick the coordinates of the starting point
                    row = random.randint(0, index_boundary)
                    col = random.randint(0, index_boundary)
                    row_end = row + ship_len
                    col_end = row + ship_len
                    # print(f"{ship}'s start point: {row}, {col}. Vertical? {vertical}")
                    if board[row, col] is None:
                        # PyLint says to use 'if condition is none' but using 'is None' instead of '== None'
                        # provides a different outcome for np.count_nonzero()
                        if vertical and np.count_nonzero(board[row:row_end, col] == None) == ship_len:
                            board[row:row + ship_len, col] = ship
                            break
                        elif not vertical and np.count_nonzero(board[row, col:col_end] == None) == ship_len:
                            board[row, col:col + ship_len] = ship
                            break
                        else:
                            continue
                    else:
                        continue

        case 'custom':
            with open('placement.json', 'r') as preset:
                placements = json.load(preset)
                if len(placements.keys()) != 5:
                    print("\nDifferent number of ships than expected!")
                    exit()

                for ship in placements:
                    ship_values = placements.get(ship)

                    try:
                        row = int(ship_values[1])
                        col = int(ship_values[0])
                    except ValueError:
                        print("\nInvalid Ship Placement!")
                        exit()

                    ship_len = ship_hp_value.get(ship)
                    row_end = row + ship_len
                    col_end = col + ship_len

                    # PyLint says to use 'if condition is none' but using 'is None' instead of '== None'
                    # provides a different outcome for np.count_nonzero()
                    if ship_values[2] == 'v' and np.count_nonzero(board[row:row_end, col] == None) == ship_len:
                        board[row:row_end, col] = ship
                    elif ship_values[2] == 'h' and np.count_nonzero(board[row, col:col_end] == None) == ship_len:
                        board[row, col:col_end] = ship
                    else:
                        print("Invalid Ship Placement")

    return board.tolist()


def debug_display_current_board(board):
    print("\nCURRENT BOARD STATE:")
    for line in board:
        print(line)


"""
# TEST CODE
test_game = place_battleships(board=initialise_board(10), ships=create_battleships(), algorithm='custom')

debug_display_current_board(test_game)
"""
