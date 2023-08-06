import random, time
import sys

from Game import Game


class MemoryGame(Game):
    def __init__(self, diff_game, name):
        super().__init__(diff_game, name)
        self.sequence = []

    def play(self):

        print("Welcome to Memory Game\n"
              f"Well {self.name},  I am thinking of a sequence with {self.diff} digit/s")

        for i in range(0, self.diff):
            self.sequence.append(random.randint(1, 102))
        print(self.sequence, end='')
        time.sleep(0.7)
        sys.stdout.write('\b'*len(self.sequence.__str__()))

        while self.guesses_taken < 6:
            if not self.get_guess():
                continue

            self.guesses_taken += 1

            print("Number entered")
            if self.guess < self.sequence[i]:
                print('Your guess is too low.')
            elif self.guess > self.sequence[i]:
                print('Your guess is too high.')
            else:
                print(f'Good job, {self.name}! You guessed my sequence!')
                return

        print(f'Nope. The sequence I was thinking of was {self.sequence}')
