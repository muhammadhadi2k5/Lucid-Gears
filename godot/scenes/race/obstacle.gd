extends Area2D
## A single hazard - visually AI infrastructure (barricade/drone/conduit).
## Position lives in road space (depth 0.0 at the horizon, 1.0 at the
## bottom; offset -1.0 left edge .. 1.0 right edge), same idea as the
## pygame Obstacle class. `road` must be assigned right after instancing,
## before this node enters the tree (see obstacle_spawner.gd).

const SIZE_FRACTION := 0.18 ## width as a fraction of the road's width at this depth
const HEIGHT_RATIO := 0.6
const COLOR := Color(0.235, 0.863, 1.0) ## cold cyan - reads as "AI", contrasts with the car's orange

var road: Node2D
var offset: float = 0.0
var depth: float = 0.0
var speed: float = 0.0 ## extra depth/sec on top of the road's own scroll

@onready var collision_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	collision_shape.shape = RectangleShape2D.new()
	add_to_group("obstacles")

func _process(delta: float) -> void:
	depth += (road.SCROLL_SPEED + speed) * delta
	_update_transform()
	queue_redraw()

func is_off_screen() -> bool:
	return depth > 1.0

func _update_transform() -> void:
	var width: float = road.width_at(depth) * SIZE_FRACTION
	var height: float = width * HEIGHT_RATIO
	position = Vector2(road.x_at(depth, offset), road.y_at(depth) - height / 2.0)
	collision_shape.shape.size = Vector2(width, height)

func _draw() -> void:
	var width: float = road.width_at(depth) * SIZE_FRACTION
	var height: float = width * HEIGHT_RATIO
	draw_rect(Rect2(-width / 2.0, -height / 2.0, width, height), COLOR)
