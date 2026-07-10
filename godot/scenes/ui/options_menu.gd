extends Control

@onready var fullscreen_toggle: CheckButton = $CenterContainer/VBoxContainer/FullscreenToggle
@onready var back_button: Button = $CenterContainer/VBoxContainer/BackButton

func _ready() -> void:
	fullscreen_toggle.button_pressed = get_window().mode == Window.MODE_FULLSCREEN
	fullscreen_toggle.toggled.connect(_on_fullscreen_toggled)
	back_button.pressed.connect(_on_back_pressed)

func _on_fullscreen_toggled(toggled_on: bool) -> void:
	if toggled_on:
		get_window().mode = Window.MODE_FULLSCREEN
	else:
		get_window().mode = Window.MODE_WINDOWED

func _on_back_pressed() -> void:
	GameManager.go_to_scene("res://scenes/ui/main_menu.tscn")
