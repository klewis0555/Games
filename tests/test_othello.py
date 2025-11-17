import pytest
from Othello.othello import Othello, DEFAULT, SIZE
from prettytable import PrettyTable

default_board_dict = {
  "A1": DEFAULT,
  "A2": DEFAULT,
  "A3": DEFAULT,
  "A4": DEFAULT,
  "A5": DEFAULT,
  "A6": DEFAULT,
  "B1": DEFAULT,
  "B2": DEFAULT,
  "B3": DEFAULT,
  "B4": DEFAULT,
  "B5": DEFAULT,
  "B6": DEFAULT,
  "C1": DEFAULT,
  "C2": DEFAULT,
  "C3": Othello.Color.WHITE.value,
  "C4": Othello.Color.BLACK.value,
  "C5": DEFAULT,
  "C6": DEFAULT,
  "D1": DEFAULT,
  "D2": DEFAULT,
  "D3": Othello.Color.BLACK.value,
  "D4": Othello.Color.WHITE.value,
  "D5": DEFAULT,
  "D6": DEFAULT,
  "E1": DEFAULT,
  "E2": DEFAULT,
  "E3": DEFAULT,
  "E4": DEFAULT,
  "E5": DEFAULT,
  "E6": DEFAULT,
  "F1": DEFAULT,
  "F2": DEFAULT,
  "F3": DEFAULT,
  "F4": DEFAULT,
  "F5": DEFAULT,
  "F6": DEFAULT,
}

default_board_table = PrettyTable([DEFAULT] + [chr(65+i) for i in range(6)])
default_board_table.add_row([1] + [DEFAULT] * 6, divider=True)
default_board_table.add_row([2] + [DEFAULT] * 6, divider = True)
default_board_table.add_row([3] + [DEFAULT] * 2 + [Othello.Color.WHITE.value, Othello.Color.BLACK.value] + [DEFAULT] * 2, divider = True)
default_board_table.add_row([4] + [DEFAULT] * 2 + [Othello.Color.BLACK.value, Othello.Color.WHITE.value] + [DEFAULT] * 2, divider = True)
default_board_table.add_row([5] + [DEFAULT] * 6, divider = True)
default_board_table.add_row([6] + [DEFAULT] * 6, divider = True)

@pytest.mark.parametrize(
  "provided_size, actual_size",
  [
    (None, SIZE),
    (6, 6),
    (20, 20),
    (26, 26),
    (5, SIZE),
    (27, SIZE),
    (0, SIZE),
    ("Seven", SIZE),
    ("6", SIZE),
    (-1, SIZE),
    (9.0, SIZE),
    (7, 8),
    (13, 8),
    (14, 14),
  ],
)
def test_board_size(provided_size, actual_size):
  test_board = Othello(provided_size)
  assert test_board.size == actual_size

def test_initialize_board_dict():
  test_board = Othello(6)
  test_board._board_dict = {}
  assert test_board._board_dict == {}

  test_board.initialize_board_dict()
  assert test_board._board_dict == default_board_dict

@pytest.mark.parametrize(
  "size, letters",
  [
    (6, [chr(65+i) for i in range(6)]),
    (8, [chr(65+i) for i in range(8)]),
    (14, [chr(65+i) for i in range(14)]),
    (26, [chr(65+i) for i in range(26)]),
  ],
)
def test_get_column_letters(size, letters):
  test_board = Othello(size)
  assert test_board.get_column_letters() == [" "] + letters

  test_board.toggle_guides()
  assert test_board.get_column_letters() == letters

def test_update_board_table():
  test_board = Othello(6)
  assert test_board._board_table.get_string() == default_board_table.get_string()

  updated_table = default_board_table.copy()
  updated_table.del_row(5)
  updated_table.add_row([6, Othello.Color.BLACK.value] + [DEFAULT] * 5)

  test_board.set_square('A6', test_board.Color.BLACK)
  test_board.update_board_table()
  assert test_board._board_table.get_string() == updated_table.get_string()
