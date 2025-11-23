import sys
from typing import Any
from prettytable import PrettyTable
from Othello.othello import Othello

# WHITE = "◉"
# BLACK = "◎"
WHITE = "⚪"
BLACK = "⚫"
# WHITE = "⬤"
# BLACK = "◯"
SIZE = 8
DEFAULT = " "
SHOW_GUIDES = False


# =========================================== starting test code ===========================================
# guides = True
# columns = [" "] if guides else []

# for i in range(SIZE):
#   columns.append(chr(65 + i))

# board = PrettyTable(columns)

# for i in range(SIZE):
#   half = int(SIZE / 2)
#   start = [i + 1] if guides else[]
#   if i == half:
#     board.add_row(start + [DEFAULT] * (half-1) + [WHITE, BLACK] + [DEFAULT] * (half-1), divider=True)
#   elif i+1 == half:
#     board.add_row(start + [DEFAULT] * (half-1) + [BLACK, WHITE] + [DEFAULT] * (half-1), divider=True)
#   else:
#     board.add_row(start + [DEFAULT] * (SIZE), divider=True)

# board.header = guides
# print(board)

# =========================================== ending test code ===========================================

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
  turn = board.Color.BLACK
  skip_count = 0

  board.print_board()

  # x = input(f"It's {turn.name.title()}'s turn! Choose a square: ")
  # print(x)
  while skip_count < 2:
    has_valid_move, moves = board.any_valid_move(turn)
    if has_valid_move:
      move_chosen = False
      while not move_chosen:
        space = input(f"It's {turn.name.title()}'s turn! Choose a square: ")
        if space in moves:
          #implement setting the space
          move_chosen = True
        else:
          print("Invalid move!")
      skip_count = 0
    else:
      print(f"No valid moves for {turn.name.title()}. Skipping turn.")
      skip_count += 1


# run_game()

direction = "upleft"
print("down" in direction)

column = "B"
print(chr(ord(column)-1))

test_size = 20
c_board = Othello(test_size)

c_board.set_square("d1", c_board.Color.BLACK)
c_board.update_board_table()
c_board.print_board()
c_board.toggle_guides()
c_board.print_board()
print(c_board.get_next_space('a1', 'left'))
can_move, spaces = c_board.check_move("k12", c_board.Color.BLACK)
if can_move:
  print(f"Valid move! Spaces: {spaces}")
else:
  print("Invalid move!")
