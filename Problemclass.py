import random
import pygame

BUBBLE_SPEED = 30
BUBBLE_FREQUENCY = 40
BUBBLE_RADIUS = 50
BLACK = (0, 0, 0)


class Problem:
    def __init__(self):
        self.a = random.randint(1, 9)
        self.b = random.randint(1, 9)
        self.solution = self.a + self.b
        self.x = random.randint(102 + BUBBLE_RADIUS, 921 - BUBBLE_RADIUS)
        self.y = 690 - BUBBLE_RADIUS
        self.active = True

    def draw(self, screen, font):
        bubble_image = pygame.image.load('puzirik.png')
        bubble_image = pygame.transform.smoothscale(bubble_image, (100, 100))
        screen.blit(bubble_image, (self.x - 50, self.y - 50))
        problem_text = font.render(f'{self.a} + {self.b}', True, BLACK)
        problem_text_rect = problem_text.get_rect()
        problem_text_rect.centerx = self.x
        problem_text_rect.centery = self.y
        screen.blit(problem_text, problem_text_rect)

    def move(self):
        self.y -= BUBBLE_SPEED
