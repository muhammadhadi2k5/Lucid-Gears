extends Node2D
## Orchestrates the race: keeps the player car clamped to the road's
## bounds every frame, and handles pause/game-over. Road and PlayerCar
## don't know about each other, or about pausing - Race is the only
## thing that needs to.
##
## Race itself runs at process_mode ALWAYS so it keeps listening for the
## pause toggle while the tree is paused. That would normally cascade
## ALWAYS down to every child - Road, PlayerCar, and ObstacleSpawner are
## each explicitly set back to PAUSABLE (in their own scenes) specifically
## to opt back out of that and freeze correctly during pause.

@onready var road = $Road
@onready var car = $PlayerCar
@onready var obstacle_spawner = $ObstacleSpawner
@onready var health_gauge = $HUD/HealthGauge
@onready var pause_menu = $PauseLayer/PauseMenu
@onready var game_over_menu = $GameOverLayer/GameOverMenu

var is_game_over: bool = false

func _ready() -> void:
	process_priority = 1
	process_mode = Node.PROCESS_MODE_ALWAYS

	var viewport_size := get_viewport_rect().size
	car.position = Vector2(viewport_size.x / 2.0, viewport_size.y - car.HEIGHT / 2.0 - 20.0)
	obstacle_spawner.road = road
	health_gauge.car = car
	health_gauge.position = Vector2(80, viewport_size.y - 80)

	pause_menu.continue_pressed.connect(_on_continue_pressed)
	pause_menu.restart_pressed.connect(_on_restart_pressed)
	pause_menu.main_menu_pressed.connect(_on_main_menu_pressed)

	game_over_menu.restart_pressed.connect(_on_restart_pressed)
	game_over_menu.main_menu_pressed.connect(_on_main_menu_pressed)

func _process(_delta: float) -> void:
	if Input.is_action_just_pressed("ui_cancel") and not is_game_over:
		_toggle_pause()

	if get_tree().paused or is_game_over:
		return

	var edges: Vector2 = road.edges_at_y(car.position.y + car.HEIGHT / 2.0)
	car.clamp_x(edges.x, edges.y)

	if car.health <= 0:
		_trigger_game_over()

func _toggle_pause() -> void:
	get_tree().paused = not get_tree().paused
	pause_menu.visible = get_tree().paused

func _trigger_game_over() -> void:
	is_game_over = true
	get_tree().paused = true
	game_over_menu.visible = true

func _on_continue_pressed() -> void:
	get_tree().paused = false
	pause_menu.visible = false

func _on_restart_pressed() -> void:
	get_tree().paused = false
	get_tree().reload_current_scene()

func _on_main_menu_pressed() -> void:
	get_tree().paused = false
	GameManager.go_to_scene("res://scenes/ui/main_menu.tscn")
