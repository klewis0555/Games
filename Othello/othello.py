# import sys
from enum import Enum
from prettytable import PrettyTable
from typing import Union

SIZE = 8
DEFAULT = " "

class Othello:
  class Color(Enum):
    WHITE = "⚪"
    BLACK = "⚫"

  # Instance Variables
  size: int
  column_letters: list[str]
  _board_dict: dict[str, Color] # TODO: Make this private / inaccessible
  _board_table: PrettyTable # TODO: Make this private / inaccessible

  def __init__(self, size: int=8):
    if type(size) == int and (size >= 6 and size <= 26 and size%2 == 0):
      self.size = size
    else:
      print(f"Invalid size, setting to {SIZE}.")
      self.size = SIZE
    self._show_guides = True
    self._board_dict = {}
    self.initialize_board_dict()
    self.column_letters = self.get_column_letters()
    table_columns = self.column_letters
    self._board_table = PrettyTable(table_columns)
    self.update_board_table()

  def initialize_board_dict(self) -> None:
    """Initializes the board to the starting state
    """
    for i in range(1, self.size + 1):
      for j in range(1, self.size + 1):
        if i == int(self.size/2) or i == int(self.size/2) + 1:
          if j == int(self.size/2) or j == int(self.size/2) + 1:
            if i == j:
              self._board_dict[f"{chr(64 + i)}{j}"] = self.Color.WHITE.value
            else:
              self._board_dict[f"{chr(64 + i)}{j}"] = self.Color.BLACK.value
            continue

        self._board_dict[f"{chr(64 + i)}{j}"] = DEFAULT

  def get_column_letters(self) -> list[str]:
    """Return the column letters for the board

    :return list[str]: Column letters for the board
    """
    start = [DEFAULT] if self._show_guides else []
    return start + [chr(65 + i) for i in range(self.size)]

  def update_board_table(self) -> None:
    """Updates the board table with the values in the board dictionary
    """
    self._board_table.clear()
    self._board_table.header = self._show_guides
    self._board_table.field_names = self.get_column_letters()
    for i in range(self.size):
      start = [i + 1] if self._show_guides else []
      self._board_table.add_row(start + self.get_row(i+1), divider=True)

  def set_square(self, key: str, color: Color) -> bool:
    """Sets a single square in the board dictionary to a color. Returns True if successful, False if not

    :param str key: The key to set
    :param str color: The color to set
    :return bool: Returns True if successful, False if not.
    """
    key = key.upper()
    if key in self._board_dict.keys():
      if color in self.Color:
        self._board_dict[key] = color.value
        self.update_board_table()
        return True

    return False

  def set_squares(self, keys: list[str], color: Color) -> bool:
    """Sets multiple squares in the board dictionary to a color. Returns True if successful, False if not

    :param list[str] keys: The keys to set
    :param Color color: The color to set
    :return bool: Returns True if successful, False if not.
    """
    valid = True
    for key in keys:
      key = key.upper()
      if key in self._board_dict.keys():
        if color in self.Color:
          self._board_dict[key] = color.value
        else:
          valid = False
      else:
        valid = False

    self.update_board_table()
    return valid

  def get_square(self, key: str) -> str:
    """Returns the value in the provided square

    :param str key: The square to get the value for
    :return str: The value of the square
    """
    try:
      return self._board_dict[key.upper()]
    except KeyError:
      print("Invalid square. Not in board.")
      return None

  def toggle_guides(self) -> None:
    """Toggles the guides of the board table and refreshes the board.
    """
    self._show_guides = not self._show_guides
    self.update_board_table()

  def print_board(self) -> None:
    """Prints the board
    """
    print(self._board_table)

  def get_row(self, row: int) -> list[str]:
    """Returns a list of the values in the given row

    :param int row: The row to get the values for
      Must be between 1 and the max size of the board
    :return list[str]: The items in the given row
    """
    try:
      row = int(row)
    except ValueError:
      print("Invalid row input. Must be Integer")
      return []

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
    try:
      column = str(column)
    except ValueError:
      print("Invalid row input. Must be String")
      return []

    column = column.upper()
    if (not column in self.column_letters) or column == DEFAULT:
      print(f"Invalid column input. Must be between A and {self.column_letters[-1]}")
      return []

    return [self._board_dict[f"{column}{i + 1}"] for i in range(self.size)]

  # def get_left(self, space: str) -> Union[str, None]:
  #   """Returns the key of the space to the left of the given space.

  #   :param str space: The starting space.
  #   :return Union[str, None]: Returns the key to the space to the left of the given space.
  #     If given space is column A, return None.
  #   """

  #   space = space.upper()
  #   # TODO: add proper error handling to this method instead of just returning None
  #   error_message = f"Error!: get_left - Invalid key: {space}"
  #   if len(space) != 2:
  #     print(error_message)
  #     return None
  #   column, row = list(space)
  #   row = int(row) # TODO: need error handling around this

  #   if not column in self.column_letters:
  #     print(error_message)
  #     print(f"Column must be in {self.column_letters}")
  #     return None

  #   if row < 1 or row > self.size:
  #     print(error_message)
  #     print(f"Row must be between 1 and {self.size}")
  #     return None

  #   if column == "A":
  #     return None

  #   return f"{chr(ord(column)-1)}{row}"

  # def get_right(self, space: str) -> Union[str, None]:
  #   """Returns the key of the space to the right of the given space.

  #   :param str space: The starting space.
  #   :return Union[str, None]: Returns the key to the space to the right of the given space.
  #     If given space is the last column, return None.
  #   """
  #   space = space.upper()
  #   # TODO: add proper error handling to this method instead of just returning None
  #   error_message = f"Error!: get_right - Invalid key: {space}"
  #   if len(space) != 2:
  #     print(error_message)
  #     return None
  #   column, row = list(space)
  #   row = int(row) # TODO: need error handling around this

  #   if not column in self.column_letters:
  #     print(error_message)
  #     print(f"Column must be in {self.column_letters}")
  #     return None

  #   if row < 1 or row > self.size:
  #     print(error_message)
  #     print(f"Row must be between 1 and {self.size}")
  #     return None

  #   if column == self.column_letters[-1]:
  #     return None

  #   return f"{chr(ord(column)+1)}{row}"

  # def get_above(self, space: str) -> Union[str, None]:
  #   """Returns the key of the space above the given space.

  #   :param str space: The starting space.
  #   :return Union[str, None]: Returns the key to the space above the given space.
  #     If given space is row 1, return None.
  #   """
  #   space = space.upper()
  #   # TODO: add proper error handling to this method instead of just returning None
  #   error_message = f"Error!: get_above - Invalid key: {space}"
  #   if len(space) != 2:
  #     print(error_message)
  #     return None
  #   column, row = list(space)
  #   row = int(row) # TODO: need error handling around this

  #   if not column in self.column_letters:
  #     print(error_message)
  #     print(f"Column must be in {self.column_letters}")
  #     return None

  #   if row < 1 or row > self.size:
  #     print(error_message)
  #     print(f"Row must be between 1 and {self.size}")
  #     return None

  #   if row == 1:
  #     return None

  #   return f"{column}{row-1}"

  # def get_below(self, space: str) -> Union[str, None]:
  #   """Returns the key of the space below the given space.

  #   :param str space: The starting space.
  #   :return Union[str, None]: Returns the key to the below above the given space.
  #     If given space is row 1, return None.
  #   """
  #   space = space.upper()
  #   # TODO: add proper error handling to this method instead of just returning None
  #   error_message = f"Error!: get_below - Invalid key: {space}"
  #   if len(space) != 2:
  #     print(error_message)
  #     return None
  #   column, row = list(space)
  #   row = int(row) # TODO: need error handling around this

  #   if not column in self.column_letters:
  #     print(error_message)
  #     print(f"Column must be in {self.column_letters}")
  #     return None

  #   if row < 1 or row > self.size:
  #     print(error_message)
  #     print(f"Row must be between 1 and {self.size}")
  #     return None

  #   if row == self.size:
  #     return None

  #   return f"{column}{row+1}"

  # def get_dul(self, space: str) -> Union[str, None]:
  #   """Returns the key of the space diagonally up and to the left of the given space.
  #     dul = Diagonally Up Left

  #   :param str space: The starting space.
  #     If this is in the top row or first column, return None.
  #   :return str or None: The key to the space diagonally up and to the left of the given space
  #   """
  #   space = space.upper()
  #   # TODO: add proper error handling to this method instead of just returning None
  #   error_message = f"Error!: get_dul - Invalid key: {space}"
  #   if len(space) != 2:
  #     print(error_message)
  #     return None
  #   column, row = list(space)
  #   row = int(row) # TODO: need error handling around this

  #   if not column in self.column_letters:
  #     print(error_message)
  #     print(f"Column must be in {self.column_letters}")
  #     return None

  #   if row < 1 or row > self.size:
  #     print(error_message)
  #     print(f"Row must be between 1 and {self.size}")
  #     return None

  #   if column == "A" or row == 1:
  #     return None

  #   return f"{chr(ord(column)-1)}{row-1}"

  # def get_dur(self, space: str) -> Union[str, None]:
  #   """Returns the key of the space diagonally up and to the right of the given space.
  #     dur = Diagonally Up right

  #   :param str space: The starting space.
  #     If this is in the top row or last column, return None.
  #   :return str or None: The key to the space diagonally up and to the right of the given space
  #   """
  #   space = space.upper()
  #   # TODO: add proper error handling to this method instead of just returning None
  #   error_message = f"Error!: get_dur - Invalid key: {space}"
  #   if len(space) != 2:
  #     print(error_message)
  #     return None
  #   column, row = list(space)
  #   row = int(row) # TODO: need error handling around this

  #   if not column in self.column_letters:
  #     print(error_message)
  #     print(f"Column must be in {self.column_letters}")
  #     return None

  #   if row < 1 or row > self.size:
  #     print(error_message)
  #     print(f"Row must be between 1 and {self.size}")
  #     return None

  #   if column == self.column_letters[-1] or row == 1:
  #     return None

  #   return f"{chr(ord(column)+1)}{row-1}"

  # def get_ddl(self, space: str) -> Union[str, None]:
  #   """Returns the key of the space diagonally down and to the left of the given space.
  #     ddl = Diagonally Down Left

  #   :param str space: The starting space.
  #     If this is in the top row or first column, return None.
  #   :return str or None: The key to the space diagonally down and to the left of the given space
  #   """
  #   space = space.upper()
  #   # TODO: add proper error handling to this method instead of just returning None
  #   error_message = f"Error!: get_ddl - Invalid key: {space}"
  #   if len(space) != 2:
  #     print(error_message)
  #     return None
  #   column, row = list(space)
  #   row = int(row) # TODO: need error handling around this

  #   if not column in self.column_letters:
  #     print(error_message)
  #     print(f"Column must be in {self.column_letters}")
  #     return None

  #   if row < 1 or row > self.size:
  #     print(error_message)
  #     print(f"Row must be between 1 and {self.size}")
  #     return None

  #   if column == "A" or row == self.size:
  #     return None

  #   return f"{chr(ord(column)-1)}{row+1}"

  # def get_ddr(self, space: str) -> Union[str, None]:
    # """Returns the key of the space diagonally down and to the right of the given space.
    #   ddl = Diagonally Down Right

    # :param str space: The starting space.
    #   If this is in the top row or first column, return None.
    # :return str or None: The key to the space diagonally down and to the right of the given space
    # """
    # space = space.upper()
    # # TODO: add proper error handling to this method instead of just returning None
    # error_message = f"Error!: get_ddr - Invalid key: {space}"
    # if len(space) != 2:
    #   print(error_message)
    #   return None
    # column, row = list(space)
    # row = int(row) # TODO: need error handling around this

    # if not column in self.column_letters:
    #   print(error_message)
    #   print(f"Column must be in {self.column_letters}")
    #   return None

    # if row < 1 or row > self.size:
    #   print(error_message)
    #   print(f"Row must be between 1 and {self.size}")
    #   return None

    # if column == self.column_letters[-1] or row == self.size:
    #   return None

    # return f"{chr(ord(column)+1)}{row+1}"

  def get_next_space(self, space: str, direction: str) -> Union[str, None]:
    space = space.upper()
    error_message = f"Error!: Invalid key: {space}"
    if len(space) != 2 and len(space) != 3:
      print(error_message)
      return None
    column = list(space)[0]
    row = int(''.join(list(space)[1:])) # TODO: need error handling around this

    valid_column_letters = [letter for letter in self.column_letters if letter != DEFAULT]
    if not column in valid_column_letters:
      print(error_message)
      print(f"Column must be in {valid_column_letters}")
      return None

    if row < 1 or row > self.size:
      print(error_message)
      print(f"Row must be between 1 and {self.size}")
      return None

    direction = direction.lower()
    valid_directions = ["left", "right", "up", "down", "upleft", "upright", "downleft", "downright"]
    if direction not in valid_directions:
      print (f"Error!: Invalid direction: {direction}")
      print(f"Directions must be in {valid_directions}")
      return None

    if "left" in direction:
      if column == "A":
        return None
      else:
        column = chr(ord(column)-1)
    elif "right" in direction:
      if column == valid_column_letters[-1]:
        return None
      else:
        column = chr(ord(column)+1)

    if "up" in direction:
      if row == 1:
        return None
      else:
        row -= 1
    elif "down" in direction:
      if row == self.size:
        return None
      else:
        row += 1

    return f"{column}{row}"

  def check_move(self, space: str, color: Color) -> tuple[bool, list[str]]:
    """Checks if given space is a valid move for given color (will flank with a piece with a matching color)

    :param str space: Space to check validity of move
    :param Color color: Color to check if valid move
    :return tuple[bool, list[str]]: Boolean of whether the move is valid or not,
      and a list of spaces to flip if a piece were placed there.
    """
    space = space.upper()
    if (space not in self._board_dict.keys()) or color not in self.Color or self.get_square(space) != DEFAULT:
      return False, []

    spaces_to_flip: list[str] = []  # spaces to be flipped if move is valid
    # directions = ["left", "right", "above", "below", "dul", "dur", "ddl", "ddr"]
    directions = ["left", "right", "up", "down", "upleft", "upright", "downleft", "downright"]

    for direction in directions:
      current_space = space
      working_spaces: list[str] = []  # working list of spaces, only add to final list if valid move
      continue_check = True
      count = 0
      while continue_check and count < 100:
        count += 1
        # current_space = getattr(self, f"get_{direction}")(current_space)
        current_space = self.get_next_space(current_space, direction)

        if current_space == None: # edge of board, not valid move
          continue_check = False
        elif self.get_square(current_space) == DEFAULT: # empty space, not a valid move
          continue_check = False
        elif self.get_square(current_space) == color.value: # flanking with same color, valid move
          spaces_to_flip += working_spaces # add working spaces to total list
          continue_check = False
        else: # opposite color, add to working list and continue
          working_spaces.append(current_space)

    if spaces_to_flip:
      return True, spaces_to_flip
    else:
      return False, spaces_to_flip

  def any_valid_move(self, color: Color) -> tuple[bool, list[str]]:
    """Loops through all spaces on the board to check if there are any valid moves for the given color.

    :param Color color: Color to check valid moves for
    :return tuple[bool, list[str]]: A boolean of whether there are any valid moves, and a list of valid spaces.
    """
    valid_spaces: list[str] = []
    for space in self._board_dict.keys():
      if self.check_move(space, color)[0]:
        valid_spaces.append(space)

    return len(valid_spaces) > 0, valid_spaces
