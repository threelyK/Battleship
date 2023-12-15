
from components import initialise_board, create_battleships, place_battleships

new_board = initialise_board(10)
fleet = create_battleships()
game_board = place_battleships(board=new_board, ships=fleet, algorithm='random')


def attack(coordinates: tuple, board, battleships) -> bool:
    row = coordinates[0]
    col = coordinates[1]
    print(f"ATK func target: {board[row][col]}")

    if board[row][col] is not None:
        ship = board[row][col]
        ship_hp = battleships.get(ship)
        battleships.update({ship: ship_hp - 1})
        # print(f"Ship: {ship}, Ship HP: {ship_hp}")
        board[row][col] = None
        if ship_hp == 1:
            battleships.pop(ship)
        return True
    else:
        return False
    pass


""" TEST CODE
print("\nBOARD STATE before atk:")
for line in placed_test_board:
    print(line)

for row in range(0, 10):
    for col in range(0, 10):
        attack((row, col), board=placed_test_board, battleships=battleship_dict)

print(f"\n{battleship_dict}")

print("\nBOARD STATE after atk:")
for line in placed_test_board:
    print(line)
"""


def cli_coordinates_input():
    invalid_input = True
    while invalid_input:
        try:
            row_value = int(input("\nWhich row?")) - 1
            col_value = int(input("Which column?")) - 1
            if 0 <= row_value <= 9 and 0 <= col_value <= 9:
                invalid_input = False
            else:
                print("Type an integer between 1-10")
        except ValueError:
            print("Type an integer between 1-10")
    return tuple((row_value, col_value))


def simple_game_loop():
    print("\nWelcome to BATTLESHIP")

    # Board and battleships dictionary are called from outside the function
    while len(fleet) > 0:
        if attack(cli_coordinates_input(), board=game_board, battleships=fleet):
            print("Hit!\n")
            yield game_board
        else:
            print("Miss!\n")
            yield game_board
    print("\nGame Over!")


if __name__ == '__main__':
    for current_board in simple_game_loop():
        pass
