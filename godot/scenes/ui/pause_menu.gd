extends Control

signal continue_pressed
signal restart_pressed
signal main_menu_pressed

@onready var continue_button: Button = $CenterContainer/VBoxContainer/ContinueButton
@onready var restart_button: Button = $CenterContainer/VBoxContainer/RestartButton
@onready var main_menu_button: Button = $CenterContainer/VBoxContainer/MainMenuButton

func _ready() -> void:
	continue_button.pressed.connect(func(): continue_pressed.emit())
	restart_button.pressed.connect(func(): restart_pressed.emit())
	main_menu_button.pressed.connect(func(): main_menu_pressed.emit())
