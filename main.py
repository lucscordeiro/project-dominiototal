# main.py
import pygame
import sys
from button import Button
from territory import Territory
from turn import Turn
from dice import Dice
from player import Player

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def get_num_players():
    input_active = False
    input_text = ""

    while True:
        SCREEN.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        num_players = int(input_text)
                        return num_players
                    except ValueError:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    input_text += event.unicode

        NUM_PLAYERS_TEXT = get_font(45).render("Enter the number of players:", True, "Black")
        NUM_PLAYERS_RECT = NUM_PLAYERS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(NUM_PLAYERS_TEXT, NUM_PLAYERS_RECT)

        input_rect = pygame.Rect(640 - 100, 350, 200, 50)
        pygame.draw.rect(SCREEN, (0, 0, 0), input_rect, 2)
        input_surface = get_font(40).render(input_text, True, "Black")
        SCREEN.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.update()

def get_player_names(num_players):
    player_names = []
    input_active = False
    input_text = ""

    for i in range(num_players):
        input_active = True
        input_text = ""

        while input_active:
            SCREEN.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_text:
                            player_names.append(input_text)
                            input_text = ""
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            PLAYER_NAME_TEXT = get_font(45).render(f"Enter the name for Player {i + 1}:", True, "Black")
            PLAYER_NAME_RECT = PLAYER_NAME_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(PLAYER_NAME_TEXT, PLAYER_NAME_RECT)

            input_rect = pygame.Rect(640 - 150, 350, 300, 50)
            pygame.draw.rect(SCREEN, (0, 0, 0), input_rect, 2)
            input_surface = get_font(40).render(input_text, True, "Black")
            SCREEN.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

            pygame.display.update()

    return player_names

def assign_players_to_territories(player_names):
    players = [Player(name) for name in player_names]
    territories = [Territory("Norte"), Territory("Sul"), Territory("Leste"), Territory("Oeste")]

    for i, player in enumerate(players):
        territories[i % len(territories)].add_player(player)
        player.add_territory(territories[i % len(territories)])

    return territories

def show_dialog(screen, text):
    input_active = True
    input_text = ""

    while input_active:
        screen.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        input_value = int(input_text)
                        input_text = ""
                        input_active = False
                        return input_value
                    except ValueError:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    input_text += event.unicode

        DIALOG_TEXT = get_font(30).render(text, True, "Black")
        DIALOG_RECT = DIALOG_TEXT.get_rect(center=(640, 260))
        screen.blit(DIALOG_TEXT, DIALOG_RECT)

        input_rect = pygame.Rect(640 - 100, 350, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)
        input_surface = get_font(40).render(input_text, True, "Black")
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.update()


