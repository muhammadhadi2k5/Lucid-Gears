extends BaseButton
## A 3D keycap-style button: the face sinks down into a wall when pressed.
## Ported from the pygame version's design - a chamfered single-diagonal
## bottom edge (not two mirrored notches, which are geometrically forced
## to lean opposite ways - see chat history). Extends BaseButton so
## hover/press state comes from Godot's own input handling via
## get_draw_mode() instead of us tracking mouse position manually.

@export var label_text: String = "BUTTON":
	set(value):
		label_text = value
		queue_redraw()

const DEPTH := 10.0
const CHAMFER := 8.0

const BASE_COLOR := Color(1.0, 0.353, 0.157)
const HOVER_COLOR := Color(0.290, 0.102, 0.510)
const PRESSED_COLOR := Color(0.180, 0.063, 0.322)
const WALL_COLOR := Color(0.059, 0.059, 0.059)

const BASE_TEXT_COLOR := Color(0, 0, 0)
const HOVER_TEXT_COLOR := Color(1, 1, 1)

func _ready() -> void:
	if custom_minimum_size == Vector2.ZERO:
		custom_minimum_size = Vector2(220, 60)

func _process(_delta: float) -> void:
	queue_redraw()

func _draw() -> void:
	var s: Vector2 = size
	draw_rect(Rect2(0, DEPTH, s.x, s.y), WALL_COLOR)

	var draw_mode := get_draw_mode()
	var is_pressed_visual: bool = draw_mode == DRAW_PRESSED or draw_mode == DRAW_HOVER_PRESSED

	var face_color: Color
	var text_color: Color
	if is_pressed_visual:
		face_color = PRESSED_COLOR
		text_color = HOVER_TEXT_COLOR
	elif draw_mode == DRAW_HOVER:
		face_color = HOVER_COLOR
		text_color = HOVER_TEXT_COLOR
	else:
		face_color = BASE_COLOR
		text_color = BASE_TEXT_COLOR

	var offset: float = DEPTH if is_pressed_visual else 0.0
	var left := 0.0
	var top := offset
	var right := s.x
	var bottom := s.y + offset
	var chamfer: float = min(CHAMFER, (bottom - top) / 2.0, (right - left) / 2.0)

	var face_polygon := PackedVector2Array([
		Vector2(left, bottom - chamfer),
		Vector2(left, top),
		Vector2(right, top),
		Vector2(right - chamfer, bottom),
	])
	draw_colored_polygon(face_polygon, face_color)

	if not is_pressed_visual:
		var light_edge: Color = face_color.lightened(0.3)
		var dark_edge: Color = face_color.darkened(0.3)
		var glow: Color = face_color
		glow.a = 0.35

		# soft glow pass first (wide, translucent), crisp edge drawn on top
		draw_line(Vector2(left, bottom - chamfer), Vector2(left, top), glow, 8.0, true)
		draw_line(Vector2(left, top), Vector2(right, top), glow, 8.0, true)
		draw_line(Vector2(right, top), Vector2(right - chamfer, bottom), glow, 8.0, true)

		draw_line(Vector2(left, bottom - chamfer), Vector2(left, top), light_edge, 3.0, true)
		draw_line(Vector2(left, top), Vector2(right, top), light_edge, 3.0, true)
		draw_line(Vector2(right, top), Vector2(right - chamfer, bottom), dark_edge, 3.0, true)

	var font: Font = get_theme_default_font()
	var font_size: int = get_theme_default_font_size()
	if font:
		var baseline_y: float = s.y / 2.0 + offset + font_size * 0.35
		draw_string(font, Vector2(0, baseline_y), label_text, HORIZONTAL_ALIGNMENT_CENTER, s.x, font_size, text_color)
