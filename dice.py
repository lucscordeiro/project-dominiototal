# dice.py
import random

class Dice:
    def __init__(self, num_faces):
        self.num_faces = num_faces

    def roll(self, num_rolls):
        return [random.randint(1, self.num_faces) for _ in range(num_rolls)]
