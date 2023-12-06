import sys

N = 19


def is_valid(b):
    return (
        ((b[2] + b[1] + b[0] == 38) or not (b[2] and b[1] and b[0]))
        and ((b[7] + b[3] + b[0] == 38) or not (b[7] and b[3] and b[0]))
        and ((b[11] + b[6] + b[2] == 38) or not (b[11] and b[6] and b[2]))
        and ((b[16] + b[12] + b[7] == 38) or not (b[16] and b[12] and b[7]))
        and ((b[18] + b[15] + b[11] == 38) or not (b[18] and b[15] and b[11]))
        and ((b[18] + b[17] + b[16] == 38) or not (b[18] and b[17] and b[16]))
        and ((b[6] + b[5] + b[4] + b[3] == 38) or not (b[6] and b[5] and b[4] and b[3]))
        and (
            (b[12] + b[8] + b[4] + b[1] == 38) or not (b[12] and b[8] and b[4] and b[1])
        )
        and (
            (b[15] + b[10] + b[5] + b[1] == 38)
            or not (b[15] and b[10] and b[5] and b[1])
        )
        and (
            (b[17] + b[13] + b[8] + b[3] == 38)
            or not (b[17] and b[13] and b[8] and b[3])
        )
        and (
            (b[17] + b[14] + b[10] + b[6] == 38)
            or not (b[17] and b[14] and b[10] and b[6])
        )
        and (
            (b[15] + b[14] + b[13] + b[12] == 38)
            or not (b[15] and b[14] and b[13] and b[12])
        )
        and (
            (b[11] + b[10] + b[9] + b[8] + b[7] == 38)
            or not (b[11] and b[10] and b[9] and b[8] and b[7])
        )
        and (
            (b[18] + b[14] + b[9] + b[4] + b[0] == 38)
            or not (b[18] and b[14] and b[9] and b[4] and b[0])
        )
        and (
            (b[16] + b[13] + b[9] + b[5] + b[2] == 38)
            or not (b[16] and b[13] and b[9] and b[5] and b[2])
        )
    )


def solve():
    board = [0] * N
    used = [0] * (N + 1)  # acts as a hash table

    def place(i):
        if i == N:
            print(board)
            return True

        for j in range(1, N + 1):
            if used[j]:
                continue

            board[i] = j
            used[j] = 1

            if is_valid(board) and place(i + 1):
                sys.exit()
                return

            board[i] = 0
            used[j] = 0

        return False

    place(0)


if __name__ == "__main__":
    solve()
