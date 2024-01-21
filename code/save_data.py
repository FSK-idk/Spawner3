class SaveData:
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60

        self.is_show_begin_cutscene = True
        self.is_show_end_cutscene = False

        self.current_level = "cats"
        self.player_position = (500, 450)

        self.wood_amount = 0
        self.stone_amount = 0

        self.tree_level = 0
        self.rock_level = 0
        self.cats_level = 0


save_data = SaveData()
