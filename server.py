import socket
import threading
import sys
import pickle
import pygame
import random
from config import *

player_score = 0
opponent_score = 0


class Ball:
    global player_score, opponent_score

    def __init__(self):
        self.body = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 15, 15)
        self.ball_speed_x = 2 * random.choice((1, -1))
        self.ball_speed_y = 2 * random.choice((1, -1))


    def ball_animation(self):
        global score_time , player_score , opponent_score
        self.body.x += self.ball_speed_x
        self.body.y += self.ball_speed_y

        if self.body.top <= 0 or self.body.bottom >= screen_height:
            self.ball_speed_y *= -1

        # Player Score
        if self.body.left <= 0.2:
            self.ball_speed_x *= -1
            if self.body.bottom <= goal_top or self.body.top >= goal_bottom:
                # self.ball_speed_x *= -1
                pass
            else:
                # pygame.mixer.Sound.play(score_sound)
                self.body.center = (screen_width/2, screen_height/2)
                print("player_score")
                player_score += 1
                # self.body.center = (screen_width/2, screen_height/2)
                return

        # Opponent Score
        if self.body.right >= screen_width-0.2:
            self.ball_speed_x *= -1

            if self.body.bottom <= goal_top or self.body.top >= goal_bottom:
                # pygame.mixer.Sound.play(plob_sound)
                # self.ball_speed_x *= -1
                pass
            else:
                # pygame.mixer.Sound.play(score_sound)
                self.body.center = (screen_width/2, screen_height/2)
                print("opponent_score")
                opponent_score += 1
                # self.body.center = (screen_width/2, screen_height/2)
                return


    def coll(self,player):
        if self.body.colliderect(player):
            # pygame.mixer.Sound.play(plob_sound)
            if abs(self.body.right - player.left) < 10 or abs(self.body.left - player.right) < 10:
                self.ball_speed_x *= -1
                ball_mid = (self.body.top+self.body.bottom)/2
                player_mid = (player.top+player.bottom)/2
                gradient = 2*abs(player_mid-ball_mid)
                gradient /= player_mid
                self.ball_speed_y = gradient*2
                self.ball_speed_y += 0.5
                # self.ball_speed_y *= -1

            elif abs(self.body.bottom - player.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            elif abs(self.body.top - player.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1



class Server():
    def __init__(self, host="localhost", port=4000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((str(host), int(port)))
        self.sock.listen(10)
        self.sock.setblocking(False)

        self.clients = []
        self.stateClients = []
        self.ball = Ball()
        print(self.ball.body)

        accept = threading.Thread(target=self.aceptarCon)
        process = threading.Thread(target=self.processarCon)

        accept.daemon = True
        accept.start()

        process.daemon = True
        process.start()


        while True:
            msg = input('')
            if msg == 'salir':
                self.sock.close()   
                sys.exit()
            else:
                pass

    def aceptarCon(self):
        print("accepting connections started")
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(False)
                self.clients.append({
                    'client': conn,
                    'data': {}
                })
                print("A player logged in: ", addr)
            except:
                pass

    def processarCon(self):
        print("processing connections started")
        while True:
            if len(self.clients) > 0:
                for c in self.clients:
                    try:
                        data = c['client'].recv(1024)
                        if data:
                            received = pickle.loads(data)
                            c['data'] = received
                            self.ball.ball_animation()
                            self.ball.coll(c['data']['player_body'])
                            status = self.setNewState(received, c['client'])
                            c['data'] = status
                            self.responseToPlayers(c['client'])
                    except: 
                        pass

    def setNewState(self, state, client):
        global player_score,opponent_score
        state['score'] = [player_score , opponent_score]
        for cl in self.clients:
            if(cl['client'] != client):
                state['opponent'] = cl['data']['player_body']

        state['ball'] = self.ball.body
        # print(state['score'])

        return state

    def responseToPlayers(self, client):
         for sclient in self.clients:
            try:
                sclient['client'].send(pickle.dumps(sclient['data']))
            except:
                self.clients.remove(sclient)


Server()