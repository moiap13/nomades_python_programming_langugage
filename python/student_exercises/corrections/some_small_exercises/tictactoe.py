import os
import random
import time
# to make animation use time.sleep(<seconds>)

# Function to draw the tic-tac-toe board
def draw_board(board: list[str]):
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


def check_win(board: list[str], player: str) -> bool:
    """
    Function to check if a player has won.
    A player wins if they have 3 consecutive marks in a row, column or diagonal.

    Arguments:
    - board (list): List representing the tic-tac-toe board.
    - player (str): Player's mark ('X' or 'O').

    Returns:
    - win (bool): True if the player has won, False otherwise.
    """
    # return (
    #   board[0] != " " and board[0] == board[1] and board[1] == board[2]
    #   or board[3] != " " and board[3] == board[4] and board[4] == board[5] 
    #   or board[6] != " " and board[6] == board[7] and board[7] == board[8]

    #   or board[0] != " " and board[0] == board[3] and board[3] == board[6] 
    #   or board[1] != " " and board[1] == board[4] and board[4] == board[7] 
    #   or board[2] != " " and board[2] == board[5] and board[5] == board[8] 

    #   or board[0] != " " and board[0] == board[4] and board[4] == board[8] 
    #   or board[2] != " " and board[2] == board[4] and board[4] == board[6] 
    # )
    # return (
    #   board[0] == board[1] == board[2] != " "
    #   or board[3] == board[4] == board[5] != " "
    #   or board[6] == board[7] == board[8] != " "

    #   or board[0] == board[3] == board[6] != " "
    #   or board[1] == board[4] == board[7] != " "
    #   or board[2] == board[5] == board[8] != " "

    #   or board[0] == board[4] == board[8] != " "
    #   or board[2] == board[4] == board[6] != " "
    # )

    combos: list[tuple[int]] = [
      # ROWS
      (0, 1, 2),
      (3, 4, 5),
      (6, 7, 8),

      # COLS
      (0, 3, 6),
      (1, 4, 7),
      (2, 5, 8),

      # DIAGS
      (0, 4, 8),
      (2, 4, 6)
    ]

    for i0, i1, i2 in combos:
      if board[i0] == board[i1] == board[i2] != " ":
         return True
    return False 

# Function to play the game
def play_game():
    # The board variable store the state of the game, where board[0] is the top left corner and board[8] is the bottom right corner
    board: list[str] = [' '] * 9
    current_player: str = 'X' if random.random() > 0.5 else 'O' # random.choice(["X", "O"])
    # the game_over variable is used to know if the game is running or not
    game_over: bool = False

    while not game_over:
        draw_board(board)
        
        # TODO: Get player's move
        # Hint: Use input() to get the move from the player
        try :
            moove: int = int(input(f"{current_player} it's your turn, enter your moove (1-9): "))
        except ValueError:
            print("The input is invalid")
            time.sleep(0.6)
            continue
        
        assert type(moove) == int

        # TODO: Check if move is valid
        # A valid move is an integer between 1 and 9 (both inclusive)
        # And the board for this integer is empty
        # if move is not valid, print "Invalid move. Try again!" and ask for a new moove

        # if (1 <= moove <= 9 and board[moove-1] == " "):
        # if not (1 <= moove and moove <= 9 and board[moove-1] == " "):
        if not (moove in range(1, 9+1) and board[moove-1] == " "):
            print("The moove is invalid")
            time.sleep(0.6)
            continue
            
        assert 1 <= moove <= 9 and board[moove-1] == " " 

        # TODO: Update the board with the move
        # The borad is the list named board that contains state of the game
        board[moove-1] = current_player

        # TODO: Check if the current player has won or draw or continue
        # Hint: Use the check_win() function to check if the current player has won
        # You need to think about something for the draw case
        # if no win and no draw the game continues, switch user 'X'->'O' || 'O'->'X'
        if check_win(board, current_player):
          draw_board(board) 
          print(f"Player {current_player} Won!!")
          game_over = True
        elif " " not in board:
          draw_board(board) 
          print("It's a tie")
          game_over = True
        else:
            current_player = "O" if current_player == "X" else "X"

# Start the game
play_game()
