from abstract import AbstractPlayer
from Reversi.board import GameState
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS, X_PLAYER, O_PLAYER
from time import time
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

        # Fields for opening book
        self.moves_till_now = ""
        self.game_board = GameState().board
        if self.color == X_PLAYER:
            self.sign = '+'
            self.opponent_sign = '-'
            self.num_round = 1
        else:
            self.sign = '-'
            self.opponent_sign = '+'
            self.num_round = 4
        self.board_opening_lost_track = False
        self.dict_for_10_common_openings = self._calculate_ten_common_openings()

    def get_move(self, game_state: GameState, possible_moves: list):
        self.clock = time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        best_move = None
        # Check if haven't got to the 10th turn
        if not self.board_opening_lost_track and self.num_round - 1 < 10*3:
            best_move = self.opening_move(game_state)
        self.num_round += 6
        if best_move is None:
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

        self.moves_till_now += self.sign + str(best_move[0]) + str(best_move[1])
        next_state = copy.deepcopy(game_state)
        next_state.perform_move(best_move[0], best_move[1])
        self.game_board = next_state.board

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time() - self.clock)

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

    def selective_deepening_criterion(self, state):
        # TODO: implement
        return False

    def no_more_time(self):
        return (time() - self.clock) >= self.time_for_current_move

    def __repr__(self):
        return '{} {}'.format(AbstractPlayer.__repr__(self), 'competition')

    def opening_move(self, game_state: GameState):
        self._calculate_last_move(game_state)
        common_moves = {move: occurrences for move, occurrences in self.dict_for_10_common_openings.items() if
                        move.startswith(self.moves_till_now)}
        if common_moves:
            best_move = sorted(common_moves.items(), key=lambda x: x[1], reverse=True)[0][0]
            return int(best_move[self.num_round]), int(best_move[self.num_round+1])
        self.board_opening_lost_track = True
        return None

    # Calculates the opponent's last move
    def _calculate_last_move(self, game_state: GameState):
        last_move = ""
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                # Got to a tile that was empty and now it belongs to the opponent
                if self.game_board[x][y] == EM and game_state.board[x][y] == OPPONENT_COLOR[self.color]:
                    last_move += self.opponent_sign + str(x) + str(y)
        self.moves_till_now += last_move

    # Getting the 70 most common 10 length openings that ends in our victory
    def _calculate_ten_common_openings(self):
        from collections import Counter
        with open("Reversi/book.gam") as f:
            plays = f.readlines()

        ten_first_openings = Counter([play[:10 * 3] + " 1" if play.rstrip()[-6] == self.sign and int(play.rstrip()[-5:-3]) > 0 else play[:10 * 3] + " 0" for play in plays])
        wining_openings = {}
        for opening_type, occurrences in ten_first_openings.items():
            # Found an opening that leads to victory
            if opening_type[-1] == "1":
                wining_openings[opening_type[:-1].rstrip()] = \
                    occurrences - ten_first_openings.get(opening_type[:-1] + "0", 0)

        sorted_openings = sorted(wining_openings.items(), key=lambda x: x[1], reverse=True)[:70]

        # Adjusting the openings to our table - performs reflection around the vertical axis \
        # and convert to zero-base
        opp_cols = {'a': '7', 'b': '6', 'c': '5', 'd': '4', 'e': '3', 'f': '2', 'g': '1', 'h': '0',
                    '1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7'}

        opp_sorted_openings = {"".join([opp_cols.get(c, c) for c in opening]): occurrences for opening, occurrences in
                               sorted_openings}

        return opp_sorted_openings
