extends Node2D
## Decides when new obstacles appear and keeps the active list current.
## `road` must be assigned externally before obstacles start spawning
## (see race.gd).

const OBSTACLE_SCENE := preload("res://scenes/race/obstacle.tscn")

const MIN_INTERVAL := 1.0 ## shortest gap between spawns, in seconds
const MAX_INTERVAL := 3.0 ## longest gap between spawns, in seconds

const OFFSET_RANGE := 0.8 ## spawn within the middle 80% of the road width

const STATIC_CHANCE := 0.6 ## fraction of spawns that are static rather than oncoming
const ONCOMING_SPEED_MIN := 0.05
const ONCOMING_SPEED_MAX := 0.15

var road: Node2D
var time_until_next_spawn: float = 0.0

func _ready() -> void:
	time_until_next_spawn = randf_range(MIN_INTERVAL, MAX_INTERVAL)

func _process(delta: float) -> void:
	time_until_next_spawn -= delta
	if time_until_next_spawn <= 0.0:
		_spawn()
		time_until_next_spawn = randf_range(MIN_INTERVAL, MAX_INTERVAL)

	for obstacle in get_children():
		if obstacle.is_off_screen():
			obstacle.queue_free()

func _spawn() -> void:
	var obstacle = OBSTACLE_SCENE.instantiate()
	obstacle.road = road
	obstacle.offset = randf_range(-OFFSET_RANGE, OFFSET_RANGE)
	if randf() < STATIC_CHANCE:
		obstacle.speed = 0.0
	else:
		obstacle.speed = randf_range(ONCOMING_SPEED_MIN, ONCOMING_SPEED_MAX)
	add_child(obstacle)
