extends Control

signal restart_pressed
signal main_menu_pressed

@onready var restart_button: BaseButton = $CenterContainer/VBoxContainer/ButtonRow/RestartButton
@onready var main_menu_button: BaseButton = $CenterContainer/VBoxContainer/ButtonRow/MainMenuButton

func _ready() -> void:
	restart_button.pressed.connect(func(): restart_pressed.emit())
	main_menu_button.pressed.connect(func(): main_menu_pressed.emit())
