import pygame
from players import Player1, Player2
# from background import *
from time import sleep
from threading import Thread

WIDTH, HEIGHT = 1400, 700
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def main():
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DIALOG-KOMBAT")
    running = True

    player1 = Player1(10, 300, 500, screen)
    player2 = Player2(10, 700, 500, screen)
    st1 = Thread(target=strike_th, args=(player1,), daemon=True)
    st2 = Thread(target=strike_th, args=(player2,), daemon=True)

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        strike1 = strike2 = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    strike1 = True
                if event.key == pygame.K_5:
                    strike2 = True

        keys = pygame.key.get_pressed()

        if strike1 and not st1.is_alive():
            st1 = Thread(target=strike_th, args=(player1,), daemon=True)
            st1.start()
        if strike2 and not st2.is_alive():
            st2 = Thread(target=strike_th, args=(player2,), daemon=True)
            st2.start()

        player1.move(keys)
        player1.draw()
        player2.move(keys)
        player2.draw()

        pygame.display.flip()


def strike_th (player1):
    pause = 0.35 / 3
    player1.change_texture(2)
    sleep(pause)
    player1.change_texture(3)
    sleep(pause)
    player1.change_texture(4)
    sleep(pause)
    player1.change_texture(0)


if __name__ == '__main__':
    main()
