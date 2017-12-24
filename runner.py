from subprocess import run

# ===============================================================================
#                              Section 0
#                       Trying to play by ourselves
# ===============================================================================
# Interactive game against 'simple_player'
# run("python run_game.py 2 5 5 y interactive simple_player")

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
print("Simple player starts:")
for _ in range(3):
    run("python run_game.py 2 5 5 n simple_player better_player")
print("\nBetter player starts:")
for _ in range(3):
    run("python run_game.py 2 5 5 n better_player simple_player")
