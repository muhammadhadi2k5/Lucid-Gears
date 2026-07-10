import pygame

from .car import PlayerCar
from .game_over_menu import GameOverMenu
from .hud import HealthGauge
from .menu import StartMenu
from .obstacle_spawner import ObstacleSpawner
from .pause_menu import PauseMenu
from .road import Road
from .story import OBSTACLES_START_TIME, OPENING_SCRIPT, StoryManager

# shared here so nothing else has to hardcode these numbers
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


class Game:
    """Owns the main window and the game loop."""

    FADE_IN_DURATION = 1.5  # seconds for the black overlay to fully clear

    def __init__(self):
        pygame.init()  # always first, before any other pygame call

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lucid")

        self.clock = pygame.time.Clock()
        self.running = True

        # "state" is which mode the game is currently in. Everything in
        # _handle_events/_update/_draw branches on this, so only the menu (or
        # only the race) is ever active at once.
        self.state = "menu"
        self.menu = StartMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.game_over_menu = GameOverMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.health_gauge = HealthGauge(80, SCREEN_HEIGHT - 80)

        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))

        self._reset_race(start_faded_in=False)

    def _reset_race(self, start_faded_in=True):
        """(Re)creates everything about the race itself - road, car, and
        obstacles - so PLAY and RESTART can both funnel through one place.
        """
        self.road = Road(SCREEN_WIDTH, SCREEN_HEIGHT)

        start_x = SCREEN_WIDTH / 2 - PlayerCar.WIDTH / 2
        start_y = SCREEN_HEIGHT - PlayerCar.HEIGHT - 20
        self.player = PlayerCar(start_x, start_y)

        self.obstacle_spawner = ObstacleSpawner()
        self.story = StoryManager(OPENING_SCRIPT, SCREEN_WIDTH)

        # fade_alpha is how opaque the black overlay drawn on top of the race
        # is: 255 = fully black (nothing visible), 0 = fully cleared. It only
        # counts down while fade_alpha > 0, so it's a no-op the rest of the time.
        self.fade_alpha = 255.0 if start_faded_in else 0.0

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

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # ESC toggles pause: opens it from the race, closes it back
                # to the race - same as clicking CONTINUE.
                if self.state == "playing":
                    self.state = "paused"
                elif self.state == "paused":
                    self.state = "playing"

            if self.state == "menu":
                action = self.menu.handle_event(event)
                if action == "play":
                    self.state = "playing"
                    self.fade_alpha = 255.0  # start fully black, then fade out
                elif action == "exit":
                    self.running = False

            elif self.state == "paused":
                action = self.pause_menu.handle_event(event)
                if action == "continue":
                    self.state = "playing"
                elif action == "restart":
                    self._reset_race(start_faded_in=True)
                    self.state = "playing"
                elif action == "exit":
                    # back to the main menu, not a full app quit - reset now
                    # so the next PLAY starts a clean race with its own fade
                    self._reset_race(start_faded_in=False)
                    self.state = "menu"

            elif self.state == "game_over":
                action = self.game_over_menu.handle_event(event)
                if action == "restart":
                    self._reset_race(start_faded_in=True)
                    self.state = "playing"
                elif action == "exit":
                    self._reset_race(start_faded_in=False)
                    self.state = "menu"

        if self.state == "playing":
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)

    def _update(self, dt):
        if self.state == "menu":
            self.menu.update(dt)
            return

        if self.state == "paused":
            self.pause_menu.update(dt)
            return  # frozen: nothing about the race itself advances

        if self.state == "game_over":
            self.game_over_menu.update(dt)
            return

        self.road.update(dt)
        self.player.update(dt)

        left, right = self.road.edges_at_y(self.player.y + PlayerCar.HEIGHT)
        self.player.clamp_x(left, right)

        self.story.update(dt)

        # no obstacles until the AI has actually warned about them
        if self.story.elapsed >= OBSTACLES_START_TIME:
            self.obstacle_spawner.update(dt, self.road.SCROLL_SPEED)

        # hit_timer also doubles as invincibility, so a hit obstacle can't
        # be immediately followed by another one stacking more damage
        if self.player.hit_timer <= 0:
            if self.obstacle_spawner.check_collision(self.player.get_rect(), self.road):
                self.player.take_hit()

        if self.player.health <= 0:
            self.state = "game_over"
            return

        if self.fade_alpha > 0:
            fade_per_second = 255 / self.FADE_IN_DURATION
            self.fade_alpha = max(0.0, self.fade_alpha - fade_per_second * dt)

    def _draw(self):
        self.screen.fill((0, 0, 0))  # wipe last frame so nothing smears

        if self.state == "menu":
            self.menu.draw(self.screen)
        elif self.state == "game_over":
            self.game_over_menu.draw(self.screen)
        else:
            self.road.draw(self.screen)
            self.obstacle_spawner.draw(self.screen, self.road)
            self.player.draw(self.screen)

            segments = PlayerCar.MAX_HEALTH // PlayerCar.HIT_DAMAGE
            self.health_gauge.draw(self.screen, self.player.health, PlayerCar.MAX_HEALTH, segments)
            self.story.draw(self.screen)

            if self.fade_alpha > 0:
                self.fade_surface.set_alpha(int(self.fade_alpha))
                self.screen.blit(self.fade_surface, (0, 0))

            if self.state == "paused":
                self.pause_menu.draw(self.screen)

        pygame.display.flip()
