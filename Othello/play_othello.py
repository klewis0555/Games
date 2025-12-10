import sys
from datetime import datetime
from typing import Any
from othello import Othello, SIZE, DEFAULT

LOG_PATH = "Othello/game_logs.txt"

def valid_size_input(size_input: Any) -> bool:
  """Checks if the input is valid (an int between 6 and 26)

  :param Any size_input: Input to check
  :return bool: Returns True if valid input, False if not.
  """
  try:
    int_input = int(size_input)
    if int_input >= 6 and int_input <= 26 and int_input%2 == 0:
      return True
    else:
      print(f"Invalid input: {int_input}. Must be an even integer between 6 and 26.")
  except ValueError:
    print(f"Invalid input: {size_input}. Must be an integer.")
  return False

def opposite_color(color: Othello.Color) -> Othello.Color:
  """Returns the opposite color of the provided parameter

  :param Othello.Color color: White or Black
  :return Othello.Color: The opposite color of the given color
  """
  if color == Othello.Color.WHITE:
    return Othello.Color.BLACK
  elif color == Othello.Color.BLACK:
    return Othello.Color.WHITE
  else:
    raise ValueError("Input must be a member of the Color enum.")

def set_up_logs() -> None:
  """Sets up the log file, clearing any previous logs
  """
  with open(LOG_PATH, "w") as l:
    l.write(f"Time: {datetime.now()}\n\n")

def log_message(message: str) -> None:
  """Writes a log message to the log file.

  :param str message: Message to write to the log file
  """
  with open(LOG_PATH, "a") as l:
    l.write(message)

def run_game():
  board_size = 0
  missing_size = True
  if len(sys.argv) > 1:
    if valid_size_input(sys.argv[1]):
      board_size = int(sys.argv[1])
      missing_size = False
      print(f"Using first argument from command line as size: {board_size}") # because argv[0] is the name of the script

  if missing_size:
    count = 0
    while missing_size and count <= 3:
      size_input = input("Size of board? ")
      if valid_size_input(size_input):
        board_size = int(size_input)
        missing_size = False
      count += 1
  print(f"Running game of Othello with {board_size}x{board_size} board.")
  board = Othello(board_size)
  empty_spaces = (board_size * board_size) - 4
  turn = Othello.Color.BLACK
  skip_count = 0
  move_number = 0
  set_up_logs()

  board.print_board()
  print(empty_spaces)

  while empty_spaces > 0 and skip_count < 2:
    if board.any_valid_move(turn):
      print(f"Open spaces left: {empty_spaces}")
      move_chosen = False
      while not move_chosen:
        space = input(f"It's {turn.name.title()}'s turn! Choose a square: ")
        is_valid, spaces_to_flip = board.check_move(space, turn)
        if is_valid:
          board.set_square(space, turn)
          board.set_squares(spaces_to_flip, turn)
          empty_spaces -= 1
          move_number += 1
          board.print_board()
          move_chosen = True
          log_message(f"{move_number}\t{turn.name.title()}\t{space}\n")
          skip_count = 0
        else:
          print("Invalid square, please select again.")
    else:
      print(f"No valid moves for {turn.name.title()}. Skipping turn.")
      skip_count += 1
      log_message(f"{turn.name.title()} skips")

    turn = opposite_color(turn)

  if skip_count >= 2:
    print("No more valid moves. Game over!")
  else:
    print("All spaces filled. Game Over!")

  white_spaces = 0
  black_spaces = 0
  for space in board._board_dict.values():
    if space == Othello.Color.BLACK.value:
      black_spaces += 1
    elif space == Othello.Color.WHITE.value:
      white_spaces += 1

  print(f"Black: {black_spaces} | White: {white_spaces}")

  if white_spaces > black_spaces:
    print("========================WHITE WINS!!!========================")
  elif black_spaces > white_spaces:
    print("========================BLACK WINS!!!========================")
  else:
    print("========================IT'S A TIE!!!========================")

run_game()
