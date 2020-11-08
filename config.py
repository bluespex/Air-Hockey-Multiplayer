import pygame


screen_width = 720
screen_height = 400

light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')

goal1 = pygame.Rect(30, screen_height/2 - 120, 5, 240)
goal2 = pygame.Rect(screen_width - 30, screen_height/2 - 120, 5, 240)

goal_top = screen_height/2 - 120
goal_bottom = screen_height/2 + 120
