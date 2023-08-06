import random
from Game import Game


class GuessGame(Game):
    def __init__(self, diff_game, name):
        super().__init__(diff_game, name)
        self.diff = self.diff + 1
        self.secret_number = random.randint(1, self.diff)

    def play(self):
        print("Welcome to Guess Game\n"
              f"Well {self.name},  I am thinking of a number between 1 and {self.diff}")

        while self.guesses_taken < 6:
            if not self.get_guess():
                continue

            self.guesses_taken += 1

            if self.guess < self.secret_number:
                print('Your guess is too low.')
            elif self.guess > self.secret_number:
                print('Your guess is too high.')
            else:
                print(f'Good job, {self.name}! You guessed my number in {self.guesses_taken} guesses!')
                return

        print(f'Nope. The number I was thinking of was {self.secret_number}')