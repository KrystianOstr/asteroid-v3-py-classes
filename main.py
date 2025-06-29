from random import randint, uniform
import pygame
import sys


class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("assets/graphics/ship.png").convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.can_shoot = True
        self.shoot_time = None

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(laser_group, self.rect.midtop)

    def update(self):
        self.laser_timer()
        self.laser_shoot()
        self.input_position()


class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.pos = pos
        self.image = pygame.image.load("assets/graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.pos))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))


class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)

        self.pos = pos
        self.image = pygame.image.load("assets/graphics/meteor.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.pos))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = 600

    def destroy_meteor_when_out_of_screen(self):
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.destroy_meteor_when_out_of_screen()


class Score:
    def __init__(self):
        self.font = pygame.font.Font("assets/graphics/subatomic.ttf", 50)

    def display(self, surface):
        score_text = self.font.render(
            f"Score: {pygame.time.get_ticks() // 1000}", True, (255, 255, 255)
        )
        text_rect = score_text.get_rect(
            midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        )
        surface.blit(score_text, text_rect)
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            text_rect.inflate(30, 30),
            width=8,
            border_radius=5,
        )


# basic setup
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Shooter - Classes")
clock = pygame.time.Clock()

# timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

# bg surf
background_surface = pygame.image.load("assets/graphics/background.png").convert()

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)
score = Score()


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
        if event.type == meteor_timer:
            meteor_x_pos = randint(-100, SCREEN_WIDTH + 100)
            meteor_y_pos = randint(-100, -50)
            meteor = Meteor(meteor_group, (meteor_x_pos, meteor_y_pos))

    # delta time

    dt = clock.tick() / 1000

    # background
    display_surface.blit(background_surface, (0, 0))

    # update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()

    # score update
    score.display(display_surface)

    # graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    pygame.display.update()
