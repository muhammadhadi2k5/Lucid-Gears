extends Node
## Global game state and scene-switching, accessible from anywhere without
## manual references between scenes. Grows as each build phase needs it -
## deliberately empty beyond the basics for now.

var current_level: int = 1
var player_health: int = 100

func go_to_scene(path: String) -> void:
	get_tree().change_scene_to_file(path)
