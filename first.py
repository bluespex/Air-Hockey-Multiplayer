import pygame
import sys
import random
import time
from client import Client
from config import *


# class obstlacles:
#     def __init__(self):
#         self.arr = []

#     def add(self, n):
#         self.arr.clear()
#         while n:
#             x = [random.choice(range(10, screen_width - 10)),
#                  random.choice(range(screen_height)), random.choice((+1, -1))]
#             self.arr.append(x)
#             n -= 1


# def obs_collide():
#     global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
#     sz = len(obs)
#     # mn = obs[0][0]*screen_width + obb.arr[0][1]
#     # mx = obb.arr[sz-1][0]*screen_width + obb.arr[sz-1][1]
#     l = 0
#     e = sz-1
#     print(obs)
#     while(l <= e):
#         mid = int((l+e)/2)

#         cur = ball.x*screen_width + ball.y
#         x = obs[mid].x*screen_width + obs[mid].y
#         if(x > cur):
#             if ball.colliderect(obs[mid]):
#                 if(ball_speed_x > 0):
#                     opponent_score += 1
#                 else:
#                     player_score += 1
#             break
#             l = mid+1
#         elif(x < cur):
#             if ball.colliderect(obs[mid]):
#                 if(ball_speed_x > 0):
#                     opponent_score += 1
#                 else:
#                     player_score += 1
#             break
#             e = mid-1
#         else:
#             if(ball_speed_x > 0):
#                 opponent_score += 1
#             else:
#                 player_score += 1
#             break


# def object_collide():
#     global ball_speed_x, player_score, opponent_score
#     for i in range(len(obs)-1):
#         if ball.colliderect(obs[i]):
#             if obb.arr[i][2] >= 1:
#                 if ball_speed_x < 0:
#                     player_score += 1
#                 else:
#                     opponent_score += 1
#             else:
#                 if ball_speed_x < 0:
#                     player_score -= 1
#                 else:
#                     opponent_score -= 1
#             obs.pop(i)
#             obb.arr.pop(i)


# def ball_animation():
#     global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

#     ball.x += ball_speed_x
#     ball.y += ball_speed_y

#     if ball.top <= 0 or ball.bottom >= screen_height:
#         pygame.mixer.Sound.play(plob_sound)
#         ball_speed_y *= -1

#     # Player Score
#     if ball.left <= 0:
#         if ball.bottom <= goal_top or ball.top >= goal_bottom:
#             pygame.mixer.Sound.play(plob_sound)
#             ball_speed_x *= -1
#         else:
#             pygame.mixer.Sound.play(score_sound)
#             score_time = pygame.time.get_ticks()
#             player_score += 1

#     # Opponent Score
#     if ball.right >= screen_width:
#         if ball.bottom <= goal_top or ball.top >= goal_bottom:
#             pygame.mixer.Sound.play(plob_sound)
#             ball_speed_x *= -1
#         else:
#             pygame.mixer.Sound.play(score_sound)
#             score_time = pygame.time.get_ticks()
#             opponent_score += 1

#     if ball.colliderect(player) and ball_speed_x > 0:
#         pygame.mixer.Sound.play(plob_sound)
#         if abs(ball.right - player.left) < 10:
#             ball_speed_x *= -1
#             ball_mid = (ball.top+ball.bottom)/2
#             player_mid = (player.top+player.bottom)/2
#             gradient = 2*abs(player_mid-ball_mid)
#             gradient /= player_mid
#             ball_speed_y = gradient*10
#             ball_speed_y += 0.5
#         elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
#             ball_speed_y *= -1
#         elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
#             ball_speed_y *= -1

#     if ball.colliderect(opponent) and ball_speed_x < 0:
#         pygame.mixer.Sound.play(plob_sound)
#         if abs(ball.left - opponent.right) < 10:
#             ball_speed_x *= -1
#             ball_mid = (ball.top+ball.bottom)/2
#             opponent_mid = (opponent.top+opponent.bottom)/2
#             gradient = 2*abs(opponent_mid-ball_mid)
#             gradient /= opponent_mid
#             ball_speed_y = gradient*10
#             ball_speed_y += 0.5
#         elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
#             ball_speed_y *= -1
#         elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
#             ball_speed_y *= -1


