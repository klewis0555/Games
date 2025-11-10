# import sys
# from random import randint, random, randrange
from prettytable import PrettyTable
from typing import Any, Union

WHITE = "◉"
BLACK = "◎"
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

class Board:
  # Instance Variables
  size: int
  board_dict: dict[str, str] # TODO: Make this private / inaccessible
  column_letters: list[str]
  board_table: PrettyTable # TODO: Make this private / inaccessible

  def __init__(self, size: int=8):
    if size >= 6 and size <= 26 and size%2 == 0:
      self.size = size
    else:
      print(f"Invalid size, setting to {SIZE}.")
      self.size = SIZE
    self.board_dict = {}
    self.initialize_board_dict()
    self.column_letters = self.get_column_letters()
    table_columns = self.column_letters
    table_columns = [" "] + table_columns if SHOW_GUIDES else table_columns
    self.board_table = PrettyTable(table_columns)

  def initialize_board_dict(self) -> None:
    """Initializes the board to the starting state
    """
    for i in range(1, self.size + 1):
      for j in range(1, self.size + 1):
        if i == int(self.size/2) or i == int(self.size/2) + 1:
          if j == int(self.size/2) or j == int(self.size/2) + 1:
            if i == j:
              self.board_dict[f"{chr(64 + i)}{j}"] = BLACK
            else:
              self.board_dict[f"{chr(64 + i)}{j}"] = WHITE
            continue
        
        self.board_dict[f"{chr(64 + i)}{j}"] = DEFAULT
  
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
    
    return [self.board_dict[f"{chr(65 + i)}{row}"] for i in range(self.size)]
  
  def get_column(self, column: str) -> list[str]:
    """Returns a list of the values in the given column

    :param str column: The column to get the values for
      Must be between 'A' and the last column of the board
    :return list[str]: The items in the given column
    """
    column = column.upper()
    if not column in self.column_letters:
      print(f"Invalid column input. Must be between 1 and {self.size}")
      return []
    
    return [self.board_dict[f"{column}{i + 1}"] for i in range(self.size)]
  
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

test_size = 14
c_board = Board(test_size)
print(c_board.get_column('o'))
# import pprint
# pprint.pprint(list(chunks(list(c_board.board_dict.values()), c_board.size)))

