import pygame

from game import SnakeGame


def main():
    pygame.init()
    pygame.mixer.quit()
    game = SnakeGame()
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()