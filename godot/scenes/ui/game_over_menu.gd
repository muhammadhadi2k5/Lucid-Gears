extends Control

signal restart_pressed
signal main_menu_pressed

@onready var restart_button: Button = $CenterContainer/VBoxContainer/RestartButton
@onready var main_menu_button: Button = $CenterContainer/VBoxContainer/MainMenuButton

func _ready() -> void:
	restart_button.pressed.connect(func(): restart_pressed.emit())
	main_menu_button.pressed.connect(func(): main_menu_pressed.emit())
