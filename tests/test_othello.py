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

row1 = [DEFAULT] * 6
row2 = [DEFAULT] * 6
row3 = [DEFAULT] * 2 + [Othello.Color.WHITE.value, Othello.Color.BLACK.value] + [DEFAULT] * 2
row4 = [DEFAULT] * 2 + [Othello.Color.BLACK.value, Othello.Color.WHITE.value] + [DEFAULT] * 2
row5 = [DEFAULT] * 6
row6 = [DEFAULT] * 6
default_board_table = PrettyTable([DEFAULT] + [chr(65+i) for i in range(6)])
default_board_table.add_row([1] + row1, divider=True)
default_board_table.add_row([2] + row2, divider=True)
default_board_table.add_row([3] + row3, divider=True)
default_board_table.add_row([4] + row4, divider=True)
default_board_table.add_row([5] + row5, divider=True)
default_board_table.add_row([6] + row6, divider=True)

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

@pytest.mark.parametrize(
  "input_value, color, return_value",
  [
    ("A1", Othello.Color.BLACK, True),
    ("a1", Othello.Color.BLACK, True),
    ("A3", Othello.Color.WHITE, True),
    ("B7", Othello.Color.WHITE, False),
    ("J2", Othello.Color.WHITE, False),
    ("Z26", Othello.Color.BLACK, False),
    ("bad square", Othello.Color.BLACK, False),
  ]
)
def test_set_square(input_value, color, return_value):
  test_board = Othello(6)
  assert test_board.set_square(input_value, color) == return_value

  if input_value in test_board._board_dict.keys():
    assert test_board._board_dict[input_value] == color.value

@pytest.mark.parametrize(
  "input_list, color, return_value",
  [
    (["A1",], Othello.Color.BLACK, True),
    (["a1"], Othello.Color.BLACK, True),
    (["a1", "A1", "a1"], Othello.Color.BLACK, True),
    (["A3", "a4", "d5"], Othello.Color.WHITE, True),
    ([], Othello.Color.WHITE, True),
    (["B7"], Othello.Color.WHITE, False),
    (["A1", "B7"], Othello.Color.WHITE, False),
    (["A1", "B7", "A2"], Othello.Color.WHITE, False),
    (["J2"], Othello.Color.WHITE, False),
    (["Z26"], Othello.Color.BLACK, False),
    (["bad square"], Othello.Color.BLACK, False),
  ]
)
def test_set_squares(input_list, color, return_value):
  test_board = Othello(6)
  assert test_board.set_squares(input_list, color) == return_value

  if set(input_list).issubset(set(test_board._board_dict.keys())):
    for square in input_list:
      assert test_board._board_dict[square] == color.value

def test_get_square():
  test_board = Othello(6)
  assert test_board.get_square("A1") == DEFAULT
  assert test_board.get_square("a1") == DEFAULT
  assert test_board.get_square("A2") == DEFAULT
  assert test_board.get_square("C3") == Othello.Color.WHITE.value
  assert test_board.get_square("c4") == Othello.Color.BLACK.value
  assert test_board.get_square("invalid") == None

  test_board.set_square('b2', Othello.Color.BLACK)
  assert test_board.get_square("B2") == Othello.Color.BLACK.value

def test_toggle_guides():
  test_board = Othello(6)
  assert test_board._show_guides == True
  assert test_board._board_table.header == True
  test_board.toggle_guides()
  assert test_board._show_guides == False
  assert test_board._board_table.header == False

@pytest.mark.parametrize(
  "row, return_list",
  [
    (1, row1),
    (2, row2),
    (3, row3),
    (4, row4),
    (5, row5),
    (6, row6),
    ("1", row1),
    ("2", row2),
    ("3", row3),
    ("4", row4),
    ("5", row5),
    ("6", row6),
    (1.1, row1),
    (7, []),
    ("7", []),
    (-1, []),
    ("-1", []),
    ("not an int", [])
  ]
)
def test_get_row(row, return_list):
  test_board = Othello(6)
  assert test_board.get_row(row) == return_list

# We can reuse the rows above because the board is symmetrical in its starting state.
@pytest.mark.parametrize(
  "column, return_list",
  [
    ("A", row1),
    ("a", row1),
    ("B", row2),
    ("C", row3),
    ("D", row4),
    ("d", row4),
    ("E", row5),
    ("F", row6),
    ("G", []),
    (DEFAULT, []),
    (1, []),
    ("not in columns", [])
  ]
)
def test_get_column(column, return_list):
  test_board = Othello(6)
  assert test_board.get_column(column) == return_list

@pytest.mark.parametrize(
  "square, direction, next_space",
  [
    ('B2', 'left', 'A2'),
    ('B2', 'upleft', 'A1'),
    ('B2', 'up', 'B1'),
    ('B2', 'upright', 'C1'),
    ('B2', 'right', 'C2'),
    ('B2', 'downright', 'C3'),
    ('B2', 'down', 'B3'),
    ('B2', 'downleft', 'A3'),
    ('B2', 'rightup', 'C1'),
    ('B2', 'right up', 'C1'),
    ('b2', 'rightup', 'C1'),
    ('B2', 'up_something_else_right', 'C1'),
    ('B2', 'upupup', 'B1'),
    ('D1', 'up', None),
    ('A1', 'upright', None),
    ('F3', 'right', None),
    ('E6', 'rightdown', None),
    ('C6', 'down', None),
    ('B6', 'downleft', None),
    ('A4', 'left', None),
    ('A2', 'leftup', None),
  ]
)
def test_get_next_space(square, direction, next_space):
  test_board = Othello(6)
  assert test_board.get_next_space(square, direction) == next_space

@pytest.mark.parametrize(
  "square, color, expected_valid, expected_spaces_to_flip",
  [
    ('C4', Othello.Color.WHITE, True, ['D4', 'E4', 'C5', 'D3']),
    ('C4', Othello.Color.BLACK, False, []),
    ('B5', Othello.Color.WHITE, True, ['C5', 'D5']),
    ('E1', Othello.Color.BLACK, True, ['E2']),
    ('Z26', Othello.Color.BLACK, False, []),
    ('E6', Othello.Color.WHITE, False, [])
  ]
)
def test_check_move(square, color, expected_valid, expected_spaces_to_flip):
  test_board = Othello(8)
  test_board.set_squares(['D4', 'D3', 'C5', 'E3', 'E5'], Othello.Color.BLACK)
  test_board.set_squares(['C6', 'F4', 'E2', 'E5', 'D6'], Othello.Color.WHITE)
  actual_valid, actual_spaces_to_flip = test_board.check_move(square, color)
  assert actual_valid == expected_valid
  assert sorted(actual_spaces_to_flip) == sorted(expected_spaces_to_flip)
