import pygame
import math
from sys import exit
from random import randint
from pygame import Vector2 as vector
from pygame.locals import *
#CONSTANTS
WIDTH = 1280
HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREY = (64,64,64)
screen_size = vector(WIDTH,HEIGHT)
screen_center = screen_size // 2

# Initialize Pygame
pygame.init()
# SET DISPLAYS
screen = pygame.display.set_mode(screen_size, flags = pygame.SCALED)
pygame.display.set_caption("one shot")

#LOAD ASSETS
gun_img = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/shotgun1.xcf').convert_alpha(), 0.25)
player_img = pygame.transform.scale_by(pygame.image.load('Assets/Sprites/flappy.xcf').convert_alpha(), 0.5)

reference_dict = {'Weapon': gun_img, 'Player':player_img}
#DEFINE FUNCTIONS
def rotate_on_pivot(image,angle,pivot,origin):

    surf = pygame.transform.rotate(image, angle)

    offset = pivot + (origin - pivot).rotate(-angle)

    rect = surf.get_rect(center = offset)

    return surf, rect

class Weapon(pygame.sprite.Sprite):
    def __init__(self,pivot):
        super().__init__()
        self.pivot  = pivot
        self.pos = pivot

        self.image_unflipped = pygame.transform.flip(reference_dict['Weapon'],True,False)
        self.image_flipped = pygame.transform.flip(self.image_unflipped,False,True)

        self.image = self.image_unflipped
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        mouse_pos = vector(pygame.mouse.get_pos())

        if mouse_pos.x < screen_center.x:
            rotate_img = self.image_flipped
        else:
            rotate_img = self.image_unflipped

        mouse_offset = mouse_pos - self.pivot
        mouse_angle= -math.degrees(math.atan2(mouse_offset.y, mouse_offset.x))
        self.image, self.rect = rotate_on_pivot(rotate_img, mouse_angle, self.pivot, self.pos)

    def draw(self, surf):
        surf.blit(self.image,self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = reference_dict['Player']


# TIMERS
clock = pygame.time.Clock()
game_active = True

# Main loop
def game():
    gun = Weapon(screen_center)
    sprites = pygame.sprite.Group()
    sprites.add(gun)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.fill(WHITE)
        sprites.draw(screen)
        sprites.update()
        # sprites.update()
        

        pygame.display.update()
        clock.tick(60)

game()