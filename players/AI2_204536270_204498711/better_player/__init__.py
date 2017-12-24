from abstract import AbstractPlayer
from Reversi.board import GameState
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS
import time
import copy


class Player(AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.clock = None

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare time of 0.05 seconds.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05

    def get_move(self, game_state: GameState, possible_moves: list):
        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        best_move = possible_moves[0]
        next_state = copy.deepcopy(game_state)
        next_state.perform_move(best_move[0], best_move[1])

        # TODO: for debugging. delete later.
        # print("# Next State - Player better made the move: [" + str(best_move[0]) + ", " + str(best_move[1]) + "]")
        # next_state.draw_board()

        # Choosing an arbitrary move
        # Get the best move according the utility function
        for move in possible_moves:
            new_state = copy.deepcopy(game_state)
            new_state.perform_move(move[0], move[1])

            # TODO: for debugging. delete later.
            # print("# New State - Player better made the move: [" + str(move[0]) + ", " + str(move[1]) + "]")
            # new_state.draw_board()

            if self.utility(new_state) > self.utility(next_state):
                next_state = new_state
                best_move = move

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.time() - self.clock)

        return best_move

    def utility(self, state: GameState):
        # Add 3 more parameters when calculating how much the state is 'good'
        opp_color = OPPONENT_COLOR[self.color]

        # Calculate Disks parameter
        curr_disks = 0
        opp_disks = 0
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                if state.board[x][y] == self.color:
                    curr_disks += 1
                if state.board[x][y] == opp_color:
                    opp_disks += 1

        disks_parameter = 100 * (curr_disks - opp_disks) / (curr_disks + opp_disks)

        # Calculate Mobility parameter
        real_curr_player = state.curr_player
        state.curr_player = self.color
        curr_mobility = len(state.get_possible_moves())
        state.curr_player = opp_color
        opp_mobility = len(state.get_possible_moves())
        state.curr_player = real_curr_player

        mobility_parameter = 0 if curr_mobility + opp_mobility == 0 else 100 * (curr_mobility - opp_mobility) / (curr_mobility + opp_mobility)

        # Calculate Corners parameter
        curr_corners = 0
        opp_corners = 0
        corners = [(0, 0), (0, 7), (7, 7), (7, 0)]
        for x, y in corners:
            curr_board_place = state.board[x][y]
            if curr_board_place == self.color:
                curr_corners += 1
            elif curr_board_place == opp_color:
                opp_corners += 1

        corners_parameter = 0 if curr_corners + opp_corners == 0 \
            else 100 * (curr_corners - opp_corners) / (curr_corners + opp_corners)

        # Calculate Stability parameter
        stability = {self.color: curr_corners, opp_color: opp_corners}
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
                            elif self._is_in_immediate_danger(state, x, y, player_on_tile, x_direction, y_direction):
                                stability[player_on_tile] -= 1
                                break

        stability_parameter = 0 if stability[self.color] + stability[opp_color] == 0 \
            else 100 * (stability[self.color] - stability[opp_color]) / (stability[self.color] + stability[opp_color])

        return 25*disks_parameter + 8*mobility_parameter + 12*corners_parameter + 25*stability_parameter

    @staticmethod
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

    def __repr__(self):
        return '{} {}'.format(AbstractPlayer.__repr__(self), 'better')
