extends Area2D
## The car the player controls. position is the car's CENTER (a
## deliberate difference from the pygame version's top-left convention -
## more natural for Godot nodes). Takes damage on collision with
## obstacles via the area_entered signal - see _on_area_entered below.

const WIDTH := 50.0
const HEIGHT := 80.0
const COLOR := Color(1.0, 0.353, 0.157)
const SPEED := 500.0 ## pixels per second

const MAX_HEALTH := 100
const HIT_DAMAGE := 20
const HIT_DURATION := 1.0 ## seconds of slowdown + flash after a hit, also the invincibility window
const HIT_SPEED_MULTIPLIER := 0.4
const FLASH_INTERVAL := 0.08
const FLASH_COLORS := [Color(0.863, 0.118, 0.118), Color(0.039, 0.039, 0.039), Color(1.0, 0.863, 0.157)]

var moving_left: bool = false
var moving_right: bool = false
var health: int = MAX_HEALTH
var hit_timer: float = 0.0 ## >0 means recently hit: flashing, slowed, invincible

@onready var collision_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	collision_shape.shape = RectangleShape2D.new()
	collision_shape.shape.size = Vector2(WIDTH, HEIGHT)
	area_entered.connect(_on_area_entered)

func _process(delta: float) -> void:
	moving_left = Input.is_physical_key_pressed(KEY_LEFT) or Input.is_physical_key_pressed(KEY_A)
	moving_right = Input.is_physical_key_pressed(KEY_RIGHT) or Input.is_physical_key_pressed(KEY_D)

	var speed := SPEED
	if hit_timer > 0.0:
		hit_timer = max(0.0, hit_timer - delta)
		speed *= HIT_SPEED_MULTIPLIER

	if moving_left:
		position.x -= speed * delta
	if moving_right:
		position.x += speed * delta

	queue_redraw()

func clamp_x(left: float, right: float) -> void:
	position.x = clamp(position.x, left + WIDTH / 2.0, right - WIDTH / 2.0)

func take_hit() -> void:
	health = max(0, health - HIT_DAMAGE)
	hit_timer = HIT_DURATION

func _on_area_entered(area: Area2D) -> void:
	if hit_timer > 0.0:
		return
	if area.is_in_group("obstacles"):
		take_hit()
		area.queue_free()

func _draw() -> void:
	var color := COLOR
	if hit_timer > 0.0:
		var elapsed: float = HIT_DURATION - hit_timer
		var flash_index: int = int(elapsed / FLASH_INTERVAL) % FLASH_COLORS.size()
		color = FLASH_COLORS[flash_index]
	draw_rect(Rect2(-WIDTH / 2.0, -HEIGHT / 2.0, WIDTH, HEIGHT), color)
