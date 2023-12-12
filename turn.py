# turn.py
class Turn:
    def __init__(self, player_names):
        self.player_names = player_names
        self.current_player_index = 0

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.player_names)
        return self.player_names[self.current_player_index]

    def get_current_player(self):
        return self.player_names[self.current_player_index]
