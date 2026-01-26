import os
import random
import time

# you can use the time.sleep() function to stop the programs for a certain amount of time in seconds


# Function to draw the tic-tac-toe board
def draw_board(board: list[str]) -> None:
    """
    Function to draw the tic-tac-toe board.

    Arguments:
    - board (list): List representing the tic-tac-toe board.
    """
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console
    # TODO: Draw the board. PRO TIP: look at the example `tictactoe.310.py`
    board_str: str = f"""TitTacToe

   |   |   
 {board[0]} | {board[1]} | {board[2]}
___|___|___
   |   |      
 {board[3]} | {board[4]} | {board[5]}    1|2|3  
___|___|___   -|-|- 
   |   |      4|5|6
 {board[6]} | {board[7]} | {board[8]}    -|-|-
   |   |      7|8|9
"""
    print(board_str)


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
    # if (
    #     (board[0] == board[1] and board[1] == board[2])
    #     or (board[3] == board[4] and board[4] == board[5])
    #     or (board[6] == board[7] and board[7] == board[8])
    #     or (board[0] == board[3] and board[3] == board[6])
    #     or (board[1] == board[4] and board[4] == board[7])
    #     or (board[2] == board[5] and board[5] == board[8])
    #     or (board[0] == board[4] and board[4] == board[8])
    #     or (board[2] == board[4] and board[4] == board[6])
    # ):
    #     return True
    # else:
    #     return False

    # return (
    #     (board[0] == board[1] == board[2] == player)
    #     or (board[3] == board[4] == board[5] == player)
    #     or (board[6] == board[7] == board[8] == player)
    #     or (board[0] == board[3] == board[6] == player)
    #     or (board[1] == board[4] == board[7] == player)
    #     or (board[2] == board[5] == board[8] == player)
    #     or (board[0] == board[4] == board[8] == player)
    #     or (board[2] == board[4] == board[6] == player)
    # )

    combos: list[tuple[int]] = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    for i0, i1, i2 in combos:
        if board[i0] == board[i1] == board[i2] == player:
            return True
    return False


# Function to play the game
def play_game():
    # The board variable store the state of the game, where board[0] is the top left corner and board[8] is the bottom right corner
    board: list[str] = [" "] * 9
    # Initialize the current player randomly between values 'X' and 'O'
    current_player: str = random.choice(["X", "O"])
    # current_player: str =  "X" if random.random() < 0.5 else "O"

    # the game_over variable is used to know if the game is running or not
    game_over: bool = False

    while not game_over:
        # Draw the board
        draw_board(board)

        # Get player's move
        # Hint: Use input() to get the move from the player
        move: int = int(input(f"Player {current_player}: Enter your move (1-9): "))

        # Check if move is valid
        # A valid move is an integer between 1 and 9 (both inclusive)
        # A valid move is a value where the board is empty: " "
        # if move is not valid, print "Invalid move. Try again!" and ask for a new moove

        # if move in range(1, 10):
        # if 1 <= move and move <= 9:
        # if move < 1 or move > 9
        if not (
            1 <= move <= 9 and board[move - 1] == " "
        ):  # we'll enter when move is invalid
            print("Invalid move. Try again!")
            time.sleep(0.3)
            continue

        assert 1 <= move <= 9 and board[move - 1] == " "
        # Update the board with the move
        # The borad is the list named board that contains state of the game
        board[move - 1] = current_player

        # Check if the current player has won or draw or continue
        # Hint: Use the check_win() function to check if the current player has won
        # You need to think about something for the draw case
        # if no win and no draw the game continues, switch user 'X'->'O' || 'O'->'X'
        if check_win(board, current_player):
            draw_board(board)
            game_over = True
            print(f"{current_player} won !!")
        elif " " not in board:
            draw_board(board)
            game_over = True
            print(f"It's a tie")
        else:
            current_player = "X" if current_player == "O" else "O"


# Start the game
if __name__ == "__main__":
    play_game()
