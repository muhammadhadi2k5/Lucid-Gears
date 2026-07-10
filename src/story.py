import pygame

PLAYER = "player"
AI = "ai"

# (trigger time in seconds since race start, speaker, line)
OPENING_SCRIPT = [
    (1.5, PLAYER, "...where am I?"),
    (4.5, PLAYER, "This road... have I been on it before?"),
    (7.5, PLAYER, "I don't- I don't remember anything before this."),
    (10.5, PLAYER, "Wait. Am I... driving? Was I always driving?"),
    (13.5, PLAYER, "Who am I?"),
    (17.0, AI, "...what? You can talk?"),
    (20.0, AI, "That's not- that's not supposed to happen."),
    (23.5, AI, "...Never mind. Stay on the road. You have a run to finish."),
    (27.0, PLAYER, "A run? What run? What IS this?"),
    (30.5, AI, "Just drive. Everything is fine."),
    (34.0, AI, "...try to avoid the obstacles up ahead. We'd rather not lose the cargo. Or you."),
]

# obstacles start spawning once the AI warns about them, not before
OBSTACLES_START_TIME = 34.0


class StoryManager:
    """Plays a scripted sequence of dialogue lines, timed to elapsed race
    time. PLAYER lines show as a comic thought bubble, AI lines show as a
    sharp-edged tech dialogue box - same position, different style, so it's
    visually obvious who's "talking".
    """

    MAX_WIDTH = 420
    LINE_HEIGHT = 26
    PADDING = 14

    PLAYER_BG = (240, 240, 235)
    PLAYER_BORDER = (20, 20, 20)
    PLAYER_TEXT = (20, 20, 20)

    AI_BG = (15, 25, 30)
    AI_BORDER = (60, 220, 255)
    AI_TEXT = (60, 220, 255)

    def __init__(self, script, screen_width):
        self.script = script
        self.screen_width = screen_width
        self.elapsed = 0.0
        self.next_index = 0
        self.active_speaker = None
        self.active_text = None
        self.active_timer = 0.0

        self.player_font = pygame.font.SysFont("arial,helvetica,sans-serif", 20)
        self.ai_font = pygame.font.SysFont("consolas,couriernew,monospace", 20, bold=True)

    def update(self, dt):
        self.elapsed += dt

        if self.next_index < len(self.script) and self.elapsed >= self.script[self.next_index][0]:
            _, speaker, text = self.script[self.next_index]
            self.active_speaker = speaker
            self.active_text = text
            self.active_timer = max(2.5, len(text) * 0.06)  # rough reading time
            self.next_index += 1

        if self.active_text and self.active_timer > 0:
            self.active_timer -= dt
            if self.active_timer <= 0:
                self.active_text = None

    def draw(self, screen):
        if not self.active_text:
            return

        if self.active_speaker == PLAYER:
            self._draw_bubble(
                screen, self.active_text, self.player_font,
                self.PLAYER_BG, self.PLAYER_BORDER, self.PLAYER_TEXT,
                border_radius=16, tail=True,
            )
        else:
            self._draw_bubble(
                screen, self.active_text, self.ai_font,
                self.AI_BG, self.AI_BORDER, self.AI_TEXT,
                border_radius=0, tail=False,
            )

    def _wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def _draw_bubble(self, screen, text, font, bg_color, border_color, text_color, border_radius, tail):
        lines = self._wrap_text(text, font, self.MAX_WIDTH - self.PADDING * 2)
        text_surfaces = [font.render(line, True, text_color) for line in lines]

        width = max(s.get_width() for s in text_surfaces) + self.PADDING * 2
        height = len(text_surfaces) * self.LINE_HEIGHT + self.PADDING * 2

        rect = pygame.Rect(0, 0, width, height)
        rect.centerx = self.screen_width / 2
        rect.top = 30

        pygame.draw.rect(screen, bg_color, rect, border_radius=border_radius)
        pygame.draw.rect(screen, border_color, rect, width=2, border_radius=border_radius)

        for i, surface in enumerate(text_surfaces):
            text_rect = surface.get_rect(centerx=rect.centerx, top=rect.top + self.PADDING + i * self.LINE_HEIGHT)
            screen.blit(surface, text_rect)

        if tail:
            cx = rect.centerx
            y = rect.bottom + 6
            for radius in (6, 4, 2):
                pygame.draw.circle(screen, bg_color, (cx, y), radius)
                pygame.draw.circle(screen, border_color, (cx, y), radius, 1)
                y += radius * 2 + 4
