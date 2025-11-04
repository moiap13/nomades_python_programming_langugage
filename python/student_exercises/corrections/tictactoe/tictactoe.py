import os
import time

# Function to draw the tic-tac-toe board
def draw_board(board):
    """
    Function to draw the tic-tac-toe board.

    Arguments:
    - board (list): List representing the tic-tac-toe board.
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    
    print("Tic-Tac-Toe\n")
    print("   |   |   ")
    print(" {} | {} | {} ".format(board[0], board[1], board[2]))
    print("___|___|___")
    print("   |   |   ")
    print(" {} | {} | {} \t|1|2|3".format(board[3], board[4], board[5]))
    print("___|___|___\t------")
    print("   |   |    \t|4|5|6")
    print(" {} | {} | {} \t------".format(board[6], board[7], board[8]))
    print("   |   |   \t|7|8|9\n")
# def draw_board(board):
#     """
#     Function to draw the tic-tac-toe board.

#     Arguments:
#     - board (list): List representing the tic-tac-toe board.
#     """
#     os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
#     # TODO: Draw the board. PRO TIP: look at the example `tictactoe.310.pyo`
#     for a in range(9):
#         print(f" {board[a]} ", end="")
#         if a % 3 != 2:
#             print("|", end="")
#         if a%3 == 2:
#             print()
#             if a < 8:
#                 print("---|---|---")

def check_win(board: list, player: str) -> bool:
    """
    Function to check if a player has won.
    A player wins if they have 3 consecutive marks in a row, column or diagonal.

    Arguments:
    - board (list): List representing the tic-tac-toe board.
    - player (str): Player's mark ('X' or 'O').

    Returns:
    - win (bool): True if the player has won, False otherwise.
    """

    # return board[0] == board[1] == board[2] == player \
    #   or board[3] == board[4] == board[5] == player \
    #   or board[6] == board[7] == board[8] == player \
    #   or board[0] == board[3] == board[6] == player \
    #   or board[1] == board[4] == board[7] == player \
    #   or board[2] == board[5] == board[8] == player \
    #   or board[0] == board[4] == board[8] == player \
    #   or board[2] == board[4] == board[6] == player 

    # a mediter
    # if board[0] == board[4] == board[8] == player \
    #   or board[2] == board[4] == board[6] == player:
    #     return True
    
    # for i in [0,1,2]:
    #     if(board[i] == board[i+1] == board[i+2] == player):
    #         return True 
    #     if(board[i] == board[i+3] == board[i+6] == player):
    #         return True 
    # return False

    # for i in range(0, 9, 3):
    #     if board[i] == board[i+1] == board[i+2] == player:
    #         return True
        
    # for i in range(3):
    #     if board[i] == board[i+3] == board[i+6] == player:
    #         return True
        
    # if board[0] == board[4] == board[8] == player \
    #   or board[2] == board[4] == board[6] == player:
    #     return True
    # possibilities = [
    #     [0, 1, 2],+
    #     [3, 4, 5],
    #     [6, 7, 8],
    #     [0, 3, 6], 
    #     [1, 4, 7], 
    #     [2, 5, 8], 
    #     [0, 4, 8], 
    #     [2, 4, 6]
    # ]

    # for possibility in possibilities:
    #     if board[possibility[0]] == board[possibility[1]] == board[possibility[2]] == player:
    #         return True
    # return False

    possibilities = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6), 
        (1, 4, 7), 
        (2, 5, 8), 
        (0, 4, 8), 
        (2, 4, 6)
    ]

    # this also works with tuples
    # for possibility in possibilities:
    #     if board[possibility[0]] == board[possibility[1]] == board[possibility[2]] == player:
    #         return True
    # return False

    for val1, val2, val3 in possibilities:
        if board[val1] == board[val2] == board[val3] == player:
            return True
    return False

# Function to play the game
def play_game():
    # The board variable store the state of the game, where board[0] is the top left corner and board[8] is the bottom right corner
    board = [' '] * 9
    current_player = "X"
    # the game_over variable is used to know if the game is running or not
    game_over = False

    while not game_over:
        # TODO: Draw the board
        draw_board(board)

        # TODO: Get player's move
        # Hint: Use input() to get the move from the player
        move: int = int(input(f"Player {current_player}: Enter your move (1-9): "))
        assert type(move) == int

        # TODO: Check if move is valid
        # A valid move is an integer between 1 and 9 (both inclusive)
        # A valid move is a value where the board is empty: " "
        # if move is not valid, print "Invalid move. Try again!" and ask for a new moove
        if  not (1 <= move <= 9) or board[move-1] != " ":
            # moove is invalid
            print("Move invalid, please try again")
            time.sleep(0.6)
            continue

        # TODO: Update the board with the move
        # The borad is the list named board that contains state of the game
        board[move-1] = current_player
        
        # TODO: Check if the current player has won or draw or continue
        # Hint: Use the check_win() function to check if the current player has won
        # You need to think about something for the draw case
        if check_win(board, current_player):
            draw_board(board)
            print(f"Bravo! {current_player} won")
            game_over = True
        elif not " " in board:
            draw_board(board)
            print("it's a tie!")
            game_over = True 
        else:  
          # if no win and no draw the game continues, switch user 'X'->'O' || 'O'->'X'
          current_player = "O" if current_player == "X" else "X"

          # if current_player == "X":
          #     current_player = "O"
          # else:
          #     current_player = "X"
# Start the game
play_game()
