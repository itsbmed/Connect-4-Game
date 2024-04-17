import random
import os

class bcolors:
    OKGREEN = '\33[33m'
    WARNING = '\33[35m'
    ENDC = '\033[0m'

possibleLetters = ["A", "B", "C", "D", "E", "F", "G"]
gameBoard = [["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""],
             ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""]]
rows = 6
cols = 7
pl1 = "X"
pl2 = "O"

def printGameBoard():
    print("\n      A     B     C     D     E     F     G  ", end="")
    for x in range(rows):
        print("\n   +-----+-----+-----+-----+-----+-----+-----+")
        print(x, " |", end="")
        for y in range(cols):
            if gameBoard[x][y] == "X":
                # Print "X" in red color
                print(f" {bcolors.OKGREEN}{bcolors.WARNING}{gameBoard[x][y]} {bcolors.ENDC} |", end="")
            elif gameBoard[x][y] == "O":
                # Print "O" in yellow color
                print(f" {bcolors.OKGREEN}{bcolors.OKGREEN}{gameBoard[x][y]} {bcolors.ENDC} |", end="")
            else:
                # Print empty space
                print(f"  {gameBoard[x][y]}  |", end="")
    print("\n   +-----+-----+-----+-----+-----+-----+-----+")

def isFull(board, col):
    for row in range(rows - 1, -1, -1):
        if board[row][col] == "":
            return row
    return -1

def settingGame(board, col, turn):
    row = isFull(board, col)
    if row != -1:
        if turn == 0:
            board[row][col] = pl1
        else:
            board[row][col] = pl2
        return True
    else:
        print("Die Kolumne ist voll!")
        return False


def errorCheck(input_letter):
    while input_letter.upper() not in possibleLetters:
        print("Bitte geben Sie einen Buchstaben zwischen A und G ein.")
        input_letter = input("Versuchen Sie es erneut: ")
    return input_letter.upper()

def check_winner(board, col, row):
    current_player = board[row + 1][col]
    
    for c in range(cols - 3):
        if all(board[row + 1][c+i] == current_player for i in range(4)):
            return True

    for r in range(rows - 3):
        if all(board[r+i][col] == current_player for i in range(4)):
            return True

    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r+i][c+i] == current_player for i in range(4)):
                return True
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r-i][c+i] == current_player for i in range(4)):
                return True
    return False

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == "":
                return False 
    return True 

def replay_game():
    replay = input(bcolors.OKGREEN + "Möchten Sie noch einmal spielen? (ja/nein): " + bcolors.ENDC).lower()
    return replay == "ja"

def get_player_type(player_num):
    while True:
        player_type = input(f"Spieler {player_num}, wählen Sie den Gegnertyp (menschlich (1)/computer (2)): ").lower()
        if player_type == "1" or player_type == "2":
            return player_type
        else:
            print("Ungültige Auswahl. Bitte wählen Sie 'menschlich (1)' oder 'computer (2)'.")

def is_human_player(player_type):
    return player_type == "1"

def get_player_move(player_num):
    if is_human_player(player_types[player_num - 1]):
        while True:
            player_input = input(f"Spieler {player_num}, wählen Sie Ihre Spalte (A-G): ").upper()
            if player_input in possibleLetters:
                return player_input
            else:
                print("Ungültige Eingabe. Bitte geben Sie einen Buchstaben zwischen A und G ein.")
    else:
        col = computer_move(gameBoard)
        return possibleLetters[col]

def computer_move(board):
    for col in range(cols):
        if isFull(board, col) != -1:
            simulated_board = [row[:] for row in board]
            if settingGame(simulated_board, col, "O"): 
                if check_winner(simulated_board, col, isFull(simulated_board, col)):
                    return col  

    for col in range(cols):
        if isFull(board, col) != -1:
            simulated_board = [row[:] for row in board]
            if settingGame(simulated_board, col, "X"): 
                if check_winner(simulated_board, col, isFull(simulated_board, col)):
                    return col  

    while True:
        col = random.randint(0, cols - 1)
        if isFull(board, col) != -1:
            return col 

def handle_player_turn(player_num, board):
    if is_human_player(player_types[player_num - 1]):
        # Human player's turn
        while True:
            player_input = get_player_move(player_num)
            if player_input in possibleLetters:
                player_col = possibleLetters.index(player_input)
                if settingGame(board, player_col, player_num - 1):
                    break
            else:
                print("Ungültige Eingabe. Bitte geben Sie einen Buchstaben zwischen A und G ein.")
    else:
        # Computer player's turn
        player_col = computer_move(board)
        settingGame(board, player_col, player_num - 1)

    clear()
    printGameBoard()

    if check_winner(board, player_col, isFull(board, player_col)):
        clear()
        printGameBoard()
        if is_human_player(player_types[player_num - 1]):
            print(f"Spieler {player_num} gewinnt!")
        else:
            print(f"Computer {player_num} gewinnt!")
        return True

    if is_board_full(board):
        clear()
        printGameBoard()
        print("Es ist eine Zeichnung! Das Spielfeld ist voll.")
        return True

    return False

def initialize_players():
    player_types = []
    for i in range(1, 3):
        player_type = get_player_type(i)
        player_types.append(player_type)
    return player_types

while True:
    gameBoard = [["", "", "", "", "", "", ""] for _ in range(rows)]
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()

    player_types = initialize_players()
    Gameover = False

    while not Gameover:
        clear()
        printGameBoard()

        # Player 1's turn
        if handle_player_turn(1, gameBoard):
            Gameover = True
            break

        # Player 2's turn
        if handle_player_turn(2, gameBoard):
            Gameover = True
            break

    if not replay_game():
        print(bcolors.WARNING + "Vielen Dank fürs Spielen!" + bcolors.ENDC)
        break