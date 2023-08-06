from MemoryGame import MemoryGame
from GuessGame import GuessGame
from CurrencyRouletteGame import RouletteGame

GAMES = {1:MemoryGame, 2:GuessGame, 3:RouletteGame}


def welcome(name):
    print (f"Hello {name} and welcome to the World of Games (Wog).\n"
            f"Here you can find many cool games to play")
    return name


def load_game(name):
    games = {1: "Memory Game", 2: "Guess Game", 3: "Currency Roulette"}

    print("Please choose a game to play:\n"
          "1. Memory Game - a sequence of numbers ill appear for 1 second and you have to guess it back.\n"
          "2. Guess Game - guess a number and see if you chose like the computer.\n"
          "3. Currency Roulette - try and guess the value of a random amount of USD in ILS.")

    g = input("Choose your game's number: ")

    if g.isdigit() and 0 < int(g) < 4:
        g = int(g)
        game = games[g]
        print(f"The chosen game is {game}")
    else:
        return "No game was chosen. Exiting!"

    diff = input("Please choose game difficulty from 1 to 5: ")

    if diff.isdigit() and 0 < int(diff) < 6:
        diff = int(diff)
    else:
        return "No difficulty was chosen. Exiting!"

    currentgame = GAMES[g](diff, name)
    currentgame.play()