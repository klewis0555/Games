import pytest
from Othello.othello import Othello, DEFAULT, SIZE

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

def test_intitialize_board_dict():
  test_board = Othello(6)
  test_board._board_dict = {}
  assert test_board._board_dict == {}

  test_board.initialize_board_dict()
  assert test_board._board_dict == {
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
    "C3": test_board.Color.BLACK.value,
    "C4": test_board.Color.WHITE.value,
    "C5": DEFAULT,
    "C6": DEFAULT,
    "D1": DEFAULT,
    "D2": DEFAULT,
    "D3": test_board.Color.WHITE.value,
    "D4": test_board.Color.BLACK.value,
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
  assert test_board.get_column_letters() == letters
