class Game:
    def __init__(self, diff_game, name):
        self.diff = diff_game
        self.name = name
        self.guesses_taken = 0
        self.guess = None

    def get_guess(self):
        self.guess = input('Take a guess: ')
        if not self.guess.isdigit():
            print('Not a valid guess.')
            return False
        self.guess = int(self.guess)
        return True
