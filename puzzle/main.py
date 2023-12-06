"""
Board:

   # # #
  # # # #
 # # # # #
  # # # #
   # # #

Hexagons: 6 edges and 6 vertices
"""

from itertools import combinations, permutations
from typing import Generator, List, Set, Tuple

DIAGONAL_LINE_DOWN_LEFT_INDEXES: List[Tuple[Tuple[int, int], ...]] = [
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1), (3, 0)),
    ((0, 2), (1, 2), (2, 2), (3, 1), (4, 0)),
    ((1, 3), (2, 3), (3, 2), (4, 1)),
    ((2, 4), (3, 3), (4, 2)),
]

DIAGONAL_LINE_DOWN_RIGHT_INDEXES: List[Tuple[Tuple[int, int], ...]] = [
    ((2, 0), (3, 0), (4, 0)),
    ((1, 0), (2, 1), (3, 1), (4, 1)),
    ((0, 0), (1, 1), (2, 2), (3, 2), (4, 2)),
    ((0, 1), (1, 2), (2, 3), (3, 3)),
    ((0, 2), (1, 3), (2, 4)),
]

# type Board = Tuple[
#     Tuple[int, int, int],
#     Tuple[int, int, int, int],
#     Tuple[int, int, int, int, int],
#     Tuple[int, int, int, int],
#     Tuple[int, int, int],
# ]

Board = Tuple[
    Tuple[int, ...],
    Tuple[int, ...],
    Tuple[int, ...],
    Tuple[int, ...],
    Tuple[int, ...],
]

# Pieces range from 1 to 19
PIECES = range(1, 20)


def is_diagonal_valid(
    board: Board, diagonal_indexes: List[Tuple[Tuple[int, int], ...]]
) -> bool:
    for line in diagonal_indexes:
        sum_of_line = 0
        for x, y in line:
            sum_of_line += board[x][y]
        if sum_of_line != 38:
            return False
    return True


def is_board_valid(board: Board) -> bool:
    if not is_diagonal_valid(
        board=board,
        diagonal_indexes=DIAGONAL_LINE_DOWN_LEFT_INDEXES,
    ):
        return False
    if not is_diagonal_valid(
        board=board,
        diagonal_indexes=DIAGONAL_LINE_DOWN_RIGHT_INDEXES,
    ):
        return False
    return True


def get_all_rows_summing_to_38(row_length: int = 3) -> List[Tuple[int, ...]]:
    return [pieces for pieces in combinations(PIECES, row_length) if sum(pieces) == 38]


def get_valid_board_combinations() -> Generator[Board, None, None]:
    """
    num rows of 3: 30
    num rows of 4: 147
    num rows of 5: 238
    """
    rows_of_3 = get_all_rows_summing_to_38(row_length=3)
    rows_of_4 = get_all_rows_summing_to_38(row_length=4)
    rows_of_5 = get_all_rows_summing_to_38(row_length=5)

    board_count = 0
    using: Set[int] = set()
    for x in combinations(rows_of_3, 2):
        using.update(x[0])
        if using.intersection(x[1]):
            using -= set(x[0])
            continue
        using.update(x[1])
        for y in combinations(rows_of_4, 2):
            if using.intersection(y[0]):
                continue
            using.update(y[0])
            if using.intersection(y[1]):
                using -= set(y[0])
                continue
            using.update(y[1])
            for z in rows_of_5:
                if using.intersection(z):
                    continue
                for row_1 in permutations(x[0]):
                    for row_2 in permutations(y[0]):
                        for row_3 in permutations(z):
                            for row_4 in permutations(y[1]):
                                for row_5 in permutations(x[1]):
                                    board = (row_1, row_2, row_3, row_4, row_5)
                                    yield board
                                    board_count += 1
                                    if board_count % 1_000_000 == 0:
                                        print(board_count)
            using -= set(y[0])
            using -= set(y[1])
        using -= set(x[0])
        using -= set(x[1])


def solve() -> None:
    for board in get_valid_board_combinations():
        if is_board_valid(board):
            print(board)
            break


if __name__ == "__main__":
    solve()
