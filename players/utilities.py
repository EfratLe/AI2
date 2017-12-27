from Reversi.board import GameState
from utils import INFINITY
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS


def simple_utility(state: GameState, color: str):
    if len(state.get_possible_moves()) == 0:
        return INFINITY if state.curr_player != color else -INFINITY

    my_u = 0
    op_u = 0
    for x in range(BOARD_COLS):
        for y in range(BOARD_ROWS):
            if state.board[x][y] == color:
                my_u += 1
            if state.board[x][y] == OPPONENT_COLOR[color]:
                op_u += 1

    if my_u == 0:
        # I have no tools left
        return -INFINITY
    elif op_u == 0:
        # The opponent has no tools left
        return INFINITY
    else:
        return my_u - op_u


def better_utility(state: GameState, color: str):
    if len(state.get_possible_moves()) == 0:
        return INFINITY if state.curr_player != color else -INFINITY
    # Add 3 more parameters when calculating how much the state is 'good'
    opp_color = OPPONENT_COLOR[color]

    # Calculate Disks parameter
    curr_disks = 0
    opp_disks = 0
    for x in range(BOARD_COLS):
        for y in range(BOARD_ROWS):
            if state.board[x][y] == color:
                curr_disks += 1
            if state.board[x][y] == opp_color:
                opp_disks += 1

    disks_parameter = 100 * (curr_disks - opp_disks) / (curr_disks + opp_disks)

    # Calculate Mobility parameter
    real_curr_player = state.curr_player
    state.curr_player = color
    curr_mobility = len(state.get_possible_moves())
    state.curr_player = opp_color
    opp_mobility = len(state.get_possible_moves())
    state.curr_player = real_curr_player

    # Check if we got to a final state and in which condition
    # If we won, finish the heuristic calculation
    # if not curr_mobility or not opp_mobility:  # Final state
    #     return INFINITY if curr_disks > opp_disks else -INFINITY

    mobility_parameter = 0 if curr_mobility + opp_mobility == 0 else 100 * (curr_mobility - opp_mobility) / (curr_mobility + opp_mobility)

    # Calculate Corners parameter
    curr_corners = 0
    opp_corners = 0
    corners = [(0, 0), (0, 7), (7, 7), (7, 0)]
    for x, y in corners:
        curr_board_place = state.board[x][y]
        if curr_board_place == color:
            curr_corners += 1
        elif curr_board_place == opp_color:
            opp_corners += 1

    corners_parameter = 0 if curr_corners + opp_corners == 0 \
        else 100 * (curr_corners - opp_corners) / (curr_corners + opp_corners)

    # Calculate Stability parameter
    stability = {color: curr_corners, opp_color: opp_corners}
    for x in range(BOARD_COLS):
        for y in range(BOARD_ROWS):
            if (x, y) in corners:
                continue
            else:
                player_on_tile = state.board[x][y]
                if player_on_tile == EM:
                    continue
                for x_direction, y_direction in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
                    curr_x = x + x_direction  # step in the direction
                    curr_y = y + y_direction  # step in the direction
                    if state.isOnBoard(curr_x, curr_y):
                        if state.board[curr_x][curr_y] == player_on_tile:
                            # The tile is adjacent to a corner
                            if (curr_x, curr_y) in corners and (x_direction, y_direction) not in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
                                stability[player_on_tile] += 1
                                break
                        # The tile is in immediate danger
                        elif _is_in_immediate_danger(state, x, y, player_on_tile, x_direction, y_direction):
                            stability[player_on_tile] -= 1
                            break

    stability_parameter = 0 if stability[color] + stability[opp_color] == 0 \
        else 100 * (stability[color] - stability[opp_color]) / (stability[color] + stability[opp_color])

    return 25*disks_parameter + 8*mobility_parameter + 12*corners_parameter + 25*stability_parameter


def _is_in_immediate_danger(state: GameState, x: int, y: int, player_on_tile, x_direction: int, y_direction: int) -> bool:
    curr_x = x + x_direction
    curr_y = y + y_direction
    opposite_x = x - x_direction
    opposite_y = y - y_direction

    if not state.isOnBoard(x-x_direction, y-y_direction):
        return False

    if (state.board[curr_x][curr_y] == EM and state.board[opposite_x][opposite_y] == OPPONENT_COLOR[player_on_tile]) \
            or (state.board[curr_x][curr_y] == OPPONENT_COLOR[player_on_tile] and state.board[opposite_x][opposite_y] == EM):
        return True
