# main.py
import pygame
import settings
from game import Game, MOVE_EVENT
import sys

KEY_DIR = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
}

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Snake - Pygame (logic modular)")
    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIR and not game.logic.game_over:
                    game.logic.set_direction(KEY_DIR[event.key])
                elif event.key == pygame.K_SPACE:
                    game.logic.toggle_pause()
                elif event.key == pygame.K_r:
                    game.reset_all()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break

            if event.type == MOVE_EVENT:
                game.handle_move()

        game.update()
        game.render()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
