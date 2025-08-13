# main.py
# Punto de entrada único: intenta usar menu.py (pygame). Si no está, cae al modo directo.
import sys

def run():
    try:
        # preferimos el menú en pygame
        import menu
        if hasattr(menu, "run"):
            menu.run()
            return
        else:
            print("menu.py encontrado pero no tiene 'run()'. Arrancando game directo...")
            raise ImportError("menu.run missing")
    except Exception:
        # fallback: intentar iniciar game directamente (por compatibilidad)
        try:
            import pygame
            from game import Game, MOVE_EVENT
            import settings
        except Exception as e2:
            print("No se pudo arrancar el menú ni el juego directamente. Error:", e2)
            sys.exit(1)

        # Modo simple: crear la ventana y ejecutar loop similar al antiguo main.py
        pygame.init()
        screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Snake - Fallback (directo)")
        clock = pygame.time.Clock()
        game = Game(screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset_all()
                    elif event.key == pygame.K_SPACE:
                        game.logic.toggle_pause()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        break
                if event.type == MOVE_EVENT:
                    game.handle_move()

            # keyboard continuous input for direction
            keys = pygame.key.get_pressed()
            if not game.logic.game_over:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    game.logic.set_direction((0, -1))
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    game.logic.set_direction((0, 1))
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    game.logic.set_direction((-1, 0))
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    game.logic.set_direction((1, 0))

            game.update()
            game.render()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    run()
