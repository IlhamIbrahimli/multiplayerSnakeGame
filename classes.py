import random
import socket
import pygame
from settings import *
import sys
import select
import threading
import time
data= []
sock1 = ""
class thread1(threading.Thread):
    def run(self):
        global sock1
        global data
        while True:
            ready = select.select([sock1], [], [], )
            if ready[0]:
                data = sock1.recv(4096)
class Game:

    def __init__(self, sock, name):
        global sock1
        self.direction = [0, 0]
        sock1 = sock
        
        self.name = name
        self.width = WIDTH
        self.height = HEIGHT
        self.fps = FPS
        self.score = 0
        self.applePos = [0, 0]
        self.collRect = []
        self.appleRect = 0
        self.appleSpawned = False
        self.bodyParts = [[320, 320]]
        self.bodyRect = [pygame.Rect(self.bodyParts[0][0], self.bodyParts[0][1], 90, 90)]
        self.headrot = ""
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("Song.mp3")
        pygame.mixer.music.play()
        self.font = pygame.font.SysFont("arial", 36)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load('back.png')
        self.head = pygame.image.load("snek.png")
        self.bod = pygame.image.load("snekback.png")
        self.apple = pygame.image.load("apple.png")
        self.thread = thread1()
        self.thread.start()

    def update(self):

        self.bodyParts.insert(0, [self.bodyParts[0][0] + self.direction[0] * 16,
                                  self.bodyParts[0][1] + self.direction[1] * 16])
        del self.bodyParts[-1]
        self.bodyRect.insert(0, pygame.Rect(self.bodyParts[0][0], self.bodyParts[0][1], 16, 16))
        del self.bodyRect[-1]
        # self.playerRect = pygame.Rect(self.bodyParts[0][0],self.bodyParts[0][1],100,100)
    def sockets(self):
        global sock1
        z = len(str(self.score))
        t = 13-z
        sock1.sendall((self.name + "0"*t + str(self.score)).encode())

    
    def draw(self):

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.headrot = pygame.transform.rotate(self.head, 0)
        if self.direction == (0,-1):
            self.headrot = pygame.transform.rotate(self.head, 0)
        elif self.direction == (0,1):
            self.headrot = pygame.transform.rotate(self.head, 180)
        for i in range(len(self.bodyParts)):
            if i == 0:
                self.screen.blit(self.headrot, (self.bodyParts[i][0], self.bodyParts[i][1]))
            else:
                self.screen.blit(self.bod, (self.bodyParts[i][0], self.bodyParts[i][1]))

        if not self.appleSpawned:
            self.spawn_apple()
        self.screen.blit(self.apple,(self.applePos[0],self.applePos[1]))
        score_text = self.font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.update()

    def event_check(self):
        # Movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.direction != (0, 1):
                        self.direction = (0, -1)

                if event.key == pygame.K_DOWN:
                    if self.direction != (0, -1):
                        self.direction = (0, 1)
                if event.key == pygame.K_LEFT:
                    if self.direction != (1, 0):
                        self.direction = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    if self.direction != (-1, 0):
                        self.direction = (1, 0)
    def draw_text(self,text, colour, y_displace=0, size=24):
        font = pygame.font.SysFont("comicsanms", size)

        text_surface = font.render(text, True, colour) 
        text_rect = text_surface.get_rect()  
        text_rect.center = (320 / 2), (320 / 2) + y_displace  

        self.screen.blit(text_surface, text_rect) 
    def die(self):
        self.screen.fill((0, 0, 0))
        img = pygame.image.load("dead.png").convert_alpha()
        self.screen.blit(img, (0, 0))
        self.draw_text("GAME OVER", (0,255,0), -130, 72)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    def collision(self):
        if self.bodyParts[0][0] >= 640 or self.bodyParts[0][0] <= 0 or self.bodyParts[0][1] >= 640 or \
                self.bodyParts[0][1] <= 0:
            self.die()
        # Check if head collides with apple
        collide = pygame.Rect.colliderect(self.bodyRect[0], self.appleRect)

        if collide:
            self.bodyParts.append(
                [self.bodyParts[-1][0] + self.direction[0] * 17, self.bodyParts[-1][1] + self.direction[1] * 17])
            self.bodyRect.append(pygame.Rect(self.bodyParts[-1][0], self.bodyParts[-1][1], 16, 16))
            self.appleSpawned = False
            self.score += 1
        #if len(self.bodyParts) > 1:
            #self.collRect = self.bodyRect
            #del self.collRect[0]

            #print(self.collRect)
            #collide2 = pygame.Rect.collidelist(self.bodyRect[0], self.collRect)
            #print(collide2)
            #if collide2 > 0:
                #self.die()

    def spawn_apple(self):
        self.applePos[0] = random.randint(1, 39) * 16
        self.applePos[1] = random.randint(1, 39) * 16
        self.appleSpawned = True
        self.appleRect = pygame.Rect(self.applePos[0], self.applePos[1], 16, 16)



    def run(self):
        while True:
            self.event_check()
            self.update()
            self.draw()
            self.collision()
            self.sockets()
            
            self.clock.tick(FPS)
