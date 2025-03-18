import pygame
from pygame import locals
from math import sqrt
import random

class Bar:
    def __init__(self,bg,max):
        self.__max=max
        self.__var_max = max
        self.__bg = bg
        
    @property
    def var_max(self):
        return self.__var_max 
    
    def place(self,pos,plus_x,plus_y):
        pygame.draw.rect(self.__bg,"black",[(pos[0]-self.__max/2)-plus_x,pos[1]-plus_y,self.__max,10])
        pygame.draw.rect(self.__bg,"red",[(pos[0]-self.__max/2)-plus_x,pos[1]-plus_y,self.__var_max,10])
        
    def active(self,num):
        if self.__var_max > 0:
            self.__var_max -= num
    
    def full_change(self):
        self.__var_max = self.__max

class Ball:
    def __init__(self,screen:pygame.Surface,coords:tuple[float,float],radius = 10):
        self.__screen = screen
        self.__x,self.__y = coords
        self.__radius = radius
    
    @property
    def coords(self):
        return self.__x,self.__y
    
    @coords.setter
    def coords(self,coords):
        self.__x,self.__y = coords
    
    def move(self,tick,speed,keys:pygame.key.ScancodeWrapper):
        if keys[pygame.K_w]:
            self.__y -= speed * tick
        if keys[pygame.K_s]:
            self.__y += speed *tick
        if keys[pygame.K_a]:
            self.__x -= speed*tick
        if keys[pygame.K_d]:
            self.__x += speed * tick
        return self
    def draw(self,color):
        pygame.draw.circle(self.__screen,color,self.coords,self.__radius)
        return self
    
    def has_collision_with(self, other_ball:'Ball') -> bool:
        x, y = self.coords
        ox, oy = other_ball.coords
        if (x-ox)**2 + (y-oy)**2 <= (self.__radius + other_ball.__radius)**2:
            return True
        else:
            return False
    
    def line(self,other_ball:'Ball'):
        pygame.draw.aaline(self.__screen,"green",other_ball.coords,self.coords,10)
    
    def move_to_player(self,other_ball:'Ball',distance):
        if self.coords[0] > other_ball.coords[0]:
            self.__x -= distance/random.randrange(100,450)
        elif self.coords[0] < other_ball.coords[0]:
            self.__x += distance/random.randrange(100,450)
        if self.coords[1] > other_ball.coords[1]:
            self.__y -= distance/random.randrange(100,450)
        elif self.coords[1] < other_ball.coords[1]:
            self.__y += distance/random.randrange(100,450)
        
#초기화화
pygame.init()
myFont = pygame.font.SysFont( "arial", 30, True, False)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1060,950))
dt =0
point = 0
next_bot_CT = 1
next_bot_count = 7
spawned_bot = []

player = Ball(screen,pygame.Vector2(screen.get_width()/2,screen.get_height()/2),40)
mouse = Ball(screen,pygame.mouse.get_pos(),15)
pygame.mouse.set_visible(False)

player_health = Bar(screen,150)
next_bot = Bar(screen,400)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mouse.coords = pygame.mouse.get_pos()
    
    screen.fill("white")        

    #거리 계산산
    distance = sqrt((player.coords[0]-mouse.coords[0])**2 + (player.coords[1]-mouse.coords[1])**2)
    distance_color = 255 if int(distance) > 255 else int(distance)
    pygame.draw.aaline(screen,"green",mouse.coords,player.coords,10)
    
    #봇 게이지 
    if next_bot.var_max <= 0:
        spawned_bot.append(Ball(screen,[random.randint(0,screen.get_width()),random.randint(0,screen.get_height())],25))
        next_bot.full_change()
        next_bot_CT+=0.5
        point += 5
        
        next_bot_count = 20 if next_bot_count > 20 else next_bot_count + 1
        if len(spawned_bot) > next_bot_count:
            spawned_bot.pop(0)
    
    #봇 생성
    for bot in spawned_bot:
        bot.draw([0,0,255])
        bot.line(player)
        bot.move_to_player(player,distance)
        if player.has_collision_with(bot):
            player_health.active(10)
            spawned_bot.remove(bot)
        elif mouse.has_collision_with(bot):
            player_health.active(13)
            spawned_bot.remove(bot)
    
    if distance < 300:
        player.move(dt,distance*1.2,keys=pygame.key.get_pressed())
    else:
        player_health.active(1.5)
    
    if player.has_collision_with(mouse):
        player_health.active(0.5)
    
    if player_health.var_max <= 0:
        print("fsd")
        # pygame.display.flip()
        # pygame.time.delay(60000)
        

    dt = clock.tick(60) / 1000
    next_bot.active(next_bot_CT)
    
    #화면 표시시
    player.draw([255,distance_color,0])
    mouse.draw([255,distance_color,0])
    player_health.place(player.coords,0,60)
    next_bot.place((screen.get_width()/2,0),0,0)
    screen.blit(myFont.render(f"POINT : {point}",True,[0,0,0]),[0,0])
    pygame.display.flip()
    

pygame.quit()