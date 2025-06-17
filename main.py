import pygame
import sys

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.pos = pos
        self.image = pygame.image.load('assets/graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(center=(self.pos))


# basic setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Shooter- Classes")
clock = pygame.time.Clock()

background_surface = pygame.image.load('assets/graphics/background.png').convert()


# sprite groups
spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)
laser = Laser(spaceship_group, (100,500))

# game loop
while True:


    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # delta time
    clock.tick(120)

    # background
    display_surface.blit(background_surface, (0,0))

    # graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)

    pygame.display.update()