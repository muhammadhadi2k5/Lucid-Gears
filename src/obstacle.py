import pygame


class Obstacle:
    """A single piece of AI infrastructure blocking the road - a barricade,
    drone, or conduit the player has to dodge.

    Position is stored in "road space", not screen pixels:
    - depth: 0.0 at the horizon, 1.0 at the bottom of the screen. Same idea
      as the depth the Road class already uses for its scrolling rungs.
    - offset: -1.0 (left edge of the road) to 1.0 (right edge), 0.0 is dead
      center. Because it's a fraction of the road's width rather than a
      fixed pixel position, the obstacle automatically narrows in toward
      the horizon along with the road, instead of us doing that math here.
    """

    SIZE_FRACTION = 0.18  # obstacle width, as a fraction of the road's width at its depth
    HEIGHT_RATIO = 0.6    # obstacle height, as a fraction of its own width
    COLOR = (60, 220, 255)  # cold cyan - reads as "AI", contrasts with the car's orange

    def __init__(self, offset, speed, depth=0.0):
        self.offset = offset
        self.depth = depth
        # speed is EXTRA depth gained per second, on top of the road's own
        # scroll. 0 means the obstacle is static and only approaches because
        # the road is scrolling past it, like the rungs do. >0 means it's
        # oncoming - closing the distance faster than the road alone would.
        self.speed = speed

    def update(self, dt, road_scroll_speed):
        self.depth += (road_scroll_speed + self.speed) * dt

    def is_off_screen(self):
        return self.depth > 1.0

    def get_rect(self, road):
        width = road.width_at(self.depth) * self.SIZE_FRACTION
        height = width * self.HEIGHT_RATIO
        center_x = road.x_at(self.depth, self.offset)
        bottom_y = road.y_at(self.depth)
        return pygame.Rect(center_x - width / 2, bottom_y - height, width, height)

    def draw(self, screen, road):
        pygame.draw.rect(screen, self.COLOR, self.get_rect(road))
