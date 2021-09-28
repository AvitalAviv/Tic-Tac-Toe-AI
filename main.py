from __future__ import print_function
import random
import sys
import copy
import time

def create_board():
    board = []
    for col in range(0, 3):
        inner_col = []
        for in_col in range(0, 3):
            inner_col.append(None)
        board.append(inner_col)
    return board

def print_board(board):
    print("    0   1   2")
    row_num = 0
    for row in board:
        print(row_num, end=" ")
        output_row = '| '
        for output in row:
            if output is None:
                output_row += ' '
            else:
                output_row += output
            output_row += ' | '
        row_num += 1
        print(output_row)
    print("")
    print("")

def is_valid_move(move_cor, board):
    x = (move_cor[0])
    y = (move_cor[1])
    if x < 0 or x > 2:
        print("illegal coordination")
        return
    if y < 0 or y > 2:
        print("illegal coordination")
        return
    if board[x][y] is not None:
        print("Cant make move! square already taken!")
        return
    return 1

def make_move(board, move_coords, string):
    while True:
        if is_valid_move(move_coords, board) == 1:
            break
        else:
            return
    board[move_coords[0]][move_coords[1]] = string
    return board

def check_winner(board):
    for x in range(0, 3):
        col = []
        for y in range(0, 3):
            col.append(board[x][y])
        if len(set(col)) == 1 and col[0] is not None:
            return col[0]
    for y in range(0, 3):
        row = []
        for x in range(0, 3):
            row.append(board[x][y])
        if len(set(row)) == 1 and row[0] is not None:
            return row[0]
    list1 = [board[0][0], board[1][1], board[2][2]]
    list2 = [board[0][2], board[1][1], board[2][0]]
    new_list1 = set(list1)
    new_list2 = set(list2)
    if len(set(new_list1)) == 1 and list1[0] is not None:
        return list1[0]
    if len(set(new_list2)) == 1 and list2[0] is not None:
        return list2[0]
    return None

def get_diagonals(board):
    list = [[board[0][0], board[1][1], board[2][2]],[board[0][2],board[1][1],board[2][0]]]
    return list

def is_board_full(board):
    for x in board:
        for y in x:
            if y is None:
                return False
    return True

def random_ai(board, current_player_symbol):
    all_legal_moves = get_all_empty_coords(board)
    return random.choice(all_legal_moves)

def get_all_empty_coords(board):
    empty_elements = []
    for x in range(0, 3):
        for y in range(0, 3):
            if board[x][y] is None:
                empty_elements.append([x,y])
    return empty_elements

def finds_winning_moves_ai(board, current_player_symbol):
    current_player_winning_move = some_winning_move_ai(board, current_player_symbol)
    if current_player_winning_move is not None:
        return current_player_winning_move

    return random_ai(board, current_player_symbol)

def some_winning_move_ai(board, current_player_symbol):
    for row in range(0, 3):
        num_current_symbol = 0
        num_none = 0
        last_coord = None
        for value in range(0, 3):
            if board[value][row] is current_player_symbol:
                num_current_symbol += 1
            if board[value][row] is None:
                num_none += 1
                last_coord = (value, row)
        if num_current_symbol == 2 and num_none == 1:
            return last_coord

    for col in range(0, 3):
        num_current_symbol = 0
        num_none = 0
        last_coord = None
        for value in range(0, 3):
            if board[col][value] is current_player_symbol:
                num_current_symbol += 1
            if board[col][value] is None:
                num_none += 1
                last_coord = (col, value)
        if num_current_symbol == 2 and num_none == 1:
            return last_coord

    diagonals = [[[0,0],[1,1],[2,2]],[[0,2],[1,1],[2,0]]]
    for diagonal in diagonals:
        num_current_symbol = 0
        num_none = 0
        last_coord = None
        for (x,y) in diagonal:
            if board[x][y] is current_player_symbol:
                num_current_symbol += 1
            if board[x][y] is None:
                num_none += 1
                last_coord = (x,y)
        if num_current_symbol == 2 and num_none == 1:
            return last_coord

