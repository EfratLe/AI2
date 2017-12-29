from subprocess import run

# ===============================================================================
#                              Section 0
#                       Trying to play by ourselves
# ===============================================================================
# Interactive game against 'simple_player'
# run("python run_game.py 2 5 5 y interactive competition_player")

# ===============================================================================
#                              Section A
# ===============================================================================
# The parameters for 'run_game.py' are:
# setup_time, time_per_k_turns, k, verbose, x_player, o_player
# print("Simple player starts:")
# for _ in range(3):
#     run("python run_game.py 2 5 5 n simple_player random_player")
# print("\nRandom player starts:")
# for _ in range(3):
#     run("python run_game.py 2 5 5 n random_player simple_player")


# ===============================================================================
#                              Section B
# ===============================================================================
# The parameters for 'run_game.py' are:
# setup_time, time_per_k_turns, k, verbose, x_player, o_player

# print("Simple player starts:")
# for _ in range(3):
#     run("python run_game.py 2 5 5 n simple_player better_player")
# print("\nBetter player starts:")
# for _ in range(3):
#     run("python run_game.py 2 5 5 n better_player simple_player")

# ===============================================================================
#                              Section C
# ===============================================================================
# The parameters for 'run_game.py' are:
# setup_time, time_per_k_turns, k, verbose, x_player, o_player

# print("Simple player starts:")
# run("python run_game.py 2 2 5 n simple_player min_max_player")
# run("python run_game.py 2 10 5 n simple_player min_max_player")
# run("python run_game.py 2 50 5 n simple_player min_max_player")
#
# print("\nBetter player starts:")
# run("python run_game.py 2 2 5 n min_max_player simple_player")
# run("python run_game.py 2 10 5 n min_max_player simple_player")
# run("python run_game.py 2 50 5 n min_max_player simple_player")

# ===============================================================================
#                              Section D
# ===============================================================================
# The parameters for 'run_game.py' are:
# setup_time, time_per_k_turns, k, verbose, x_player, o_player
#
# print("Simple player starts:")
# run("python run_game.py 2 2 5 n simple_player alpha_beta_player")
# run("python run_game.py 2 10 5 n simple_player alpha_beta_player")
# run("python run_game.py 2 50 5 n simple_player alpha_beta_player")
#
# print("\nBetter player starts:")
# run("python run_game.py 2 2 5 n alpha_beta_player simple_player")
# run("python run_game.py 2 10 5 n alpha_beta_player simple_player")
# run("python run_game.py 2 50 5 n alpha_beta_player simple_player")

# ===============================================================================
#                              Section F
# ===============================================================================
# Debugging
# run("python run_game.py 2 2 5 n competition_player simple_player")
# run("python run_game.py 2 2 5 n competition_player better_player")
# run("python run_game.py 2 2 5 n better_player competition_player")
# run("python run_game.py 2 2 5 n simple_player competition_player")

# ===============================================================================
#                              Section G
# ===============================================================================
# run("python run_game.py 2 2 5 n alpha_beta_player simple_player")
# run("python run_game.py 2 2 5 n simple_player alpha_beta_player")
# run("python run_game.py 2 2 5 n min_max_player simple_player")
# run("python run_game.py 2 2 5 n simple_player min_max_player")
# run("python run_game.py 2 2 5 n alpha_beta_player min_max_player")

# ===============================================================================
#                              Section G
# ===============================================================================
# run("python run_game.py 2 2 5 n AI2_204536270_204498711.alpha_beta_player AI2_204536270_204498711.min_max_player")
run("python run_game.py 2 3 5 n AI2_204536270_204498711.competition_player simple_player")
