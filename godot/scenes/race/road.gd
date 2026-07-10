extends Node2D
## Scrolling pseudo-3D road, Out Run style - direct port of the pygame
## Road class's perspective math. "depth" is 0.0 at the horizon, 1.0 at
## the bottom of the screen; width/x/y at a given depth are all eased
## with depth^2 so things appear to accelerate toward the viewer.

var screen_width: float
var screen_height: float

const TOP_WIDTH := 60.0
const BOTTOM_WIDTH := 1100.0
const RUNG_COUNT := 12
const SCROLL_SPEED := 0.6 ## full road-length cycles per second

const ROAD_COLOR := Color(0.08, 0.08, 0.12)
const EDGE_COLOR := Color(1.0, 0.353, 0.157) ## same orange used everywhere else

var center_x: float
var horizon_y: float
var scroll: float = 0.0

func _ready() -> void:
	var viewport_size := get_viewport_rect().size
	screen_width = viewport_size.x
	screen_height = viewport_size.y
	center_x = screen_width / 2.0
	horizon_y = screen_height * 0.4

func _process(delta: float) -> void:
	scroll = fmod(scroll + SCROLL_SPEED * delta, 1.0)
	queue_redraw()

func width_at(depth: float) -> float:
	var eased := depth * depth
	return TOP_WIDTH + (BOTTOM_WIDTH - TOP_WIDTH) * eased

func y_at(depth: float) -> float:
	var eased := depth * depth
	return horizon_y + (screen_height - horizon_y) * eased

func x_at(depth: float, offset: float) -> float:
	## screen x at a given depth and lateral offset (-1 left edge .. 1 right edge)
	return center_x + offset * width_at(depth) / 2.0

func _depth_at_y(y: float) -> float:
	var fraction := (y - horizon_y) / (screen_height - horizon_y)
	return sqrt(fraction)

func edges_at_y(y: float) -> Vector2:
	## left/right x of the road at a given screen y, for keeping the car on it
	var width := width_at(_depth_at_y(y))
	return Vector2(center_x - width / 2.0, center_x + width / 2.0)

func _draw() -> void:
	draw_line(Vector2(0, horizon_y), Vector2(screen_width, horizon_y), EDGE_COLOR, 2.0)
	_draw_surface()
	_draw_rungs()

func _draw_surface() -> void:
	var top_w := width_at(0.0)
	var bottom_w := width_at(1.0)
	var points := PackedVector2Array([
		Vector2(center_x - top_w / 2.0, horizon_y),
		Vector2(center_x + top_w / 2.0, horizon_y),
		Vector2(center_x + bottom_w / 2.0, screen_height),
		Vector2(center_x - bottom_w / 2.0, screen_height),
	])
	draw_colored_polygon(points, ROAD_COLOR)
	draw_polyline(points + PackedVector2Array([points[0]]), EDGE_COLOR, 2.0)

func _draw_rungs() -> void:
	var depth_step := 1.0 / RUNG_COUNT
	for i in range(RUNG_COUNT):
		var depth := fmod(i * depth_step + scroll, 1.0)
		var y := y_at(depth)
		var width := width_at(depth)
		var left := center_x - width / 2.0
		var right := center_x + width / 2.0
		draw_line(Vector2(left, y), Vector2(right, y), EDGE_COLOR, 2.0)
