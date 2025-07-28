import pygame
from players import Player


def menushka(screen):
    player1_instance = player2_instance = None  # игроки изначально не выбраны
    curr_p1_idx = curr_p2_idx = 0
    curr_section = 1  # 1 -> player1; -1 -> player2
    plus = 1

    players = Player.players  # Список классов игроков

    player1_rect = pygame.Rect(100, 100, 300, 500)
    player2_rect = pygame.Rect(800, 100, 300, 500)

    font = pygame.font.SysFont('SysFont', 52)
    text1 = font.render('Выберите бойца', False, (255, 255, 255))
    font_small = pygame.font.SysFont('SysFont', 32)

    while (player1_instance is None) or (player2_instance is None):
        screen.fill((0, 0, 0))
        screen.blit(text1, (460, 100))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return player1_instance, player2_instance

            elif event.type == pygame.KEYDOWN:
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
                                "attack": pygame.K_RCTRL
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
                                "attack": pygame.K_f
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

        # переключение квадратов
        if curr_section == 1:
            pygame.draw.rect(screen, (0, 255, 0), player1_rect, 8)
            pygame.draw.rect(screen, (50, 50, 50), player2_rect, 8)
        else:
            pygame.draw.rect(screen, (50, 50, 50), player1_rect, 8)
            pygame.draw.rect(screen, (0, 255, 0), player2_rect, 8)

        # рисование бойцов
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

        pygame.display.flip()

    return player1_instance, player2_instance


if __name__ == '__main__':  # просто пример

    player_list = Player.players

    for player_class in player_list:
        print(player_class)
