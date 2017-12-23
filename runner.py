from subprocess import run

# Section A
# The parameters are: setup_time, time_per_k_turns, k, verbose, x_player, o_player
print("Simple player starts:")
for _ in range(3):
    run("python run_game.py 2 5 5 n simple_player random_player")
print("\nRandom player starts:")
for _ in range(3):
    run("python run_game.py 2 5 5 n random_player simple_player")
