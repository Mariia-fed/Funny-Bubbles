import pygame

WIDTH = 1024
HEIGHT = 800

STARTING_LIVES = 3
FPS = 24

LEVEL = 1

PROBLEM_SPEED = 1
PROBLEM_FREQUENCY = 1

BG_COLOR = (255, 219, 139)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

HEART_SIZE = 35
STARTING_HEART_X = int(WIDTH - HEART_SIZE * 3.6)
HEART_Y = 20


PROMPT_WIDTH = WIDTH // 2
PROMPT_HEIGHT = 50


def update_my_screen(event, bubble):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            bubble.movie_right = True
        if event.key == pygame.K_LEFT:
            bubble.movie_left = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            bubble.movie_right = False
        if event.key == pygame.K_LEFT:
            bubble.movie_left = False

    bubble.moving()


def draw_my_screen(bubble):
    bubble.draw_on_screen()


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Funny bubbles')
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(1)
    game_active = True
    bubble = Bubble(screen)

    while game_active:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False

        update_my_screen(event, bubble)
        draw_my_screen(bubble)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


class Bubble:
    def __init__(self, screen):
        self.screen = screen
        self.pos_x = 100
        self.pos_y = 100
        self.radius = 10
        self.color = (0, 0, 255)
        self.movie_left = False
        self.movie_right = False

        self.max_y = 800 - self.radius
        self.max_x = 1200 - self.radius

    def moving(self):
        if self.movie_left == True:
            self.pos_x -= 5
            if self.pos_x < self.radius:
                self.pos_x = self.radius
        if self.movie_right == True:
            self.pos_x += 5
            if self.pos_x > self.max_x:
                self.pos_x = self.max_x

    def draw_on_screen(self):
        pygame.draw.circle(self.screen, self.color, (self.pos_x, self.pos_y), self.radius)


run_game()
