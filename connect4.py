import sys
import copy
import random

max_column = 6
max_row = 5
max_slots = (max_row + 1) * (max_column + 1)
empty_character = "x"
red_character = "R"
yellow_character = "Y"
max_depth = 7

class Position:
    def __init__(self):
        self.slots = [[empty_character for row in range(max_row + 1)] for column in range(max_column + 1)]
        self.tops = [0 for column in range(max_column + 1)]
        self.player = 1
        self.number_slots_occupied = 0

    def __str__(self):
        to_return = ""
        for row in range(max_row, -1, -1):
            row_string = ""
            for column in range(max_column, -1, -1):
                row_string += str(self.slots[column][row])

            to_return += row_string

        to_return += "\r\n"
        to_return += "Tops: " + str(self.tops)
        to_return += "Player to move: " + str(self.player)

        return to_return

class Move:
    def __init__(self, column, score):
        self.column = column
        self.score = score

def flip_player(player):
    if player == 1:
        return 2
    else:
        return 1

def apply_heuristic(position):
    return random.randint(-10000,10000)

def get_possible_moves(position):
    to_return = []
    for column in range(len(position.tops)):
        if position.tops[column] < max_column:
            to_return.append(Move(column, 0))
    return to_return

def print_board_position(position):
    for row in range(max_row, -1, -1):
        row_string = ""
        for column in range(0, max_column):
            row_string += str(position.slots[column][row])

        print(row_string)
    print()
    print("Tops: " + str(position.tops))
    print("Player to move: " + str(position.player))
    print()

def create_initial_position():
    return Position()

def apply_move(position, move):
    position.slots[move.column][position.tops[move.column]] = position.player
    position.player = flip_player(position.player)
    position.tops[move.column] = position.tops[move.column] + 1
    position.number_slots_occupied += 1

def unapply_move(position, move):
    position.player = flip_player(position.player)
    position.tops[move.column] = position.tops[move.column] - 1
    position.slots[move.column][position.tops[move.column]] = empty_character
    position.number_slots_occupied -= 1

def get_score(position, depth):
    if (depth == max_depth or position.number_slots_occupied == max_slots):
        return apply_heuristic(position)
    else:
        best_move = get_best_move(position, depth)
        return best_move.score

def get_best_move(position, depth):
    best_move = None
    possible_moves = get_possible_moves(position)
    if (position.player == 1):
        best_score = sys.maxsize * -1
        for move in possible_moves:
            apply_move(position, move)
            possible_score = get_score(position, depth + 1)
            unapply_move(position, move)
            move.score = possible_score

            if possible_score > best_score:
                best_move = move
                best_score = possible_score
    else:
        best_score = sys.maxsize
        for move in possible_moves:
            apply_move(position, move)
            possible_score = get_score(position, depth + 1)
            unapply_move(position, move)
            move.score = possible_score

            if possible_score < best_score:
                best_move = move
                best_score = possible_score

    return best_move

current_position = Position()
print_board_position(current_position)

is_game_over = False

move_number = 1
while move_number <= 42:
    print("Ply: " + str(move_number))

    outer_move = get_best_move(current_position, 0)
    apply_move(current_position, outer_move)
    print_board_position(current_position)

    move_number += 1
