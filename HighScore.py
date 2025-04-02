"""encapsulates a highscore with initials (string) and score (integer)"""
__version__ = '04/02/2025'
__author__ = 'Kayla Cao'

class HighScore:
    """encapsulates a highscore with initials (string) and score (integer)"""
    def __init__(self, inits, score):
        self.initials = inits
        self.score = score

    def __eq__(self, other):
        return self.score == other.score and self.initials == other.initials
    def __lt__(self, other):
        return self.score < other.score
    def __gt__(self, other):
        return self.score > other.score

    def __str__(self):
        return str(self.initials) + ' ' + str(self.score)