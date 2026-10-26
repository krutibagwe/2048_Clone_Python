
import random
import constants as c

# Points earned from merges in the most recent move
last_move_score = 0


def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)

    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix


def add_two(mat):
    empty_cells = [
        (i, j)
        for i in range(len(mat))
        for j in range(len(mat[0]))
        if mat[i][j] == 0
    ]

    if empty_cells:
        a, b = random.choice(empty_cells)
        mat[a][b] = 2

    return mat


def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return "win"

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return "not over"

    for i in range(len(mat) - 1):
        for j in range(len(mat[0]) - 1):
            if mat[i][j] == mat[i + 1][j] or mat[i][j + 1] == mat[i][j]:
                return "not over"

    for k in range(len(mat) - 1):
        if mat[len(mat) - 1][k] == mat[len(mat) - 1][k + 1]:
            return "not over"

    for j in range(len(mat) - 1):
        if mat[j][len(mat) - 1] == mat[j + 1][len(mat) - 1]:
            return "not over"

    return "lose"


def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0]) - j - 1])
    return new


def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new


def cover_up(mat):
    new = []
    for j in range(c.GRID_LEN):
        partial_new = []
        for i in range(c.GRID_LEN):
            partial_new.append(0)
        new.append(partial_new)

    done = False

    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1

    return new, done


def merge(mat, done):
    global last_move_score

    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN - 1):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2

                # The merged tile's value is the score gained
                last_move_score += mat[i][j]

                mat[i][j + 1] = 0
                done = True

    return mat, done


def up(game):
    global last_move_score
    last_move_score = 0

    game = transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)

    return game, done


def down(game):
    global last_move_score
    last_move_score = 0

    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))

    return game, done


def left(game):
    global last_move_score
    last_move_score = 0

    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]

    return game, done


def right(game):
    global last_move_score
    last_move_score = 0

    game = reverse(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)

    return game, done
