# territory.py
from dice import Dice

class Territory:
    def __init__(self, name):
        self.name = name
        self.players = []
        self.troops = 5
        self.initial_troops_added = False
        self.dice = Dice(6)  # Adicionei a criação de um objeto Dice na inicialização
        self.num_attacker_troops = 0

    def add_player(self, player):
        self.players.append(player)

    def add_troops(self, num_troops):
        self.troops += num_troops

    def remove_troops(self, num_troops):
        self.troops -= num_troops

    def roll_dice(self, num_dice):
        return self.dice.roll(num_dice)

    def attack(self, target_territory, num_attacker_troops):
        attacker_dice = self.roll_dice(min(num_attacker_troops, 3))
        defender_dice = target_territory.roll_dice(min(target_territory.troops, 2))
        self.num_attacker_troops = num_attacker_troops

        attacker_dice.sort(reverse=True)
        defender_dice.sort(reverse=True)

        print(f"{self.name} ({num_attacker_troops} troops) vs {target_territory.name} ({target_territory.troops} troops):")

        combat_results = []  # Adicione esta linha

        # Compare os dados e subtraia as tropas do atacante ou do defensor
        for a, d in zip(attacker_dice, defender_dice):
            if a > d:
                troops_lost = min(self.num_attacker_troops, target_territory.troops)
                target_territory.remove_troops(troops_lost)
                combat_result = f"Attacker wins! {troops_lost} troops lost by the defender."
            else:
                troops_lost = min(target_territory.troops, self.troops)
                self.remove_troops(troops_lost)
                combat_result = f"Defender wins! {troops_lost} troops lost by the attacker."

            combat_results.append(combat_result)

        # Verifique se o território alvo ficou sem tropas e não tem jogadores
        if target_territory.troops == 0 and not target_territory.players:
            target_territory.add_player(self.players[0])
            combat_results.append(f"{self.name} conquered {target_territory.name}!")

        return combat_results
            
    def get_status(self):
        player_names = [player.name for player in self.players]
        return f"{self.name}: {', '.join(player_names)} ({self.troops} troops)"
    
    def move_troops(self, target_territory, num_troops):
        # Lógica de movimentação de tropas aqui
        pass

    def __str__(self):
        player_names = [player.name for player in self.players]
        return f"{self.name}: {', '.join(player_names)} ({self.troops} troops)"
