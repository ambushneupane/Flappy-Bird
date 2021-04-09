import pygame
from pygame.locals import *
import random

pygame.init()
width = 764
height = 736
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

FPS = 60
clock = pygame.time.Clock()

# load
bg = pygame.image.load("background.png")
ground_img = pygame.image.load("ground.png")
button_img = pygame.image.load("restart.png")

font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)

# define game variable
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipeGap = 180
pipe_Frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_Frequency
score = 0
pass_pipe = False


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(height / 2)
    score = 0
    return score


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.clicked = False
        self.vel = 0

    def update(self):
        if flying == True:

            # gravity
            self.vel += 0.5
            if self.vel >= 8:
                self.vel = 8
            if self.rect.bottom < 650:
                self.rect.y += int(self.vel)  # Decreases the y coordinate of the rect(bird)

        if game_over == False:



            # jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # returns list :- LEft click , middle, right

                self.clicked = True
                self.vel = -10  # negative velocity takes the bird up
            if pygame.mouse.get_pressed()[0] == 0:  # returns list :- LEft click , middle, right
                self.clicked = False

            # handling the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0

                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from Top and -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipeGap / 2)]

        if position == -1:
            self.rect.topleft = [x, y + int(pipeGap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        mouse_action = False
        # get mouse position
        position = pygame.mouse.get_pos()

        # Checking if mouse is over the button
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1:
                mouse_action = True
        # drawing the button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return mouse_action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, int(height / 2))

bird_group.add(flappy)
# Button Instance
button = Button(width // 2 - 50, height // 2 - 100, button_img)

running = True
while running:
    clock.tick(FPS)
    # Background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # Drawing the ground
    screen.blit(ground_img, (ground_scroll, 650))

    if len(pipe_group) > 0:  # pipe_group are like lists
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(width / 2), 20)
    # Looks for collison
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
        # screen.blit(button_img,(width//2 - 50, height // 2 - 100))

    # Check if bird hit the ground
    if flappy.rect.bottom >= 650:
        game_over = True
        flying = False

    if game_over == False and flying == True:

        # Generating new pipes
        time_now = pygame.time.get_ticks()

        if time_now - last_pipe > pipe_Frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(width, int(height / 2) + pipe_height, -1)
            top_pipe = Pipe(width, int(height / 2) + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:  # to keep the ground continously  moving.
            ground_scroll = 0
        pipe_group.update()

    # Checking game Over and Resetting
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()
pygame.quit()
