import json
import subprocess
import sys

import algo


def clear_screen():
    subprocess.run(["clear||cls"], shell=True)


settings = json.load(open("config.json"))

clear_screen()
print("Welcome to the TicTacToe!")
print("You can exit the program at any time by typing 'exit'.")
print("Input formats accepted: `x,y` where x and y are the row and column of the desired move: `1,2` or `2,3` etc...\n")

input("Press enter to start the game...")
clear_screen()

if not settings.get("mode"):
    mode = input("Enter the desired difficulty level (easy/hard): ")
else:
    mode = settings.get("mode")
if mode.lower() not in ["easy", "hard"]:
    print("Invalid input! Defaulting to hard mode.")
    mode = "hard"

try:
    tictactoe = algo.TicTacToe(int(settings.get("grid_size", 3)), settings.get("player_char", "X"), mode=mode)
except ValueError:
    print("Invalid grid size")
    sys.exit()

tictactoe.print_board()

while True:
    user_move = input("Enter your move: row,column: ")
    if user_move == "exit":
        break
    try:
        user_move = [int(x) for x in user_move.split(",")]
        if any([len(user_move) != 2, [int(x) for x in user_move] != list(user_move)]):
            print("Invalid input format. Please try again.")
            continue
    except ValueError:
        print("Invalid input format. Please try again.")
        continue
    user_move = [user_move[x] - 1 for x in range(len(user_move))]
    if tictactoe.check_placement(user_move[0], user_move[1]):
        tictactoe.place_piece(tictactoe.player_turn, user_move[0], user_move[1])
    else:
        print("Invalid move!")
        continue

    clear_screen()

    if tictactoe.check_game_over():
        tictactoe.print_board()
        print(tictactoe.check_game_over())
        break

    tictactoe.calculate_bot_move(auto_place=True)
    tictactoe.print_board()
    if tictactoe.check_game_over():
        print(tictactoe.check_game_over())
        break
