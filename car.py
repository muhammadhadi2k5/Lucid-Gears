import pygame


class PlayerCar:
    """The car the player controls. For now: a rectangle that moves left/right."""

    WIDTH = 50
    HEIGHT = 80
    COLOR = (255, 90, 40)  # reddish-orange accent color
    SPEED = 400  # pixels per second

    def __init__(self, x, y):
        # x, y is the top-left corner of the car's rectangle.
        self.x = x
        self.y = y

        # Set by handle_input(), read by update(). Starting them as False
        # means the car sits still until a key is actually pressed.
        self.moving_left = False
        self.moving_right = False

    def handle_input(self, keys):
        # keys is the result of pygame.key.get_pressed() — a sequence where
        # keys[SOME_KEY] is True if that key is currently held down.
        self.moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

    def update(self, dt):
        # dt = seconds since the last frame.
        if self.moving_left:
            self.x -= self.SPEED * dt
        if self.moving_right:
            self.x += self.SPEED * dt

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        pygame.draw.rect(screen, self.COLOR, rect)
