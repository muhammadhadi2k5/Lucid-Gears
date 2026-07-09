import pygame

from car import PlayerCar
from obstacle import Obstacle
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
        pygame.display.set_caption("Lucid")

        self.clock = pygame.time.Clock()
        self.running = True

        self.road = Road(SCREEN_WIDTH, SCREEN_HEIGHT)

        start_x = SCREEN_WIDTH / 2 - PlayerCar.WIDTH / 2
        start_y = SCREEN_HEIGHT - PlayerCar.HEIGHT - 20
        self.player = PlayerCar(start_x, start_y)

        # TEMPORARY: a couple of obstacles so we can see the class work
        # before building a real spawner. Both start at the horizon
        # (depth=0); one is static (speed=0), one is oncoming (speed>0) so
        # it closes the distance faster and passes the static one.
        self.obstacles = [
            Obstacle(offset=0.4, speed=0.0),
            Obstacle(offset=-0.3, speed=0.1),
        ]

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

        left, right = self.road.edges_at_y(self.player.y + PlayerCar.HEIGHT)
        self.player.clamp_x(left, right)

        for obstacle in self.obstacles:
            obstacle.update(dt, self.road.SCROLL_SPEED)

    def _draw(self):
        self.screen.fill((0, 0, 0))  # wipe last frame so nothing smears
        self.road.draw(self.screen)
        for obstacle in self.obstacles:
            if not obstacle.is_off_screen():
                obstacle.draw(self.screen, self.road)
        self.player.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
