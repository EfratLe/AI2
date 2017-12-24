"""Generic utility functions
"""
# from __future__ import print_function
from threading import Thread
from multiprocessing import Queue
import time
import copy
import random
from Reversi.board import GameState
from Reversi.consts import *

INFINITY = float(6000)


class ExceededTimeError(RuntimeError):
    """Thrown when the given function exceeded its runtime.
    """
    pass


def function_wrapper(func, args, kwargs, result_queue):
    """Runs the given function and measures its runtime.

    :param func: The function to run.
    :param args: The function arguments as tuple.
    :param kwargs: The function kwargs as dict.
    :param result_queue: The inter-process queue to communicate with the parent.
    :return: A tuple: The function return value, and its runtime.
    """
    start = time.time()
    try:
        result = func(*args, **kwargs)
    except MemoryError as e:
        result_queue.put(e)
        return

    runtime = time.time() - start
    result_queue.put((result, runtime))


def run_with_limited_time(func, args, kwargs, time_limit):
    """Runs a function with time limit

    :param func: The function to run.
    :param args: The functions args, given as tuple.
    :param kwargs: The functions keywords, given as dict.
    :param time_limit: The time limit in seconds (can be float).
    :return: A tuple: The function's return value unchanged, and the running time for the function.
    :raises PlayerExceededTimeError: If player exceeded its given time.
    """
    q = Queue()
    t = Thread(target=function_wrapper, args=(func, args, kwargs, q))
    t.start()

    # This is just for limiting the runtime of the other thread, so we stop eventually.
    # It doesn't really measure the runtime.
    t.join(time_limit)

    if t.is_alive():
        raise ExceededTimeError

    q_get = q.get()
    if isinstance(q_get, MemoryError):
        raise q_get
    return q_get


class MiniMaxAlgorithm:

    def __init__(self, utility, my_color, no_more_time, selective_deepening):
        """Initialize a MiniMax algorithms without alpha-beta pruning.

        :param utility: The utility function. Should have state as parameter.
        :param my_color: The color of the player who runs this MiniMax search.
        :param no_more_time: A function that returns true if there is no more time to run this search, or false if
                             there is still time left.
        :param selective_deepening: A functions that gets the current state, and
                        returns True when the algorithm should continue the search
                        for the minimax value recursivly from this state.
                        optional
        """
        self.utility = utility
        self.my_color = my_color
        self.no_more_time = no_more_time
        self.selective_deepening = selective_deepening

    def recursive_search(self, state, depth,max_or_min):
        child_moves=state.get_possible_moves()
        if len(child_moves)==0 or self.no_more_time():
            return self.utility(state)
        if depth <= 0:
            if not self.selective_deepening(state):
                return self.utility(state)
        if max_or_min:
            curr=-INFINITY
        else:
            curr=INFINITY
        for move in child_moves:
            new_state = copy.deepcopy(state)
            new_state.perform_move(move[0], move[1])
            new_state.curr_player = OPPONENT_COLOR[new_state.curr_player]
            if max_or_min:
                curr=max(curr,self.recursive_search(new_state,depth-1,not max_or_min))
            else:
                curr=min(curr,self.recursive_search(new_state,depth-1,not max_or_min))
        return curr

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.

        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The move in case of max node or None in min mode)
        """
        child_moves = state.get_possible_moves()
        if len(child_moves)==0 or depth == 0 or self.no_more_time():
            return (self.utility(state),None)
        move_to_make=None
        D=0
        curr_val=0
        if maximizing_player:
            while not self.no_more_time() and not D==depth:
                curr_val=-INFINITY
                for move in child_moves:
                    new_state = copy.deepcopy(state)
                    new_state.perform_move(move[0], move[1])
                    new_state.curr_player=OPPONENT_COLOR[new_state.curr_player]
                    val=self.recursive_search(new_state,D,False)
                    if curr_val < val:
                        curr_val=val
                        move_to_make=move
                D = D + 1
        else:
            print('here')
            while not self.no_more_time() and not D == depth:
                curr_val = self.recursive_search(state,D+1,False)
                move_to_make = None
                D = D + 1
        return (curr_val,move_to_make)




class MiniMaxWithAlphaBetaPruning:

    def __init__(self, utility, my_color, no_more_time, selective_deepening):
        """Initialize a MiniMax algorithms with alpha-beta pruning.

        :param utility: The utility function. Should have state as parameter.
        :param my_color: The color of the player who runs this MiniMax search.
        :param no_more_time: A function that returns true if there is no more time to run this search, or false if
                             there is still time left.
        :param selective_deepening: A functions that gets the current state, and
                        returns True when the algorithm should continue the search
                        for the minimax value recursivly from this state.
        """
        self.utility = utility
        self.my_color = my_color
        self.no_more_time = no_more_time
        self.selective_deepening = selective_deepening

    def search(self, state, depth, alpha, beta, maximizing_player):
        """Start the MiniMax algorithm.

        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param alpha: The alpha of the alpha-beta pruning.
        :param beta: The beta of the alpha-beta pruning.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The alpha-beta algorithm value, The move in case of max node or None in min mode)
        """
        return self.utility(state), None

def ut(state):
    return random.randint(5,10)
def time():
    return False
def sd(state):
    num = random.randint(0,110)
    if num==5:
        return True
    return False

test=MiniMaxAlgorithm(ut,'black',time,sd)
b_state=GameState()
print(test.search(b_state,100,True))