class Player:
    def __init__(self,isleft):

        if(isleft):
            self.body = pygame.Rect(screen_width - 50, screen_height / 2 - 40, 10, 80)
        else:
            self.body = pygame.Rect(40, screen_height / 2 - 40, 10, 80)

        self.client = Client()
        self.client.state['player_body'] = self.body
        self.speed = 0

    def speedify(self,val):
        self.speed += val

    def player_animation(self):
        self.body.y += self.speed

        if self.body.top <= goal_top:
            self.body.top = goal_top
        if self.body.bottom >= goal_bottom:
            self.body.bottom = goal_bottom
        
        self.client.state['player_body'] = self.body

    def render(self):
        # self.client.recvData()
        
        if 'opponent' in self.client.state:
            pygame.draw.rect(screen, (223, 87, 14), self.client.state['opponent'])

        if 'ball' in self.client.state:
            pygame.draw.ellipse(screen, light_grey, self.client.state['ball'])
            if(self.client.state['ball'].colliderect(self.body)):
                pygame.mixer.Sound.play(plob_sound)


        self.client.sendStatus()
        pygame.draw.rect(screen, (223, 87, 14), self.body)
        


# def ball_start():
#     global ball_speed_x, ball_speed_y, ball_moving, score_time

#     ball.center = (screen_width/2, screen_height/2)
#     current_time = pygame.time.get_ticks()

#     if current_time - score_time < 700:
#         number_three = basic_font.render("3", False, light_grey)
#         screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
#     if 700 < current_time - score_time < 1400:
#         number_two = basic_font.render("2", False, light_grey)
#         screen.blit(number_two, (screen_width/2 - 10, screen_height/2 + 20))
#     if 1400 < current_time - score_time < 2100:
#         number_one = basic_font.render("1", False, light_grey)
#         screen.blit(number_one, (screen_width/2 - 10, screen_height/2 + 20))

#     if current_time - score_time < 2100:
#         ball_speed_y, ball_speed_x = 0, 0
#     else:
#         ball_speed_x = 5 * random.choice((1, -1))
#         ball_speed_y = 5 * random.choice((1, -1))
#         score_time = None


# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colors
# light_grey = (200, 200, 200)
# bg_color = pygame.Color('grey12')

# Game Rectangles
# ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 20, 20)
# player = pygame.Rect(screen_width - 50, screen_height / 2 - 40, 10, 80)
# opponent = pygame.Rect(40, screen_height / 2 - 40, 10, 80)
# goal1 = pygame.Rect(30, screen_height/2 - 120, 5, 240)
# goal2 = pygame.Rect(screen_width - 30, screen_height/2 - 120, 5, 240)

# obs = []

# Game Variables
ball_speed_x = 2 * random.choice((1, -1))
ball_speed_y = 2 * random.choice((1, -1))
# player_speed = 0
# opponent_speed = 7
ball_moving = False
score_time = True
# goal_top = screen_height/2 - 120
# goal_bottom = screen_height/2 + 120
# obb = obstlacles()
# obb.add(10)

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)

# sound
plob_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")


def run_game(server):
    
    # prev_time = time.perf_counter()

    player = Player(False)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # player_speed -= 2
                    player.speedify(-2)
                if event.key == pygame.K_DOWN:
                    # player_speed += 2
                    player.speedify(2)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    # player_speed += 2
                    player.speedify(2)
                if event.key == pygame.K_DOWN:
                    # player_speed -= 2
                    player.speedify(-2)

        # new_time = time.perf_counter()
        # if new_time - prev_time > 5.0:
        #     prev_time = new_time
        #     obb.arr.clear()
        #     obb.add(5)
        #     obs.clear()
        #     for ele in obb.arr:
        #         x = pygame.Rect(ele[0], ele[1], 30, 30)
        #         obs.append(x)

        # Game Logic
        player.player_animation()
        # ball_animation()
        # player_animation()
        # opponent_ai()
        # object_collide()

        # Visuals
        screen.fill((37, 156, 135))
        # for i in range(len(obs)-1):
        #     if obb.arr[i][2] == 1:
        #         pygame.draw.rect(screen, (228, 227, 227), obs[i])
        #     else:
        #         pygame.draw.rect(screen, (132, 169, 172), obs[i])

        pygame.draw.rect(screen, light_grey, goal2)
        pygame.draw.rect(screen, light_grey, goal1)
        # pygame.draw.rect(screen, (223, 87, 14), player)
        # pygame.draw.rect(screen, (236, 230, 97), opponent)
        player.render()
        # pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        # if score_time:
        #     ball_start()

        player_text = basic_font.render(f'{player_score}', False, light_grey)
        screen.blit(player_text, (screen_width/2 + 15, 0))

        opponent_text = basic_font.render(f'{opponent_score}', False, light_grey)
        screen.blit(opponent_text, (screen_width/2 - 30, 0))

        pygame.display.flip()
        clock.tick(120)


def main():
    run_game('localhost')


if __name__ == '__main__':
    main()
