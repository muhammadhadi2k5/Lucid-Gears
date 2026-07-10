import pygame


class Button:
    """A button face that slides down into a wall when pressed."""

    DEPTH = 10     # how far the face sits from the wall, and how far it slides on press
    CHAMFER = 8    # size of the diagonal cut on the face's bottom side

    def __init__(self, center_x, center_y, width, height, label, font,
                 base_color, hover_color, pressed_color,
                 base_text_color, hover_text_color):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (center_x, center_y)
        self.label = label
        self.font = font

        self.base_color = base_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.base_text_color = base_text_color
        self.hover_text_color = hover_text_color

        self.hovered = False
        self.pressed = False

    def update(self, mouse_pos, mouse_button_down):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.pressed = self.hovered and mouse_button_down

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        wall_rect = self.rect.move(0, self.DEPTH)
        pygame.draw.rect(screen, (15, 15, 15), wall_rect)

        if self.pressed:
            face_color = self.pressed_color
            text_color = self.hover_text_color
        elif self.hovered:
            face_color = self.hover_color
            text_color = self.hover_text_color
        else:
            face_color = self.base_color
            text_color = self.base_text_color

        offset = self.DEPTH if self.pressed else 0
        face_rect = self.rect.move(0, offset)

        # bottom side is one diagonal (not two mirrored notches) - see chat history for why
        left, right = face_rect.left, face_rect.right
        top, bottom = face_rect.top, face_rect.bottom
        chamfer = min(self.CHAMFER, (bottom - top) / 2, (right - left) / 2)

        face_polygon = [
            (left, bottom - chamfer),
            (left, top),
            (right, top),
            (right - chamfer, bottom),
        ]
        pygame.draw.polygon(screen, face_color, face_polygon)

        if not self.pressed:
            light_edge = self._shade(face_color, 50)
            dark_edge = self._shade(face_color, -50)
            pygame.draw.line(screen, light_edge, (left, bottom - chamfer), (left, top), 3)
            pygame.draw.line(screen, light_edge, (left, top), (right, top), 3)
            pygame.draw.line(screen, dark_edge, (right, top), (right - chamfer, bottom), 3)

        text_surface = self.font.render(self.label, True, text_color)
        text_rect = text_surface.get_rect(center=face_rect.center)
        screen.blit(text_surface, text_rect)

    @staticmethod
    def _shade(color, amount):
        return tuple(max(0, min(255, channel + amount)) for channel in color)


class StartMenu:
    """Main menu: blinking "LUCID." title + Play/Exit buttons."""

    TITLE_COLOR = (255, 90, 40)

    BUTTON_BASE_COLOR = (255, 90, 40)
    BUTTON_HOVER_COLOR = (74, 26, 130)
    BUTTON_PRESSED_COLOR = (46, 16, 82)

    BUTTON_BASE_TEXT_COLOR = (0, 0, 0)
    BUTTON_HOVER_TEXT_COLOR = (255, 255, 255)

    CURSOR_BLINK_INTERVAL = 0.5  # seconds

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont("consolas,couriernew,monospace", 72, bold=True)
        self.button_font = pygame.font.SysFont("consolas,couriernew,monospace", 32, bold=True)

        self.cursor_visible = True
        self.cursor_timer = 0.0

        center_x = screen_width / 2
        self.play_button = Button(
            center_x, screen_height * 0.55, 220, 60, "PLAY", self.button_font,
            self.BUTTON_BASE_COLOR, self.BUTTON_HOVER_COLOR, self.BUTTON_PRESSED_COLOR,
            self.BUTTON_BASE_TEXT_COLOR, self.BUTTON_HOVER_TEXT_COLOR,
        )
        self.exit_button = Button(
            center_x, screen_height * 0.68, 220, 60, "EXIT", self.button_font,
            self.BUTTON_BASE_COLOR, self.BUTTON_HOVER_COLOR, self.BUTTON_PRESSED_COLOR,
            self.BUTTON_BASE_TEXT_COLOR, self.BUTTON_HOVER_TEXT_COLOR,
        )

    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= self.CURSOR_BLINK_INTERVAL:
            self.cursor_timer = 0.0
            self.cursor_visible = not self.cursor_visible

        mouse_pos = pygame.mouse.get_pos()
        mouse_button_down = pygame.mouse.get_pressed()[0]
        self.play_button.update(mouse_pos, mouse_button_down)
        self.exit_button.update(mouse_pos, mouse_button_down)

    def handle_event(self, event):
        # fire on release, not press, so the pressed visual is visible for a moment
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.play_button.is_clicked(event.pos):
                return "play"
            if self.exit_button.is_clicked(event.pos):
                return "exit"
        return None

    def draw(self, screen):
        title_surface = self.title_font.render("LUCID", True, self.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(self.screen_width / 2, self.screen_height * 0.3))
        screen.blit(title_surface, title_rect)

        if self.cursor_visible:
            cursor_surface = self.title_font.render(".", True, self.TITLE_COLOR)
            screen.blit(cursor_surface, (title_rect.right + 6, title_rect.top))

        self.play_button.draw(screen)
        self.exit_button.draw(screen)
