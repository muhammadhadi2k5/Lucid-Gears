extends Node2D
## Orchestrates the race: keeps the player car clamped to the road's
## bounds every frame. Mirrors what Game._update did in the pygame
## version - Road and PlayerCar don't know about each other directly.

@onready var road = $Road
@onready var car = $PlayerCar
@onready var obstacle_spawner = $ObstacleSpawner
@onready var health_gauge = $HUD/HealthGauge

func _ready() -> void:
	# lower process_priority runs earlier, globally across the whole tree -
	# without this, Race (the parent) processes before PlayerCar (its
	# child) by default, so clamping would run BEFORE that frame's
	# movement instead of after it, letting the car poke past the edge
	# every frame while a key is held.
	process_priority = 1
	var viewport_size := get_viewport_rect().size
	car.position = Vector2(viewport_size.x / 2.0, viewport_size.y - car.HEIGHT / 2.0 - 20.0)
	obstacle_spawner.road = road
	health_gauge.car = car
	health_gauge.position = Vector2(80, viewport_size.y - 80)

func _process(_delta: float) -> void:
	var edges: Vector2 = road.edges_at_y(car.position.y + car.HEIGHT / 2.0)
	car.clamp_x(edges.x, edges.y)
