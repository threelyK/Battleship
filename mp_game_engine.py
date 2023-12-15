
from game_engine import attack, cli_coordinates_input
from components import initialise_board, create_battleships, place_battleships
import random

shot_history = []

board_1 = initialise_board(10)
board_2 = board_1.copy()

fleet_1 = create_battleships()
fleet_2 = create_battleships()

player_boards = {'user_board': place_battleships(board_1, ships=fleet_1, algorithm='custom'),
                 'ai_board': place_battleships(board_2, ships=fleet_2, algorithm='random')}


def generate_attack() -> tuple:
    while True:
        row = random.randint(0, 9)  # If board size is not 10x10 this function will not work correctly
        col = random.randint(0, 9)
        shot_space = (row, col)

        if shot_space not in shot_history:  # This makes sure a space is not shot more than once
            shot_history.append(shot_space)
            return shot_space


def ai_opponent_game_loop():
    print("\nWelcome to BATTLESHIP")

    while len(fleet_2) > 0 and len(fleet_1) > 0:
        if attack(cli_coordinates_input(), board=player_boards.get('ai_board'), battleships=fleet_2):
            print("Hit!\n")
            yield player_boards.get('ai_board')
        else:
            print("Miss!\n")
            yield player_boards.get('ai_board')

        if attack(generate_attack(), board=player_boards.get('user_board'), battleships=fleet_1):
            print("Hit!\n")
        else:
            print("Miss\n")

        for line in player_boards.get('user_board'):
            print(line)

        # For debug purposes only
        # print("AI board:")
        # for line in player_boards.get('ai_board'):
        #    print(line)

    if len(fleet_2) == 0:
        print("\nGame Over!, Player Wins")
    else:
        print("\nGame Over!, AI Wins")


if __name__ == '__main__':
    for current_board in ai_opponent_game_loop():
        pass
