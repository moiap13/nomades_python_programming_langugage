import random
import os
import time


# ---------- Board Drawing ----------
def draw_board(board: list[str]) -> None:
    os.system("cls" if os.name == "nt" else "clear")  # Clear the console
    lines: list[str] = [
        "Tic-Tac-Toe\n",
        "   |   |   ",
        f" {board[0]} | {board[1]} | {board[2]} ",
        "___|___|___",
        "   |   |   ",
        f" {board[3]} | {board[4]} | {board[5]}\t|1|2|3",
        "___|___|___\t------",
        "   |   |\t|4|5|6",
        f" {board[6]} | {board[7]} | {board[8]}\t------",
        "   |   |\t|7|8|9",
    ]
    for line in lines:
        print(line)


# ---------- Win Check ----------
def check_win(board: list[str], player: str) -> bool:
    combos: list[tuple[int]] = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),  # rows
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),  # cols
        (0, 4, 8),
        (6, 4, 2),  # diagonals
    ]
    for combo in combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False


# ---------- Computer Strategies ----------
def empty_cells(board: list[str]) -> list[int]:
    return [i for i, cell in enumerate(board) if cell == " "]


def random_choice(board: list[str]) -> int:
    return random.choice(empty_cells(board))


def winning_move(board: list[str], player: str) -> int | None:
    for i in empty_cells(board):
        board[i] = player
        if check_win(board, player):
            board[i] = " "
            return i
        board[i] = " "
    return None


def blocking_move(board: list[str], player: str) -> int | None:
    opponent = "X" if player == "O" else "O"
    return winning_move(board, opponent)


def center_priority(board: list[str]) -> int | None:
    return 4 if board[4] == " " else None


def corner_priority(board: list[str]) -> int | None:
    corners = [i for i in [0, 2, 6, 8] if board[i] == " "]
    return random.choice(corners) if corners else None


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
    board = [" "] * 9
    human = random.choice(["X", "O"])
    computer = "O" if human == "X" else "X"
    current_player = "X"
    game_over = False

    print(f"You are {human}, computer is {computer} (strategy = {strategy})")

    while not game_over:
        draw_board(board)

        if current_player == human:
            move = input(f"Player {human}, choose (1-9): ")
            move = int(move) if move.isnumeric() else 0
            if not (move in range(1, 10) and board[move - 1] == " "):
                print("Invalid move")
                time.sleep(0.5)
                continue
            move_index = move - 1
        else:
            print(f"Computer ({strategy}) is thinking...")
            time.sleep(0.5)
            move_index = computer_move(board, computer, strategy)

        board[move_index] = current_player

        if check_win(board, current_player):
            draw_board(board)
            print(
                f"{'Computer' if current_player == computer else 'Player'} ({current_player}) wins!"
            )
            game_over = True
        elif " " not in board:
            draw_board(board)
            print("It's a tie!")
            game_over = True
        else:
            current_player = "X" if current_player == "O" else "O"


# ---------- Run ----------
if __name__ == "__main__":
    # Try different strategies: "random", "win", "block", "win_block", "center", "corners", "rule_based"
    play_game_vs_computer(strategy="rule_based")
