import random
import pygame

BUBBLE_SPEED = 30
BUBBLE_FREQUENCY = 40
BUBBLE_RADIUS = 50
BLACK = (0, 0, 0)


class Problem:
    def __init__(self):
        # Случайно выбираем между умножением и делением
        self.operation = random.choice(['*', '/'])

        if self.operation == '*':
            # Генерация задачи на умножение
            self.a = random.randint(1, 9)
            self.b = random.randint(1, 9)
            self.solution = self.a * self.b
        else:
            # Генерация задачи на деление
            self.b = random.randint(1, 9)
            self.solution = random.randint(1, 9)
            self.a = self.b * self.solution  # Убедимся, что деление будет целым

        self.x = random.randint(102 + BUBBLE_RADIUS, 921 - BUBBLE_RADIUS)
        self.y = 690 - BUBBLE_RADIUS
        self.active = True

    def draw(self, screen, font):
        bubble_image = pygame.image.load('img/puzirik.png')
        bubble_image = pygame.transform.smoothscale(bubble_image, (100, 100))
        screen.blit(bubble_image, (self.x - 50, self.y - 50))
        problem_text = font.render(f'{self.a} {self.operation} {self.b}', True, BLACK)
        problem_text_rect = problem_text.get_rect()
        problem_text_rect.centerx = self.x
        problem_text_rect.centery = self.y
        screen.blit(problem_text, problem_text_rect)

    def move(self):
        self.y -= BUBBLE_SPEED