import pygame


class PlayerCar:
    """The car the player controls. For now: a rectangle that moves left/right."""

    WIDTH = 50
    HEIGHT = 80
    COLOR = (255, 90, 40)  # reddish-orange accent color
    SPEED = 400  # pixels per second

    MAX_HEALTH = 100
    HIT_DAMAGE = 20
    HIT_DURATION = 1.0          # seconds of slowdown + flash after a hit, also the invincibility window
    HIT_SPEED_MULTIPLIER = 0.4  # how much slower the car moves while hit_timer is active
    FLASH_INTERVAL = 0.08       # seconds between flash colors
    FLASH_COLORS = [(220, 30, 30), (10, 10, 10), (255, 220, 40)]  # red, black, yellow

    def __init__(self, x, y):
        # x, y is the top-left corner of the car's rectangle.
        self.x = x
        self.y = y

        # Set by handle_input(), read by update(). Starting them as False
        # means the car sits still until a key is actually pressed.
        self.moving_left = False
        self.moving_right = False

        self.health = self.MAX_HEALTH
        self.hit_timer = 0.0  # >0 means recently hit: flashing, slowed, invincible

    def handle_input(self, keys):
        # keys is the result of pygame.key.get_pressed() — a sequence where
        # keys[SOME_KEY] is True if that key is currently held down.
        self.moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

    def take_hit(self):
        self.health = max(0, self.health - self.HIT_DAMAGE)
        self.hit_timer = self.HIT_DURATION

    def update(self, dt):
        speed = self.SPEED
        if self.hit_timer > 0:
            self.hit_timer = max(0.0, self.hit_timer - dt)
            speed *= self.HIT_SPEED_MULTIPLIER

        if self.moving_left:
            self.x -= speed * dt
        if self.moving_right:
            self.x += speed * dt

    def clamp_x(self, left, right):
        self.x = max(left, min(self.x, right - self.WIDTH))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def draw(self, screen):
        color = self.COLOR
        if self.hit_timer > 0:
            elapsed = self.HIT_DURATION - self.hit_timer
            flash_index = int(elapsed / self.FLASH_INTERVAL) % len(self.FLASH_COLORS)
            color = self.FLASH_COLORS[flash_index]
        pygame.draw.rect(screen, color, self.get_rect())
