import sys
# from random import randint, random, randrange
from prettytable import PrettyTable
from typing import Any, Union

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
guides = True
columns = [" "] if guides else []

for i in range(SIZE):
  columns.append(chr(65 + i))

board = PrettyTable(columns)

for i in range(SIZE):
  half = int(SIZE / 2)
  start = [i + 1] if guides else[]
  if i == half:
    board.add_row(start + [DEFAULT] * (half-1) + [WHITE, BLACK] + [DEFAULT] * (half-1), divider=True)
  elif i+1 == half:
    board.add_row(start + [DEFAULT] * (half-1) + [BLACK, WHITE] + [DEFAULT] * (half-1), divider=True)
  else:
    board.add_row(start + [DEFAULT] * (SIZE), divider=True)

board.header = guides
# print(board)


# Function used to break a list down into evenly sized chunks, similar to many `slice`
def chunks(lst: list[Any], n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# =========================================== ending test code ===========================================

class OthelloBoard:
  # Instance Variables
  size: int
  column_letters: list[str]
  _board_dict: dict[str, str] # TODO: Make this private / inaccessible
  _board_table: PrettyTable # TODO: Make this private / inaccessible

  def __init__(self, size: int=8):
    if size >= 6 and size <= 26 and size%2 == 0:
      self.size = size
    else:
      print(f"Invalid size, setting to {SIZE}.")
      self.size = SIZE
    self._board_dict = {}
    self.initialize_board_dict()
    self.column_letters = self.get_column_letters()
    table_columns = self.column_letters
    table_columns = [" "] + table_columns if SHOW_GUIDES else table_columns
    self._board_table = PrettyTable(table_columns)
    self._board_table.header = False
    self.update_board_table()
    # self._board_table.add_rows(
    #   [self.get_row(col) for col in range(1, self.size + 1)]
    # )

  def initialize_board_dict(self) -> None:
    """Initializes the board to the starting state
    """
    for i in range(1, self.size + 1):
      for j in range(1, self.size + 1):
        if i == int(self.size/2) or i == int(self.size/2) + 1:
          if j == int(self.size/2) or j == int(self.size/2) + 1:
            if i == j:
              self._board_dict[f"{chr(64 + i)}{j}"] = BLACK
            else:
              self._board_dict[f"{chr(64 + i)}{j}"] = WHITE
            continue

        self._board_dict[f"{chr(64 + i)}{j}"] = DEFAULT

  def set_square(self, key: str, value: str) -> bool:
    """Sets a single square in the board dictionary. Returns True if successful, False if not

    :param str key: The key to set
    :param str value: The value to set
    :return bool: Returns True if successful, False if not.
    """
    key = key.upper()
    if key in self._board_dict.keys():
      if value in [WHITE, BLACK]:
        self._board_dict[key] = value
        return True

    return False

  def get_square(self, key: str) -> str:
    """Returns the value in the provided square

    :param str key: The square to get the value for
    :return str: The value of the square
    """
    return self._board_dict[key]

  def update_board_table(self) -> None:
    self._board_table.clear_rows()
    for i in range(self.size):
      self._board_table.add_row(self.get_row(i+1), divider=True)

  def print_board(self) -> None:
    """Prints the board
    """
    print(self._board_table)

  def get_column_letters(self) -> list[str]:
    """Return the column letters for the board

    :return list[str]: Column letters for the board
    """
    return [chr(65 + i) for i in range(self.size)]

  def get_row(self, row: int) -> list[str]:
    """Returns a list of the values in the given row

    :param int row: The row to get the values for
      Must be between 1 and the max size of the board
    :return list[str]: The items in the given row
    """
    if row < 1 or row > self.size:
      print(f"Invalid row input. Must be between 1 and {self.size}")
      return []

    return [self._board_dict[f"{chr(65 + i)}{row}"] for i in range(self.size)]

  def get_column(self, column: str) -> list[str]:
    """Returns a list of the values in the given column

    :param str column: The column to get the values for
      Must be between 'A' and the last column of the board
    :return list[str]: The items in the given column
    """
    column = column.upper()
    if not column in self.column_letters:
      print(f"Invalid column input. Must be between A and {self.column_letters[-1]}")
      return []

    return [self._board_dict[f"{column}{i + 1}"] for i in range(self.size)]

  def get_left(self, space: str) -> Union[str, None]:
    """Returns the key of the space to the left of the given space.

    :param str space: The starting space.
    :return Union[str, None]: Returns the key to the space to the left of the given space.
      If given space is column A, return None.
    """

    space = space.upper()
    # TODO: add proper error handling to this method instead of just returning None
    error_message = f"Error!: get_left - Invalid key: {space}"
    if len(space) != 2:
      print(error_message)
      return None
    column, row = list(space)
    row = int(row) # TODO: need error handling around this

    if not column in self.column_letters:
      print(error_message)
      print(f"Column must be in {self.column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    if column == "A":
      return None

    return f"{chr(ord(column)-1)}{row}"

  def get_right(self, space: str) -> Union[str, None]:
    """Returns the key of the space to the right of the given space.

    :param str space: The starting space.
    :return Union[str, None]: Returns the key to the space to the right of the given space.
      If given space is the last column, return None.
    """
    space = space.upper()
    # TODO: add proper error handling to this method instead of just returning None
    error_message = f"Error!: get_right - Invalid key: {space}"
    if len(space) != 2:
      print(error_message)
      return None
    column, row = list(space)
    row = int(row) # TODO: need error handling around this

    if not column in self.column_letters:
      print(error_message)
      print(f"Column must be in {self.column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    if column == self.column_letters[-1]:
      return None

    return f"{chr(ord(column)+1)}{row}"

  def get_above(self, space: str) -> Union[str, None]:
    """Returns the key of the space above the given space.

    :param str space: The starting space.
    :return Union[str, None]: Returns the key to the space above the given space.
      If given space is row 1, return None.
    """
    space = space.upper()
    # TODO: add proper error handling to this method instead of just returning None
    error_message = f"Error!: get_above - Invalid key: {space}"
    if len(space) != 2:
      print(error_message)
      return None
    column, row = list(space)
    row = int(row) # TODO: need error handling around this

    if not column in self.column_letters:
      print(error_message)
      print(f"Column must be in {self.column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    if row == 1:
      return None

    return f"{column}{row-1}"

  def get_below(self, space: str) -> Union[str, None]:
    """Returns the key of the space below the given space.

    :param str space: The starting space.
    :return Union[str, None]: Returns the key to the below above the given space.
      If given space is row 1, return None.
    """
    space = space.upper()
    # TODO: add proper error handling to this method instead of just returning None
    error_message = f"Error!: get_below - Invalid key: {space}"
    if len(space) != 2:
      print(error_message)
      return None
    column, row = list(space)
    row = int(row) # TODO: need error handling around this

    if not column in self.column_letters:
      print(error_message)
      print(f"Column must be in {self.column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    if row == self.size:
      return None

    return f"{column}{row+1}"

  def get_dul(self, space: str) -> Union[str, None]:
    """Returns the key of the space diagonally up and to the left of the given space.
      dul = Diagonally Up Left

    :param str space: The starting space.
      If this is in the top row or first column, return None.
    :return str or None: The key to the space diagonally up and to the left of the given space
    """
    space = space.upper()
    # TODO: add proper error handling to this method instead of just returning None
    error_message = f"Error!: get_dul - Invalid key: {space}"
    if len(space) != 2:
      print(error_message)
      return None
    column, row = list(space)
    row = int(row) # TODO: need error handling around this

    if not column in self.column_letters:
      print(error_message)
      print(f"Column must be in {self.column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    if column == "A" or row == 1:
      return None

    return f"{chr(ord(column)-1)}{row-1}"

  def get_dur(self, space: str) -> Union[str, None]:
    """Returns the key of the space diagonally up and to the right of the given space.
      dur = Diagonally Up right

    :param str space: The starting space.
      If this is in the top row or last column, return None.
    :return str or None: The key to the space diagonally up and to the right of the given space
    """
    space = space.upper()
    # TODO: add proper error handling to this method instead of just returning None
    error_message = f"Error!: get_dur - Invalid key: {space}"
    if len(space) != 2:
      print(error_message)
      return None
    column, row = list(space)
    row = int(row) # TODO: need error handling around this

    if not column in self.column_letters:
      print(error_message)
      print(f"Column must be in {self.column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    if column == self.column_letters[-1] or row == 1:
      return None

    return f"{chr(ord(column)+1)}{row-1}"

  def get_ddl(self, space: str) -> Union[str, None]:
    """Returns the key of the space diagonally down and to the left of the given space.
      ddl = Diagonally Down Left

    :param str space: The starting space.
      If this is in the top row or first column, return None.
    :return str or None: The key to the space diagonally down and to the left of the given space
    """
    space = space.upper()
    # TODO: add proper error handling to this method instead of just returning None
    error_message = f"Error!: get_ddl - Invalid key: {space}"
    if len(space) != 2:
      print(error_message)
      return None
    column, row = list(space)
    row = int(row) # TODO: need error handling around this

    if not column in self.column_letters:
      print(error_message)
      print(f"Column must be in {self.column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    if column == "A" or row == self.size:
      return None

    return f"{chr(ord(column)-1)}{row+1}"

  def get_ddr(self, space: str) -> Union[str, None]:
    """Returns the key of the space diagonally down and to the right of the given space.
      ddl = Diagonally Down Right

    :param str space: The starting space.
      If this is in the top row or first column, return None.
    :return str or None: The key to the space diagonally down and to the right of the given space
    """
    space = space.upper()
    # TODO: add proper error handling to this method instead of just returning None
    error_message = f"Error!: get_ddr - Invalid key: {space}"
    if len(space) != 2:
      print(error_message)
      return None
    column, row = list(space)
    row = int(row) # TODO: need error handling around this

    if not column in self.column_letters:
      print(error_message)
      print(f"Column must be in {self.column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    if column == self.column_letters[-1] or row == self.size:
      return None

    return f"{chr(ord(column)+1)}{row+1}"

  def check_move(self, space: str, color: str) -> tuple[bool, list[str]]:
    space = space.upper()
    if (space not in self._board_dict.keys()) or color not in [WHITE, BLACK] or self.get_square(space) != DEFAULT:
      return False, []

    spaces_to_flip: list[str] = []  # spaces to be flipped if move is valid
    directions = ["left", "right", "above", "below", "dul", "dur", "ddl", "ddr"]

    for direction in directions:
      current_space = space
      working_spaces: list[str] = []  # working list of spaces, only add to final list if valid move
      continue_check = True
      count = 0
      while continue_check and count < 100:
        count += 1
        current_space = getattr(self, f"get_{direction}")(current_space)

        if current_space == None: # edge of board, not valid move
          continue_check = False
        elif self.get_square(current_space) == DEFAULT: # empty space, not a valid move
          continue_check = False
        elif self.get_square(current_space) == color: # flanking with same color, valid move, add working spaces to total list
          spaces_to_flip += working_spaces
          continue_check = False
        else: # opposite color, add to working list and continue
          working_spaces.append(current_space)

    if spaces_to_flip:
      return True, spaces_to_flip
    else:
      return False, spaces_to_flip

  # TODO: Test function
  def any_valid_move(self, color: str) -> tuple[bool, list[str]]:
    valid_spaces: list[str] = []
    for space in self._board_dict.keys():
      if self.check_move(space, color)[0]:
        valid_spaces.append(space)

    return len(valid_spaces) > 0, valid_spaces

def valid_size_input(size_input):
  try:
    int_input = int(size_input)
    if int_input >= 6 and int_input <= 26:
      return True
    else:
      print(f"Invalid input: {int_input}. Must be between 6 and 26.")
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
  board = OthelloBoard(board_size)
  turn = BLACK

run_game()
# test_size = 8
# c_board = OthelloBoard(test_size)

# # c_board.set_square("d1", BLACK)
# c_board.update_board_table()
# c_board.print_board()
# can_move, spaces = c_board.check_move("c3", WHITE)
# if can_move:
#   print(f"Valid move! Spaces: {spaces}")
# else:
#   print("Invalid move!")
# print([c_board.get_row(col) for col in range(1,c_board.size + 1)])
# import pprint
# pprint.pprint(list(chunks(list(c_board._board_dict.values()), c_board.size)))
