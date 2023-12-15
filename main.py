
from components import place_battleships, debug_display_current_board, initialise_board
from flask import Flask, render_template, request, jsonify
from mp_game_engine import player_boards, fleet_1, fleet_2, generate_attack
from game_engine import attack
import random
import json

app = Flask(__name__)

app.secret_key = 'juk'
shot_history = []


# Separate function as original generate_attack function is in the form:
# (y,x) or (row, col) instead of the form (x, y) or (col, row)
def generate_attack_xy() -> tuple:
    # print(shot_history)
    while True:
        row = random.randint(0, 9)  # If board size is not 10x10 this function will not work correctly
        col = random.randint(0, 9)
        shot_space = (col, row)

        if shot_space not in shot_history:  # This makes sure a space is not shot more than once
            shot_history.append(shot_space)
            return tuple((row, col))


@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    match request.method:
        case 'GET':
            return render_template('placement.html',
                                   ships=fleet_1,
                                   board_size=len(player_boards.get('user_board')[0])
                                   )
        case 'POST':
            data = request.get_json()
            with open('placement.json', 'w') as preset:
                json.dump(data, preset)

            player_boards.update({'user_board': initialise_board(10)})
            player_boards.update({'user_board': place_battleships(board=player_boards.get('user_board'),
                                                                  ships=fleet_1,
                                                                  algorithm='custom')})

            return player_boards.get('user_board')


@app.route('/', methods=['GET'])
def root():
    match request.method:
        case 'GET':
            return render_template('main.html',
                                   ships=fleet_1,
                                   board_size=len(player_boards.get('user_board')[0]),
                                   player_board=player_boards.get('user_board'),
                                   )


@app.route('/attack', methods=['GET'])
def process_attack():
    match request.method:
        case 'GET':
            x = int(request.args.get('x'))
            y = int(request.args.get('y'))
            # print(player_boards.get('ai_board')[y][x])
            # print(player_boards.get('ai_board')[y][x] is not None)
            # print(f"\nfleet1: {len(fleet_1)}, fleet2: {len(fleet_2)}")
            # print(f"Fleet 1:\n{fleet_1.keys()}")
            # print(f"Fleet 2:\n{fleet_2.keys()}")

            while len(fleet_1) >= 0 and len(fleet_2) >= 0:

                # debug_display_current_board(player_boards.get('ai_board'))
                ai_atk = generate_attack()

                # print(debug_display_current_board(player_boards.get('user_board')))
                print(f"ai atk: {ai_atk}")
                row1 = ai_atk[0]
                col1 = ai_atk[1]
                print(f"row,col {row1},{col1}")
                print(f"Shot at: {player_boards.get('user_board')[row1][col1]}")

                attack(ai_atk, board=player_boards.get('user_board'), battleships=fleet_1)
                print(fleet_1)

                # PROBLEM: When AI is winning it wins 2 turns after its hit the final ship
                # atk function is returning a different board compared to
                # player_boards.get('user_board')[row1][col1]
                if attack((y, x), board=player_boards.get('ai_board'), battleships=fleet_2):

                    if len(fleet_2) == 0:
                        print("PLAYER HAS WON")
                        return jsonify({
                            'hit': True,
                            'AI_Turn': ai_atk,
                            'finished': "Game Over Player Wins"
                        })
                    elif len(fleet_1) == 0:
                        print("AI HAS WON")
                        return jsonify({
                            'hit': True,
                            'AI_Turn': ai_atk,
                            'finished': "Game Over AI Wins"
                        })
                    else:
                        return jsonify({
                            'hit': True,
                            'AI_Turn': ai_atk
                        })

                elif not attack((y, x), board=player_boards.get('ai_board'), battleships=fleet_2):

                    # Attack function board and current_board mismatch
                    if len(fleet_1) == 0:
                        print("AI HAS WON")
                        return jsonify({
                            'hit': False,
                            'AI_Turn': ai_atk,
                            'finished': "Game Over AI Wins"
                        })
                    else:
                        return jsonify({
                            'hit': False,
                            'AI_Turn': ai_atk
                        })


if __name__ == '__main__':
    app.run(debug=True)
