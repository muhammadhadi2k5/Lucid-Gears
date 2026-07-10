import random

from .obstacle import Obstacle


class ObstacleSpawner:
    """Decides when new obstacles appear, and keeps the list of active ones current."""

    MIN_INTERVAL = 1  # shortest gap between spawns, in seconds
    MAX_INTERVAL = 3  # longest gap between spawns, in seconds

    OFFSET_RANGE = 0.8  # spawn within the middle 80% of the road width, not hugging the very edge

    STATIC_CHANCE = 0.6  # fraction of spawns that are static rather than oncoming
    ONCOMING_SPEED_RANGE = (0.05, 0.15)  # extra depth/sec on top of the road's own scroll

    def __init__(self):
        self.obstacles = []
        self.time_until_next_spawn = self._random_interval()

    def _random_interval(self):
        return random.uniform(self.MIN_INTERVAL, self.MAX_INTERVAL)

    def _spawn(self):
        offset = random.uniform(-self.OFFSET_RANGE, self.OFFSET_RANGE)

        if random.random() < self.STATIC_CHANCE:
            speed = 0.0
        else:
            speed = random.uniform(*self.ONCOMING_SPEED_RANGE)

        self.obstacles.append(Obstacle(offset=offset, speed=speed))

    def update(self, dt, road_scroll_speed):
        self.time_until_next_spawn -= dt
        if self.time_until_next_spawn <= 0:
            self._spawn()
            self.time_until_next_spawn = self._random_interval()

        for obstacle in self.obstacles:
            obstacle.update(dt, road_scroll_speed)

        # drop anything that's scrolled past the bottom of the screen, so the
        # list doesn't grow forever
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

    def check_collision(self, player_rect, road):
        # removes the first obstacle the player touches and reports the hit -
        # only one hit per frame matters since Game grants invincibility after
        for obstacle in self.obstacles:
            if obstacle.get_rect(road).colliderect(player_rect):
                self.obstacles.remove(obstacle)
                return True
        return False

    def draw(self, screen, road):
        for obstacle in self.obstacles:
            obstacle.draw(screen, road)
