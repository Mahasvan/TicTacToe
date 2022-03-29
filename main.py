import subprocess
import sys

import algo


def clear_screen():
    subprocess.run(["clear||cls"], shell=True)


settings = {
    "player_char": "x",
    "grid_size": 3,
}


def change_setting():
    quit = False
    while not quit:
        print()
        print("Available settings")
        for key, value in settings.items():
            print(f"{key} - {value}")
        print("\n")
        key_to_change = input("Enter key to change:")
        if key_to_change in settings:
            new_value = input(f"Enter new value for {key_to_change}:")
            settings[key_to_change] = new_value
        else:
            print("Invalid key")
        choice = input("Change another setting? (y/n)")
        if choice.lower() == "n":
            quit = True
        clear_screen()


clear_screen()
print("Welcome to the TicTacToe!")
print("You can exit the program at any time by typing 'exit'.")
print("Input formats accepted: `x,y` where x and y are the row and column of the desired move: 1,2 or 2,3 etc...\n")

while True:
    print("[Enter]: Start game\nS. Settings\nQ. Quit")
    choice = input(">> ")

    if choice.lower() == "s":
        clear_screen()
        change_setting()
    elif choice.lower() == "q":
        sys.exit()
    else:  # Start game
        break
clear_screen()

try:
    tictactoe = algo.TicTacToe(int(settings.get("grid_size", 3)), settings.get("player_char", "x"))
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

    tictactoe.calculate_bot_move()
    tictactoe.print_board()
    if tictactoe.check_game_over():
        print(tictactoe.check_game_over())
        break
