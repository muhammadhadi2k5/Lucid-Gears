extends Node2D
## Circular health display: a segmented ring (one segment per hit the car
## can take) around a placeholder speedometer face. `car` must be
## assigned externally before this draws meaningfully (see race.gd).

const RADIUS := 45.0
const RING_WIDTH := 10.0
const GAP_DEGREES := 6.0
const ARC_POINTS := 24 ## smoothness of each segment's curve

const FACE_COLOR := Color(0.078, 0.078, 0.118)
const FACE_EDGE_COLOR := Color(0.235, 0.235, 0.275)
const EMPTY_SEGMENT_COLOR := Color(0.216, 0.216, 0.243)
const FULL_COLOR := Color(1.0, 0.353, 0.157)
const LOW_COLOR := Color(0.863, 0.118, 0.118)

var car: Area2D
var segments: int = 5 ## kept independent of PlayerCar internals - just how many chunks to draw

func _process(_delta: float) -> void:
	queue_redraw()

func _draw() -> void:
	draw_circle(Vector2.ZERO, RADIUS - RING_WIDTH, FACE_COLOR)
	draw_arc(Vector2.ZERO, RADIUS - RING_WIDTH, 0.0, TAU, 32, FACE_EDGE_COLOR, 2.0, true)

	if car == null:
		return

	var fraction: float = float(car.health) / float(car.MAX_HEALTH)
	var fill_color: Color = FULL_COLOR.lerp(LOW_COLOR, 1.0 - fraction)
	var segment_health: float = float(car.MAX_HEALTH) / segments

	var gap: float = deg_to_rad(GAP_DEGREES)
	var segment_angle: float = (TAU / segments) - gap
	var arc_radius: float = RADIUS - RING_WIDTH / 2.0

	for i in range(segments):
		var start: float = -PI / 2.0 + i * (TAU / segments) + gap / 2.0
		var end: float = start + segment_angle
		var filled: bool = car.health > i * segment_health
		var color: Color = fill_color if filled else EMPTY_SEGMENT_COLOR
		draw_arc(Vector2.ZERO, arc_radius, start, end, ARC_POINTS, color, RING_WIDTH, true)
