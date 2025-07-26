import pygame


def menushka(screen):
    '''  tmp
    player1 = Player1(10, 300, 500, screen)
    player2 = Player2(10, 700, 500, screen)
    '''
    player1 = player2 = None
    curr_p1_idx = curr_p2_idx = 0
    curr_player = 1  # 1 -> player1; -1 -> player2
    player_images = [
        pygame.image.load('images/борян-база.png').convert_alpha(),  # борян
        pygame.image.load('images/base.png').convert_alpha()         # свш
    ]
    player1_rect = pygame.Rect(100, 100, 300, 500)
    player2_rect = pygame.Rect(800, 100, 300, 500)

    font = pygame.font.SysFont('SysFont', 52)
    text1 = font.render('Выберите бойца', False, (255, 255, 255))
    font_small = pygame.font.SysFont('SysFont', 32)

    screen.fill((0, 0, 0))
    screen.blit(text1, (460, 100))

    #
    while (player1 is None) or (player2 is None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (player1, player2)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # переключение панелей
                    curr_player *= -1

                elif event.key == pygame.K_RETURN:  # выбор игрока
                    if curr_player == 1 and player1 is None:
                        player1 = Player1(10, 300, 500, screen, [player_images[curr_p1_idx], None, None, None, None])

                    elif curr_player == -1 and player2 is None:
                        player2 = Player2(10, 300, 500, screen, [player_images[curr_p2_idx], None, None, None, None])

                elif event.key == pygame.K_DOWN:  # переключение игроков
                    curr_p1_idx = (curr_p1_idx - 1) % len(player_images)

                elif event.key == pygame.K_UP:
                    curr_p2_idx = (curr_p2_idx + 1) % len(player_images)

        # переключение квадратов
        if curr_player == 1:
            pygame.draw.rect(screen, GREEN, player1_rect, 8)
            pygame.draw.rect(screen, GREY, player2_rect, 8)
        else:
            pygame.draw.rect(screen, GREY, player1_rect, 8)
            pygame.draw.rect(screen, GREEN, player2_rect, 8)

        # рисование бойцов
        screen.blit(player_images[curr_p2_idx], player_images[curr_p2_idx].get_rect())
        screen.blit(player_images[curr_p1_idx], player_images[curr_p1_idx].get_rect())

        if player1 is not None:
            text_selected1 = font_small.render("Боец 1 выбран", True, RED)
            screen.blit(text_selected1, (player1_rect.centerx - text_selected1.get_width() // 2, player1_rect.bottom + 10))
        if player2 is not None:
            text_selected2 = font_small.render("Боец 2 выбран", True, RED)
            screen.blit(text_selected2, (player2_rect.centerx - text_selected2.get_width() // 2, player2_rect.bottom + 10))
        pygame.display.flip()

    sleep(1)
    return (player1, player2)