def choose_target_territory(territories, current_player):
    SCREEN.fill("black")

    TARGET_TEXT = get_font(45).render("Escolha um território alvo:", True, "White")
    TARGET_RECT = TARGET_TEXT.get_rect(center=(640, 100))
    SCREEN.blit(TARGET_TEXT, TARGET_RECT)

    y_offset = 200
    valid_targets = [
        (i, territory) for i, territory in enumerate(territories)
        if current_player not in territory.players
    ]

    for i, (index, territory) in enumerate(valid_targets):
        target_text = get_font(30).render(f"{i + 1}. {territory.name} ({territory.troops} tropas)", True, "White")
        target_rect = target_text.get_rect(center=(640, y_offset))
        SCREEN.blit(target_text, target_rect)
        y_offset += 50

    input_text = ""
    input_rect = pygame.Rect(640 - 100, 350, 200, 50)
    pygame.draw.rect(SCREEN, (255, 255, 255), input_rect, 2)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text and 1 <= int(input_text) <= len(valid_targets):
                        target_index = int(input_text) - 1
                        return valid_targets[target_index][0]
                    else:
                        show_dialog(SCREEN, "Invalid choice. Please enter a valid number.")
                        break  # Adicionado para interromper o loop se a escolha for inválida
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    input_text += event.unicode

        TARGET_INPUT_TEXT = get_font(40).render(input_text, True, "White")
        SCREEN.blit(TARGET_INPUT_TEXT, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.update()

def show_combat_results(screen, combat_results):
    input_active = True

    while input_active:
        screen.fill("black")
        y_offset = 200

        for result in combat_results:
            combat_result_text = get_font(30).render(result, True, "White")
            combat_result_rect = combat_result_text.get_rect(center=(640, y_offset))
            screen.blit(combat_result_text, combat_result_rect)
            y_offset += 30

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                
def play(num_players, player_names):
    territories = assign_players_to_territories(player_names)
    turn = Turn(player_names)

    troops_to_add = 3
    troops_for_attack = 0
    combat_results = []

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render(f"{turn.get_current_player()} Turn", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        y_offset = 200
        for territory in territories:
            assignment_text = get_font(30).render(territory.get_status(), True, "White")
            assignment_rect = assignment_text.get_rect(center=(640, y_offset))
            SCREEN.blit(assignment_text, assignment_rect)
            y_offset += 50

        ACTION_TEXT = get_font(30).render("Select an action:", True, "White")
        ACTION_RECT = ACTION_TEXT.get_rect(center=(640, 500))
        SCREEN.blit(ACTION_TEXT, ACTION_RECT)

        ACTION_ADD_TROOPS = Button(image=None, pos=(640, 550),
                                text_input=f"Add Troops ({troops_to_add})", font=get_font(40), base_color="White", hovering_color="Green")
        ACTION_ATTACK = Button(image=None, pos=(640, 600),
                            text_input="Attack", font=get_font(40), base_color="White", hovering_color="Red")
        ACTION_MOVE_TROOPS = Button(image=None, pos=(640, 650),
                                text_input="Move Troops", font=get_font(40), base_color="White", hovering_color="Blue")

        ACTION_ADD_TROOPS.changeColor(PLAY_MOUSE_POS)
        ACTION_ATTACK.changeColor(PLAY_MOUSE_POS)
        ACTION_MOVE_TROOPS.changeColor(PLAY_MOUSE_POS)

        ACTION_ADD_TROOPS.update(SCREEN)
        ACTION_ATTACK.update(SCREEN)
        ACTION_MOVE_TROOPS.update(SCREEN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_territory = territories[turn.current_player_index]
                if ACTION_ADD_TROOPS.checkForInput(PLAY_MOUSE_POS):
                    current_territory.add_troops(troops_to_add)
                elif ACTION_ATTACK.checkForInput(PLAY_MOUSE_POS):
                    # Chama a função para escolher o território alvo
                    target_index = choose_target_territory(territories, current_territory.players[0])
                    target_territory = territories[target_index]
                    
                    # Verifica se o jogador escolheu seu próprio território
                    if current_territory is target_territory:
                        show_dialog(SCREEN, "You cannot attack your own territory!")
                    else:
                        troops_for_attack = show_input_dialog(SCREEN, "Enter the number of troops for the attack: ")
                        result = current_territory.attack(target_territory, troops_for_attack)

                        if result is not None:
                            combat_results.extend(result)

                        # Exibir o resultado do combate na tela
                        show_combat_results(SCREEN, combat_results)

                        # Agora, esperar até que o jogador pressione Enter para continuar
                        input_active = True
                        while input_active:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        input_active = False

                elif ACTION_MOVE_TROOPS.checkForInput(PLAY_MOUSE_POS):
                    pass

                current_player = turn.next_player()

def show_input_dialog(screen, prompt):
    input_active = True
    input_text = ""

    while input_active:
        screen.fill("white")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        input_value = int(input_text)
                        input_text = ""
                        input_active = False
                        return input_value
                    except ValueError:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    input_text += event.unicode

        PROMPT_TEXT = get_font(30).render(prompt, True, "Black")
        PROMPT_RECT = PROMPT_TEXT.get_rect(center=(640, 260))
        screen.blit(PROMPT_TEXT, PROMPT_RECT)

        input_rect = pygame.Rect(640 - 100, 350, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)
        input_surface = get_font(40).render(input_text, True, "Black")
        screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                             text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    num_players = get_num_players()
                    player_names = get_player_names(num_players)
                    play(num_players, player_names)
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