def finds_winning_and_losing_moves_ai(board, current_player_symbol):
    current_player_winning_move = some_winning_move_ai(board, current_player_symbol)
    if current_player_winning_move is not None:
        return current_player_winning_move

    block_move_current_player = some_winning_move_ai(board, get_other_player(current_player_symbol))
    if block_move_current_player is not None:
        return block_move_current_player

    return random_ai(board, current_player_symbol)

def find_other_player_winning_move(board, current_player_symbol):
    other_player_winning_move = some_winning_move_ai(board, get_other_player(current_player_symbol))
    if other_player_winning_move:
        return other_player_winning_move

    return random_ai(board, get_other_player(current_player_symbol))

def get_other_player(current_player_symbol):
    if current_player_symbol == 'X':
        return 'O'
    return 'X'

def get_all_lines(board):
    cols = []
    for x in range(0, 3):
        col = []
        for y in range(0, 3):
            col.append(board[x][y])
        cols.append(col)

    rows = []
    for y in range(0, 3):
        row = []
        for x in range(0, 3):
            row.append(board[x][y])
        rows.append(row)

    return cols + rows + get_diagonals(board)

def human_player():
    print("please enter your next move: ")
    x_coord = int(input("X?: "))
    y_coord = int(input("Y?: "))
    return (y_coord, x_coord)

def get_move(board, current_player_symbol, algo_name):
    if algo_name == 'random_ai':
        return random_ai(board, current_player_symbol)
    if algo_name == 'finds_winning_moves_ai':
        return finds_winning_moves_ai(board, current_player_symbol)
    if algo_name == 'finds_winning_and_losing_moves_ai':
        return finds_winning_and_losing_moves_ai(board, current_player_symbol)
    if algo_name == 'minimax_ai':
        return minimax_ai(board, current_player_symbol)
    else:
        raise Exception("Unknown algorithm name- " + algo_name)

def minimax_ai(board, current_player_symbol):
    best_move = None
    best_score = None
    all_moves = get_all_empty_coords(board)
    for move in all_moves:
        copy_board = copy.deepcopy(board)
        make_move(copy_board, move, current_player_symbol)
        other_player_symbol = get_other_player(current_player_symbol)
        score = minmax_score(copy_board, other_player_symbol, current_player_symbol)
        if best_score is None or score > best_score:
            best_move = move
            best_score = score
    return best_move

def minmax_score(board, player_to_move, player_better_score):
    game_winner = check_winner(board)
    if game_winner is not None:
        if game_winner == player_better_score:
            return 10
        else:
            return -10
    if game_winner is None and is_board_full(board):
        return 0

    scores = []
    all_legal_moves = get_all_empty_coords(board)
    for move in all_legal_moves:
        copy_board = copy.deepcopy(board)
        make_move(copy_board, move, player_to_move)
        other_player_symbol = get_other_player(player_to_move)
        other_player_best_score = minmax_score(copy_board, other_player_symbol, player_better_score)
        scores.append(other_player_best_score)

    if player_to_move == player_better_score:
        return max(scores)
    else:
        return min(scores)

def game_flow(param_one, param_two):
    name_one = input("first player's name: ")
    name_two = input("second player's name: ")
    players = [('O', name_one), ('X', name_two)]
    board = create_board()
    turn_num = 0
    winner = None
    while True:
        current_player_symbol, current_player_name = players[turn_num % 2]
        time.sleep(2)
        print_board(board)
        if current_player_symbol == 'O':
            move_coord = get_move(board, current_player_symbol, param_one)
        else:
            move_coord = get_move(board, current_player_symbol, param_two)
        board = make_move(board, move_coord, current_player_symbol)
        winner = check_winner(board)
        if winner is not None:
            time.sleep(2)
            print_board(board)
            print("THE WINNER IS: " + current_player_name)
            break
        if is_board_full(board):
            time.sleep(2)
            print_board(board)
            print("ITS A DRAW!!!")
            break
        turn_num += 1

def main():
    game_flow(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()