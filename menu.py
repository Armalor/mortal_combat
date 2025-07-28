import pygame
from players import Player


def menushka(screen):
    player1_instance = player2_instance = None  # игроки изначально не выбраны
    curr_p1_idx = curr_p2_idx = 0
    curr_section = 1  # 1 -> player1; -1 -> player2
    plus = 1
    show_instructions = False

    players = Player.players  # Список классов игроков

    # Load background textures
    try:
        bg_choose = pygame.image.load('textures/pchoosebck.png').convert_alpha()
        bg_p1 = pygame.image.load('textures/p1bck.png').convert_alpha()
        bg_p2 = pygame.image.load('textures/p2bck.png').convert_alpha()

        # Scale backgrounds to fit the selection areas
        bg_choose = pygame.transform.scale(bg_choose, (screen.get_width(), screen.get_height()))
        bg_p1 = pygame.transform.scale(bg_p1, (300, 500))
        bg_p2 = pygame.transform.scale(bg_p2, (300, 500))
    except:
        # Fallback if textures are missing
        bg_choose = pygame.Surface((screen.get_width(), screen.get_height()))
        bg_choose.fill((0, 0, 0))
        bg_p1 = pygame.Surface((300, 500))
        bg_p1.fill((50, 0, 0))
        bg_p2 = pygame.Surface((300, 500))
        bg_p2.fill((0, 0, 50))

    player1_rect = pygame.Rect(100, 100, 300, 500)
    player2_rect = pygame.Rect(800, 100, 300, 500)

    font = pygame.font.SysFont('SysFont', 52)
    font_small = pygame.font.SysFont('SysFont', 32)
    font_instructions = pygame.font.SysFont('SysFont', 24)

    # Instruction texts
    instruction_prompt = font_small.render("Нажмите F1 для инструкций", True, (255, 255, 255))

    instruction_texts = [
        "Для выбора персонажа:",
        "- Используйте стрелочки ВВЕРХ/ВНИЗ для выбора персонажа",
        "- Нажмите ENTER для подтверждения выбора",
        "- Нажмите TAB для переключения между игроками",
        "",
        "Управление в игре:",
        "Игрок 1:",
        "- A/D для движения",
        "- Q/W/E для атак и S для блока",
        "",
        "Игрок 2:",
        "- Стрелочки ВЛЕВО/ВПРАВО для движения",
        "- ctrl/ВВЕРХ/shift для атак и вниз для блока"
    ]

    while (player1_instance is None) or (player2_instance is None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return player1_instance, player2_instance

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:  # Toggle instructions
                    show_instructions = not show_instructions

                if not show_instructions:
                    if event.key == pygame.K_TAB:  # переключение панелей
                        curr_section *= -1

                    elif event.key == pygame.K_RETURN:  # выбор игрока
                        if curr_section == 1 and player1_instance is None:  # если не выбран первый игрок
                            player1_instance = players[curr_p1_idx](
                                x=200,
                                y=690,
                                screen=screen,
                                controls={
                                    "left": pygame.K_d,
                                    "right": pygame.K_a,
                                    "attack": pygame.K_DOWN,
                                    "block": pygame.K_UP,
                                    "jump": pygame.K_RCTRL,
                                    "aperkot": pygame.K_RSHIFT,
                                    "magic": pygame.K_SLASH,
                                },
                                flip=True,
                                is_player1=True
                            )
                        elif curr_section == -1 and player2_instance is None:
                            player2_instance = players[curr_p2_idx](
                                x=700,
                                y=690,
                                screen=screen,
                                controls={
                                    "left": pygame.K_RIGHT,
                                    "right": pygame.K_LEFT,
                                    "attack": pygame.K_s,
                                    "block": pygame.K_w,
                                    "jump": pygame.K_e,
                                    "aperkot": pygame.K_q,
                                    "magic": pygame.K_x,
                                },
                                flip=False,
                                is_player1=False
                            )

                    elif event.key == pygame.K_DOWN:  # переключение игроков
                        plus = 1
                    elif event.key == pygame.K_UP:
                        plus = -1

                    #
                    if player1_instance is None and curr_section == 1:
                        curr_p1_idx = (curr_p1_idx + plus) % len(players)
                    if player2_instance is None and curr_section == -1:
                        curr_p2_idx = (curr_p2_idx + plus) % len(players)

        # Draw everything
        screen.blit(bg_choose, (0, 0))

        if not show_instructions:
            # Draw character selection screen
            screen.blit(bg_p1, player1_rect)
            screen.blit(bg_p2, player2_rect)

            # Draw green outline for current selection
            if curr_section == 1:
                pygame.draw.rect(screen, (0, 255, 0), player1_rect, 8)
            else:
                pygame.draw.rect(screen, (0, 255, 0), player2_rect, 8)

            # Draw characters
            player_img1 = pygame.image.load(players[curr_p1_idx].TEXTURES[0])
            player_img1_rect = player_img1.get_rect(center=(250, 350))

            player_img2 = pygame.image.load(players[curr_p2_idx].TEXTURES[0])
            player_img2_rect = player_img2.get_rect(center=(950, 350))

            screen.blit(player_img1, player_img1_rect)
            screen.blit(player_img2, player_img2_rect)

            if player1_instance is not None:
                text_selected1 = font_small.render("Боец 1 выбран", True, (255, 0, 0))
                screen.blit(text_selected1,
                            (player1_rect.centerx - text_selected1.get_width() // 2, player1_rect.bottom + 10))
            if player2_instance is not None:
                text_selected2 = font_small.render("Боец 2 выбран", True, (255, 0, 0))
                screen.blit(text_selected2,
                            (player2_rect.centerx - text_selected2.get_width() // 2, player2_rect.bottom + 10))
        else:
            # Draw instructions screen
            instruction_title = font.render("Инструкции", True, (255, 255, 0))
            screen.blit(instruction_title, (screen.get_width() // 2 - instruction_title.get_width() // 2, 100))

            for i, line in enumerate(instruction_texts):
                text = font_instructions.render(line, True, (255, 255, 255))
                screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 180 + i * 30))

            back_text = font_small.render("Нажмите F1 чтобы вернуться", True, (255, 255, 0))
            screen.blit(back_text, (screen.get_width() // 2 - back_text.get_width() // 2, 650))

        # Always show instruction prompt if not in instructions screen
        if not show_instructions:
            screen.blit(instruction_prompt,
                        (screen.get_width() // 2 - instruction_prompt.get_width() // 2,
                         screen.get_height() - 50))

        pygame.display.flip()

    return player1_instance, player2_instance


if __name__ == '__main__':  # просто пример
    player_list = Player.players
    for player_class in player_list:
        print(player_class)