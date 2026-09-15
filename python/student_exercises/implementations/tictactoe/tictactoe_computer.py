import random
import os
import time


# ---------- Board Drawing ----------
def draw_board(board: list[str]) -> None:
    """
    Function to draw the tic-tac-toe board.

    Arguments:
    - board (list): List representing the tic-tac-toe board.
    """
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console
    # TODO: Draw the board. PRO TIP: look at the example `tictactoe.310.py`


# ---------- Win Check ----------
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
    return False


# ---------- Computer Strategies ----------
def empty_cells(board: list[str]) -> list[int]:
    """
    Returns a list of indices of empty cells on the board.

    Arguments:
    - board (list): List representing the tic-tac-toe board.

    Returns:
    - empty (list): List of indices of empty cells.
    """
    # TODO: loop through the board and return the indices of empty cells
    return []


def random_choice(board: list[str]) -> int:
    """
    Returns a random index of an empty cell on the board.

    Arguments:
    - board (list): List representing the tic-tac-toe board.

    Returns:
    - index (int): Index of a randomly chosen empty cell.
    """
    # TODO: Use the random.choice function to get an index from the list of empty cells
    return -1


def winning_move(board: list[str], player: str) -> int | None:
    """
    Returns the index of a winning move for the player if available.
    The winning strategy checks if there is a move that allows the player to win in the next turn.
    if no winning move is available, returns None.

    Arguments:
    - board (list): List representing the tic-tac-toe board.
    - player (str): Player's mark ('X' or 'O').

    Returns:
    - index (int | None): Index of the winning move, or None if no winning move is available.
    """
    # TODO: Loop through empty cells, simulate the move, check for win, and return the index if it results in a win
    return None


def blocking_move(board: list[str], player: str) -> int | None:
    """
    Returns the index of a blocking move against the opponent if available.
    The blocking strategy checks if the opponent has a winning move in the next turn and blocks it.
    if no blocking move is available, returns None.

    Arguments:
    - board (list): List representing the tic-tac-toe board.
    - player (str): Player's mark ('X' or 'O').

    Returns:
    - index (int | None): Index of the blocking move, or None if no blocking move is available.
    """
    # TODO: Loop through empty cells, simulate the move, check for a blocking move, and return the index if it results in a blocking
    return None


def center_priority(board: list[str]) -> int | None:
    """
    Returns the index of the center cell if it is empty otherwise None.

    Arguments:
    - board (list): List representing the tic-tac-toe board.

    Returns:
    - index (int | None): Index of the center cell (4), or None if it is not empty.
    """
    # TODO: Check if the center cell (index 4) is empty and return the index or None
    return None


def corner_priority(board: list[str]) -> int | None:
    """
    Returns the index of a random empty corner cell if available otherwise None.

    Arguments:
    - board (list): List representing the tic-tac-toe board.

    Returns:
    - index (int | None): Index of a random empty corner cell, or None if no corners are empty.
    """
    # TODO: Check the corner cells (indices 0, 2, 6, 8) and return a random empty corner index or None
    return None


def computer_move(board: list[str], player: str, strategy: str = "random") -> int:
    if strategy == "random":
        return random_choice(board)
    elif strategy == "win":
        return winning_move(board, player) or random_choice(board)
    elif strategy == "block":
        return blocking_move(board, player) or random_choice(board)
    elif strategy == "win_block":
        return (
            winning_move(board, player)
            or blocking_move(board, player)
            or random_choice(board)
        )
    elif strategy == "center":
        return center_priority(board) or random_choice(board)
    elif strategy == "corners":
        return corner_priority(board) or random_choice(board)
    elif strategy == "rule_based":
        return (
            winning_move(board, player)
            or blocking_move(board, player)
            or center_priority(board)
            or corner_priority(board)
            or random_choice(board)
        )
    else:
        return random_choice(board)


# ---------- Game Loop ----------
def play_game_vs_computer(strategy: str = "random"):
    # The board variable store the state of the game, where board[0] is the top left corner and board[8] is the bottom right corner
    board = [" "] * 9
    human = ...  # TODO: select the human player's mark randomly between 'X' and 'O'
    computer = (
        ...
    )  # TODO: assign the computer player's mark based on the human player's mark 'O' or 'X'
    current_player = "X"
    game_over = False

    print(f"You are {human}, computer is {computer} (strategy = {strategy})")
    time.sleep(1)

    while not game_over:
        # TODO: Draw the board

        if current_player == human:
            # TODO: Get player's move
            # Hint: Use input() to get the move from the player
            move = None

            # TODO: Check if move is valid
            # A valid move is an integer between 1 and 9 (both inclusive)
            # A valid move is a value where the board is empty: " "
            # if move is not valid, print "Invalid move. Try again!" and ask for a new moove
        else:
            print(f"Computer ({strategy}) is thinking...")
            time.sleep(0.5)
            move_index = (
                ...
            )  # TODO: call computer move function to get the computer's move index

        # TODO: Update the board with the move (human or computer)
        # The borad is the list named board that contains state of the game

        # TODO: Check if the current player has won or draw or continue
        # Hint: Use the check_win() function to check if the current player has won
        # You need to think about something for the draw case
        # if no win and no draw the game continues, switch user 'X'->'O' || 'O'->'X'
        # Note: don't forget to say who win (human or computer) or if it's a tie


# ---------- Run ----------
if __name__ == "__main__":
    # Try different strategies: "random", "win", "block", "win_block", "center", "corners", "rule_based"
    play_game_vs_computer(strategy="rule_based")
