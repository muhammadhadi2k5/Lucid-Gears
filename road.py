import pygame


class Road:
    """Draws a scrolling pseudo-3D wireframe road, Out Run style."""

    TOP_WIDTH = 40      # road width at the horizon
    BOTTOM_WIDTH = 700   # road width at the bottom of the screen
    RUNG_COUNT = 12      # number of scrolling crossbars
    SCROLL_SPEED = 0.6   # full road-length cycles per second

    ROAD_COLOR = (20, 20, 30)
    EDGE_COLOR = (255, 90, 40)

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_x = screen_width / 2
        self.horizon_y = screen_height * 0.4
        self.scroll = 0.0

    def update(self, dt):
        self.scroll = (self.scroll + self.SCROLL_SPEED * dt) % 1.0

    def draw(self, screen):
        pygame.draw.line(
            screen, self.EDGE_COLOR,
            (0, self.horizon_y), (self.screen_width, self.horizon_y),
        )
        self._draw_surface(screen)
        self._draw_rungs(screen)

    def _width_at(self, depth):
        eased = depth ** 2
        return self.TOP_WIDTH + (self.BOTTOM_WIDTH - self.TOP_WIDTH) * eased

    def _y_at(self, depth):
        eased = depth ** 2
        return self.horizon_y + (self.screen_height - self.horizon_y) * eased

    def _depth_at_y(self, y):
        # inverse of _y_at - undo the square with a square root
        fraction = (y - self.horizon_y) / (self.screen_height - self.horizon_y)
        return fraction ** 0.5

    def edges_at_y(self, y):
        """Left/right x of the road at a given screen y, for keeping the car on it."""
        width = self._width_at(self._depth_at_y(y))
        return self.center_x - width / 2, self.center_x + width / 2

    def _draw_surface(self, screen):
        top_w = self._width_at(0)
        bottom_w = self._width_at(1)
        points = [
            (self.center_x - top_w / 2, self.horizon_y),
            (self.center_x + top_w / 2, self.horizon_y),
            (self.center_x + bottom_w / 2, self.screen_height),
            (self.center_x - bottom_w / 2, self.screen_height),
        ]
        pygame.draw.polygon(screen, self.ROAD_COLOR, points)
        pygame.draw.polygon(screen, self.EDGE_COLOR, points, width=2)

    def _draw_rungs(self, screen):
        depth_step = 1 / self.RUNG_COUNT
        for i in range(self.RUNG_COUNT):
            depth = (i * depth_step + self.scroll) % 1.0
            y = self._y_at(depth)
            width = self._width_at(depth)
            left = self.center_x - width / 2
            right = self.center_x + width / 2
            pygame.draw.line(screen, self.EDGE_COLOR, (left, y), (right, y), 2)
