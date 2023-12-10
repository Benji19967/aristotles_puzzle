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

Board = Tuple[
    Tuple[int, ...],
    Tuple[int, ...],
    Tuple[int, ...],
    Tuple[int, ...],
    Tuple[int, ...],
]

# Pieces range from 1 to 19
PIECES = range(1, 20)
REQUIRED_SUM = 38


def is_diagonal_valid(
    board: Board, diagonal_indexes: List[Tuple[Tuple[int, int], ...]]
) -> bool:
    for line in diagonal_indexes:
        sum_of_line = 0
        for x, y in line:
            sum_of_line += board[x][y]
        if sum_of_line != REQUIRED_SUM:
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


def get_all_rows_summing_to_required_sum(row_length: int = 3) -> List[Tuple[int, ...]]:
    return [
        pieces
        for pieces in combinations(PIECES, row_length)
        if sum(pieces) == REQUIRED_SUM
    ]


def generate_valid_board_combinations() -> Generator[Board, None, None]:
    """
    num rows of 3: 30
    num rows of 4: 147
    num rows of 5: 238
    """
    rows_of_3 = get_all_rows_summing_to_required_sum(row_length=3)
    rows_of_4 = get_all_rows_summing_to_required_sum(row_length=4)
    rows_of_5 = get_all_rows_summing_to_required_sum(row_length=5)

    count = 0
    for rows in list(
        combinations((p for row in rows_of_3 for p in permutations(row)), 3)
    ):
        all = set(rows[0])
        is_valid = True
        for r in rows[1:]:
            if not len(all.intersection(r)) == 1 or not rows[0][2] == rows[1][0]:
                is_valid = False
            all.update(r)
        if is_valid:
            count += 1
    print(count)

    board_count = 0
    using: Set[int] = set()
    for row_1, row_5 in combinations(rows_of_3, 2):
        using.update(row_1)
        if using.intersection(row_5):
            using -= set(row_1)
            continue
        using.update(row_5)
        for row_2, row_4 in combinations(rows_of_4, 2):
            if using.intersection(row_2):
                continue
            using.update(row_2)
            if using.intersection(row_4):
                using -= set(row_2)
                continue
            using.update(row_4)
            for row_3 in rows_of_5:
                if using.intersection(row_3):
                    continue
                for row_1_permutation in permutations(row_1):
                    for row_2_permutation in permutations(row_2):
                        for row_3_permutation in permutations(row_3):
                            for row_4_permutation in permutations(row_4):
                                for row_5_permutation in permutations(row_5):
                                    board = (
                                        row_1_permutation,
                                        row_2_permutation,
                                        row_3_permutation,
                                        row_4_permutation,
                                        row_5_permutation,
                                    )
                                    yield board
                                    board_count += 1
                                    if board_count % 1_000_000 == 0:
                                        print(board_count)
            using -= set(row_2)
            using -= set(row_4)
        using -= set(row_1)
        using -= set(row_5)


def solve() -> None:
    for board in generate_valid_board_combinations():
        if is_board_valid(board):
            print(board)
            break


if __name__ == "__main__":
    solve()
