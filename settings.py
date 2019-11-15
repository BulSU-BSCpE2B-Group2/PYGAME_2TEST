import itertools

# game resolution and fps
title = "Pygame Platformer Test"
WIDTH = 800
height = 768
fps = 60
font_name = 'courier'
highscore_textfile = 'highscore.txt'

# Player properties:
player_accel = 0.5
player_friction = -0.08
player_width = 30
player_height = 40
player_gravity = 1
player_jump = 20

# list of platforms
platform_list = [((WIDTH / 2 - 50, height * 3 / 4), (100, 20)), ((125, height - 350), (100, 20)),
                 ((350, 200), (100, 20)), ((172, 100), (50, 20))]

gaps_1 = [()]


# temporary (0, height - 40, width, 40),

# color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (125, 125, 125)
yellow = (255, 255, 0)
dark_red = (125, 0, 0)
colors = itertools.cycle(['red', 'blue', 'orange', 'purple'])
