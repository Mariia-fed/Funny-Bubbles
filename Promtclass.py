import pygame

WIDTH = 1024
HEIGHT = 768
PROMPT_WIDTH = 200
PROMPT_HEIGHT = 50
MAX_PROMPT_LENGTH = 10
ORANGE = (102, 195, 192)
BLACK = (0, 0, 0)


class Prompt:
    def __init__(self):
        self.value = ""

    def draw(self, screen, font):

        pygame.draw.rect(screen, ORANGE, (WIDTH // 2 - PROMPT_WIDTH // 2, HEIGHT - PROMPT_HEIGHT * 1.1,
                                          PROMPT_WIDTH, PROMPT_HEIGHT))
        prompt_text = font.render(self.value, True, BLACK)
        prompt_text_rect = prompt_text.get_rect()
        prompt_text_rect.centerx = WIDTH // 2
        prompt_text_rect.centery = HEIGHT - PROMPT_HEIGHT * 1.2 // 2
        screen.blit(prompt_text, prompt_text_rect)

    def add_digit(self, digit):
        if (len(self.value) < MAX_PROMPT_LENGTH and
                not (len(self.value) == 0 and digit == 0)):
            self.value += str(digit)

    def delete_digit(self):
        if len(self.value) > 0:
            self.value = self.value[:-1]
