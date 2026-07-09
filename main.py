import pygame

from car import PlayerCar
from road import Road

# shared here so nothing else has to hardcode these numbers
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


class Game:
    """Owns the main window and the game loop."""

    def __init__(self):
        pygame.init()  # always first, before any other pygame call

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lucid Gears")

        self.clock = pygame.time.Clock()
        self.running = True

        self.road = Road(SCREEN_WIDTH, SCREEN_HEIGHT)

        start_x = SCREEN_WIDTH / 2 - PlayerCar.WIDTH / 2
        start_y = SCREEN_HEIGHT - PlayerCar.HEIGHT - 20
        self.player = PlayerCar(start_x, start_y)

    def run(self):
        """The main game loop: handle input, update, draw. Repeat."""
        while self.running:
            # tick(FPS) caps the frame rate and hands back how long the last
            # frame took, in ms - divide by 1000 to get dt in seconds
            dt = self.clock.tick(FPS) / 1000

            self._handle_events()
            self._update(dt)
            self._draw()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def _update(self, dt):
        self.road.update(dt)
        self.player.update(dt)

    def _draw(self):
        self.screen.fill((0, 0, 0))  # wipe last frame so nothing smears
        self.road.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
