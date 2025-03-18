import pygame
from pygame import locals
from math import sqrt

# def map_value(x, in_min, in_max, out_min, out_max):
#     return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
class Ball:
    def __init__(self, screen:pygame.Surface, color:list=[255,0,0], coords:tuple[float, float]= (0,0), radius:float = 3, width:float=0, **kwargs) -> None:
        self.screen = screen
        self.x, self.y = coords
        self.radius = radius
        self.width = width
        self.color = color
        self.kwargs = kwargs

    @property
    def coords(self) -> tuple[float, float]:
        return self.x, self.y

    def move(self, pressed_keys:pygame.key.ScancodeWrapper,tick) -> 'Ball':
        if pressed_keys[locals.K_UP]:
            self.y -= 300 * tick
        if pressed_keys[locals.K_DOWN]:
            self.y += 300 * tick
        if pressed_keys[locals.K_LEFT]:
            self.x -= 300 * tick
        if pressed_keys[locals.K_RIGHT]:
            self.x += 300 * tick
        return self

    def draw(self) -> 'Ball':
        pygame.draw.circle(self.screen, color=self.color, center=self.coords, radius=self.radius, width=self.width, **self.kwargs)
        return self

class Health:
    def __init__(self,bg,max):
        self.max=max
        self.var_max = max
        self.bg = bg
    
    def place(self,pos,plus_x,plus_y):
        pygame.draw.rect(self.bg,"black",[(pos[0]-self.max/2)-plus_x,pos[1]-plus_y,self.max,10])
        pygame.draw.rect(self.bg,"red",[(pos[0]-self.max/2)-plus_x,pos[1]-plus_y,self.var_max,10])
        
    def active(self,num):
        if self.var_max > 0:
            self.var_max -= num

pygame.init()
clock = pygame.time.Clock()
player_color = [255,255,0]
screen = pygame.display.set_mode((1060,950))
player_pos = pygame.Vector2(screen.get_width()/2,screen.get_height()/2)
player = Ball(screen,player_color,player_pos,40,0)
pygame.mouse.set_visible(False)
dt =0

player_health = Health(screen,150)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mouse_pos = pygame.mouse.get_pos()
    
    screen.fill("white")        
    player_health.place(player_pos,0,60)
    distance = sqrt((player_pos[0]-mouse_pos[0])**2 + (player_pos[1]-mouse_pos[1])**2)
    distance_color = 255 if int(distance) > 255 else int(distance)
    pygame.draw.aaline(screen,"green",mouse_pos,player_pos,10)
    
    # player=pygame.draw.circle(screen,[255,distance_color,0],player_pos,40)
    # mouse =pygame.draw.circle(screen,[255,distance_color,0],mouse_pos,20)
    player.move(pressed_keys=pygame.key.get_pressed()).draw(dt)
    
    dt = clock.tick(60) / 1000
    pygame.display.flip()
    
            

pygame.quit()