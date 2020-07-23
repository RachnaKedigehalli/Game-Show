# Game-Show

# Instructions to run the program:
1. Go to the directory in which the files are stored.
2. In the terminal for server, run the command python3 server.py
3. In 3 other terminals (for clients), run the command python3 client.py

# Project Overview:

There are 3 players in the game. The game starts when 3 players join the game. The players are given questions randomly from a list of questions which the host has, such that the questions are not repeated. The players are given 10 seconds to press the buzzer. The first player to press the buzzer is given a chance to answer the question within 10 seconds. If the answer is correct, the player gets 1 point, otherwise -0.5. If no answer is given within 10 seconds or if no player pressed the buzzer, the host moves on to the next question. The game ends when any player gets 5 or more points and that player is declared the winner.
