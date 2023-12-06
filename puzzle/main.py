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
from typing import Generator, List, Tuple

VALID_CELLS = {
    (0, 2),
    (0, 4),
    (0, 6),
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 0),
    (2, 2),
    (2, 4),
    (2, 6),
    (2, 8),
    (3, 1),
    (3, 3),
    (3, 5),
    (3, 7),
    (4, 2),
    (4, 4),
    (4, 6),
}

NEIGHBORS = [
    # Diagonals
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
    # Left / Right
    (0, -1),
    (0, 1),
]

# LINES = [
#     [(0, 0), (0, 1), (0, 2)],
#     [(1, 0), (0, 1), (0, 2)],
#     [(0, 0), (0, 1), (0, 2)],
#     [(0, 0), (0, 1), (0, 2)],
#     [(0, 0), (0, 1), (0, 2)],
# ]

DIAGONAL_LINE_DOWN_LEFT_INDEXES = [
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1), (3, 0)),
    ((0, 2), (1, 2), (2, 2), (3, 1), (4, 0)),
    ((1, 3), (2, 3), (3, 2), (4, 1)),
    ((2, 4), (3, 3), (4, 2)),
]

DIAGONAL_LINE_DOWN_RIGHT_INDEXES = [
    ((2, 0), (3, 0), (4, 0)),
    ((1, 0), (2, 1), (3, 1), (4, 1)),
    ((0, 0), (1, 1), (2, 2), (3, 2), (4, 2)),
    ((0, 1), (1, 2), (2, 3), (3, 3)),
    ((0, 2), (1, 3), (2, 4)),
]


class Node:
    def __init__(self, i: int, j: int, neighbors: List["Node"]) -> None:
        self.i = i
        self.j = j
        self.neighbors = neighbors


def get_board() -> List[List[int]]:
    """
    5x9 board
    """
    return [[0] * 9] * 5


def is_board_valid(board: Tuple[Tuple]) -> bool:
    for line in DIAGONAL_LINE_DOWN_LEFT_INDEXES:
        sum_of_line = 0
        for x, y in line:
            sum_of_line += board[x][y]
        if sum_of_line != 38:
            return False
    for line in DIAGONAL_LINE_DOWN_RIGHT_INDEXES:
        sum_of_line = 0
        for x, y in line:
            sum_of_line += board[x][y]
        if sum_of_line != 38:
            return False
    return True


# def get_valid_board_combinations() -> List[Tuple[Tuple]]:
def get_valid_board_combinations() -> Generator[Tuple[Tuple], None, None]:
    """
    num rows of 3: 30
    num rows of 4: 147
    num rows of 5: 238
    """
    boards = []
    rows_of_3 = get_all_rows_summing_to_38(row_length=3)
    rows_of_4 = get_all_rows_summing_to_38(row_length=4)
    rows_of_5 = get_all_rows_summing_to_38(row_length=5)

    board_count = 0
    using = set()
    for x in combinations(rows_of_3, 2):
        # print(f"Start using: {using}")
        using.update(x[0])
        if using.intersection(x[1]):
            using -= set(x[0])
            continue
        using.update(x[1])
        # print(f"Using 1: {using}")
        # print(f"x={x[0], x[1]}")
        for y in combinations(rows_of_4, 2):
            if using.intersection(y[0]):
                continue
            using.update(y[0])
            if using.intersection(y[1]):
                using -= set(y[0])
                continue
            using.update(y[1])
            # print(y[0], y[1])
            # print(f"Using 2: {using}")
            for z in rows_of_5:
                if using.intersection(z):
                    continue
                # print(f"Using 3: {using}")
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

    # print(f"Boards: {boards}")
    # print(len(boards))
    # return boards

    for first_row_idx in range(len(rows_of_3)):
        first_row = rows_of_3[first_row_idx]
        for last_row_idx in range(first_row_idx + 1, len(rows_of_3)):
            last_row = rows_of_3[last_row_idx]
            for second_row_idx in range(len(rows_of_4)):
                second_row = rows_of_4[second_row_idx]
                for fourth_row_idx in range(second_row_idx + 1, len(rows_of_4)):
                    fourth_row = rows_of_4[fourth_row_idx]
                    for third_row in rows_of_5:
                        boards.append(
                            [first_row, second_row, third_row, fourth_row, last_row]
                        )
    print(boards)


def get_all_rows_summing_to_38(row_length: int = 3) -> List[Tuple[int]]:
    rows = []
    for tup in list(combinations(range(1, 20), row_length)):
        if sum(tup) == 38:
            rows.append(tup)
    return rows


def solve() -> None:
    for board in get_valid_board_combinations():
        # for board in boards:
        if is_board_valid(board):
            print(board)
            break


if __name__ == "__main__":
    solve()
