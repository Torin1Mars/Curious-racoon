vertical_tile_number:int = 11
tile_size:int = 64

# 704 x 1200
screen_height:int = vertical_tile_number*tile_size
screen_width:int = 1200
fps:int = 60

default_gravity:float = 0.9
default_jump_height:float = -18

player_speed:float = 5

game_mode: dict = {'easy': 3,
                    'normal': 5,
                    'hard': 7}
