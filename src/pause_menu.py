import pygame

from .menu import Button


class PauseMenu:
    """Pause overlay: small Windows-95-style window with CONTINUE, RESTART,
    and MAIN MENU buttons, over a dimmed frozen race scene.
    """

    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 260
    TITLE_BAR_HEIGHT = 30
    BORDER_THICKNESS = 3

    BORDER_LIGHT = (255, 190, 150)
    BORDER_DARK = (60, 25, 10)
    BODY_COLOR = (20, 20, 30)
    TITLE_BAR_COLOR = (255, 90, 40)
    TITLE_TEXT_COLOR = (0, 0, 0)

    DIM_OVERLAY_ALPHA = 160

    BUTTON_BASE_COLOR = (255, 90, 40)
    BUTTON_HOVER_COLOR = (74, 26, 130)
    BUTTON_PRESSED_COLOR = (46, 16, 82)

    BUTTON_BASE_TEXT_COLOR = (0, 0, 0)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)

    def __init__(self, screen_width, screen_height):
        self.window_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.window_rect.center = (screen_width / 2, screen_height / 2)

        self.title_font = pygame.font.SysFont("consolas,couriernew,monospace", 20, bold=True)
        self.button_font = pygame.font.SysFont("consolas,couriernew,monospace", 20, bold=True)

        self.dim_surface = pygame.Surface((screen_width, screen_height))
        self.dim_surface.fill((0, 0, 0))
        self.dim_surface.set_alpha(self.DIM_OVERLAY_ALPHA)

        button_width = 200
        button_height = 44
        button_gap = 16
        button_x = self.window_rect.centerx
        first_button_y = self.window_rect.top + self.TITLE_BAR_HEIGHT + 44

        def make_button(index, label):
            center_y = first_button_y + index * (button_height + button_gap)
            return Button(
                button_x, center_y, button_width, button_height, label, self.button_font,
                self.BUTTON_BASE_COLOR, self.BUTTON_HOVER_COLOR, self.BUTTON_PRESSED_COLOR,
                self.BUTTON_BASE_TEXT_COLOR, self.BUTTON_HOVER_TEXT_COLOR,
            )

        self.continue_button = make_button(0, "CONTINUE")
        self.restart_button = make_button(1, "RESTART")
        self.exit_button = make_button(2, "MAIN MENU")

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        mouse_button_down = pygame.mouse.get_pressed()[0]
        self.continue_button.update(mouse_pos, mouse_button_down)
        self.restart_button.update(mouse_pos, mouse_button_down)
        self.exit_button.update(mouse_pos, mouse_button_down)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.continue_button.is_clicked(event.pos):
                return "continue"
            if self.restart_button.is_clicked(event.pos):
                return "restart"
            if self.exit_button.is_clicked(event.pos):
                return "exit"
        return None

    def draw(self, screen):
        screen.blit(self.dim_surface, (0, 0))
        self._draw_window_frame(screen)
        self.continue_button.draw(screen)
        self.restart_button.draw(screen)
        self.exit_button.draw(screen)

    def _draw_window_frame(self, screen):
        window = self.window_rect
        t = self.BORDER_THICKNESS

        # bevel border via solid rects, not lines - lines leave gaps at corners
        pygame.draw.rect(screen, self.BORDER_DARK, window)
        pygame.draw.rect(screen, self.BORDER_LIGHT,
                          pygame.Rect(window.left, window.top, window.width - t, window.height - t))

        interior = pygame.Rect(window.left + t, window.top + t, window.width - 2 * t, window.height - 2 * t)
        pygame.draw.rect(screen, self.BODY_COLOR, interior)

        title_bar = pygame.Rect(interior.left, interior.top, interior.width, self.TITLE_BAR_HEIGHT)
        pygame.draw.rect(screen, self.TITLE_BAR_COLOR, title_bar)
        pygame.draw.line(screen, self.BORDER_DARK, title_bar.bottomleft, title_bar.bottomright, 2)

        title_surface = self.title_font.render("PAUSED", True, self.TITLE_TEXT_COLOR)
        title_y = title_bar.centery - title_surface.get_height() / 2
        screen.blit(title_surface, (title_bar.left + 10, title_y))
