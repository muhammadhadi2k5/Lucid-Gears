extends Control
## Bevelled window frame for the pause menu, ported from the pygame
## version's PauseMenu - solid layered rects rather than drawn border
## lines, since thick lines don't join cleanly at 90-degree corners in
## either engine. Buttons/content live as separate child Controls layered
## on top (see pause_menu.tscn); this script only draws the frame itself.

const BORDER_THICKNESS := 3.0
const TITLE_BAR_HEIGHT := 44.0

const BORDER_LIGHT := Color(1.0, 0.745, 0.588)
const BORDER_DARK := Color(0.235, 0.098, 0.039)
const BODY_COLOR := Color(0.078, 0.078, 0.118)
const TITLE_BAR_COLOR := Color(1.0, 0.353, 0.157)
const TITLE_TEXT_COLOR := Color(0, 0, 0)

func _draw() -> void:
	var s: Vector2 = size
	var t := BORDER_THICKNESS

	draw_rect(Rect2(Vector2.ZERO, s), BORDER_DARK)
	draw_rect(Rect2(Vector2.ZERO, Vector2(s.x - t, s.y - t)), BORDER_LIGHT)

	var interior := Rect2(Vector2(t, t), Vector2(s.x - t * 2.0, s.y - t * 2.0))
	draw_rect(interior, BODY_COLOR)

	var title_bar := Rect2(interior.position, Vector2(interior.size.x, TITLE_BAR_HEIGHT))
	draw_rect(title_bar, TITLE_BAR_COLOR)
	draw_line(
		title_bar.position + Vector2(0, TITLE_BAR_HEIGHT),
		title_bar.position + Vector2(title_bar.size.x, TITLE_BAR_HEIGHT),
		BORDER_DARK, 2.0, true,
	)

	var font: Font = get_theme_default_font()
	var font_size: int = get_theme_default_font_size()
	if font:
		var baseline_y: float = title_bar.position.y + TITLE_BAR_HEIGHT / 2.0 + font_size * 0.35
		draw_string(font, Vector2(title_bar.position.x + 12, baseline_y), "PAUSED", HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, TITLE_TEXT_COLOR)
