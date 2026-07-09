import pygame

from car import PlayerCar

# Window size, in pixels. Defined once here so every other class can
# reference these same numbers instead of guessing at hardcoded values.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


class Game:
    """Owns the main window and the game loop."""

    def __init__(self):
        # pygame.init() sets up all of pygame's internal systems
        # (display, input, timing, etc.) — must be called before anything else.
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lucid Gears")

        # Clock lets us cap the loop at a fixed frame rate (see run() below).
        self.clock = pygame.time.Clock()

        # Controls whether the loop below keeps running.
        self.running = True

        # Start the car roughly centered horizontally, near the bottom.
        start_x = SCREEN_WIDTH / 2 - PlayerCar.WIDTH / 2
        start_y = SCREEN_HEIGHT - PlayerCar.HEIGHT - 20
        self.player = PlayerCar(start_x, start_y)

    def run(self):
        """The main game loop: handle input, update, draw. Repeat."""
        while self.running:
            # clock.tick(FPS) both caps the frame rate AND tells us how many
            # milliseconds the last frame took. Divide by 1000 to get dt in
            # seconds, which is what PlayerCar.update() expects.
            dt = self.clock.tick(FPS) / 1000

            self._handle_events()
            self._update(dt)
            self._draw()

        pygame.quit()

    def _handle_events(self):
        # pygame queues up everything that happened since we last checked
        # (key presses, mouse clicks, the window's close button, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # get_pressed() gives the current held-down state of every key,
        # which is what we want for "steer while the key is held."
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

    def _update(self, dt):
        self.player.update(dt)

    def _draw(self):
        # Fill the whole screen with black before drawing anything else,
        # otherwise each frame would paint over the last one and smear.
        self.screen.fill((0, 0, 0))

        self.player.draw(self.screen)

        # Flip the newly drawn frame onto the actual visible window.
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
