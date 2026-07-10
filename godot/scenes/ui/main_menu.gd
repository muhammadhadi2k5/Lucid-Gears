extends Control

@onready var play_button: Button = $CenterContainer/VBoxContainer/PlayButton
@onready var options_button: Button = $CenterContainer/VBoxContainer/OptionsButton

func _ready() -> void:
	play_button.pressed.connect(_on_play_pressed)
	options_button.pressed.connect(_on_options_pressed)

func _on_play_pressed() -> void:
	GameManager.go_to_scene("res://scenes/race/race.tscn")

func _on_options_pressed() -> void:
	GameManager.go_to_scene("res://scenes/ui/options_menu.tscn")
