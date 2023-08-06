import requests
import random
from Game import Game


class RouletteGame(Game):
    def __init__(self, diff_game, name):
        super().__init__(diff_game, name)
        self.amount = random.randint(1, 101)
        self.currency = None
        self.convert = None

    def play(self):

        params = {'base': 'USD', 'symbols': 'ILS', 'format': 1}
        req = requests.get('http://api.exchangeratesapi.io/latest', params=params)
        currency = req.json()['rates']['ILS']

        currency = int(currency) * self.amount
        self.currency = (currency - (5 - self.diff), currency + (5 - self.diff))

        print("Welcome to Currency Roulette\n"
              f"Well {self.name},  The amount in ILS is between {self.currency}\n"
              f"How many USD is that?")

        while self.guesses_taken < 6:
            if not self.get_guess():
                continue
            self.guesses_taken += 1

            if self.guess < self.amount:
                print('Your guess is too low.')
            elif self.guess > self.amount:
                print('Your guess is too high.')
            else:
                print(f'Good job, {self.name}! You guessed my number in {self.guesses_taken} guesses!')
                return

        print(f'Nope. The amount I was thinking of was {self.amount}')