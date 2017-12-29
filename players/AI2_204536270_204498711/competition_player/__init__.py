from abstract import AbstractPlayer
from Reversi.board import GameState
from time import time
from utils import INFINITY, MiniMaxWithAlphaBetaPruning

from players.AI2_204536270_204498711.utilities import better_utility


class Player(AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.clock = None

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare time of 0.05 seconds.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.2

    def get_move(self, game_state: GameState, possible_moves: list):
        if len(possible_moves) == 1:
            return possible_moves[0]
        self.clock = time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - self.time_per_k_turns * 0.05

        minimaxObject = MiniMaxWithAlphaBetaPruning(self.utility, self.color, self.no_more_time,
                                                    self.selective_deepening_criterion)
        D = 1
        (value, best_move) = (0, possible_moves[0])
        while not self.no_more_time():
            (value, move1) = minimaxObject.search(game_state, D, -INFINITY, INFINITY, True)
            if not self.no_more_time():
                best_move = move1
            D = D + 1

        return best_move

    def utility(self, state: GameState):
        return better_utility(state, self.color)

    def selective_deepening_criterion(self, state):
        # TODO: implement
        return False

    def no_more_time(self):
        return (time() - self.clock) >= self.time_for_current_move

    def __repr__(self):
        return '{} {}'.format(AbstractPlayer.__repr__(self), 'competition')
