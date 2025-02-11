import pygame

from Problemclass import Problem
from Promtclass import Prompt

WIDTH = 1024
HEIGHT = 768

STARTING_LIVES = 3
STARTING_LEVEL = 1
SCORE_NEW_LIFE = 5000

BUBBLE_FREQUENCY = 40

FPS = 24

WHITE = (255, 255, 255)
ORANGE = (102, 195, 192)

HEART_SIZE = 32
STARTING_HEART_X = int(WIDTH - HEART_SIZE * 3.6)
HEART_Y = 20

TARGET_RECT = pygame.Rect(int(WIDTH * 0.1), int(HEIGHT * 0.1), WIDTH * 0.8, HEIGHT * 0.8)


class Game:
    def __init__(self):
        self.screen = None
        self.solution = None
        pygame.init()
        self.set_up_canvas()
        self.font = pygame.font.SysFont('Arial bolt', 32)
        self.big_font = pygame.font.SysFont('Arial bolt', 80)
        self.running = True
        self.start_screen = True
        self.game_over_screen = False
        self.score = 0
        self.tick = 0
        self.lives = STARTING_LIVES
        self.level = STARTING_LEVEL
        self.next_life_score = SCORE_NEW_LIFE
        self.problems = []
        self.prompt = Prompt()
        self.clock = pygame.time.Clock()
        self.start_new_game()

    def set_up_canvas(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Funny Bubbles')
        icon = pygame.image.load('bubbles.jpg')
        pygame.display.set_icon(icon)

    def start_new_game(self):
        self.score = 0
        self.tick = 0
        self.problems = []
        self.start_screen = True
        self.solution = None
        self.game_over_screen = False
        self.lives = STARTING_LIVES
        self.level = STARTING_LEVEL
        self.next_life_score = SCORE_NEW_LIFE

    def start_new_life(self):
        self.problems = []
        self.tick = 0

    def launch(self):
        while self.running:
            self.handle_events()
            if not self.start_screen and not self.game_over_screen:
                self.change_game_state()
            self.draw()
            self.clock.tick(FPS)
            self.tick += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)

    def handle_key_press(self, key):
        if self.start_screen:
            if key == pygame.K_RETURN:
                self.start_screen = False
        elif self.game_over_screen:
            if key == pygame.K_RETURN:
                self.game_over_screen = False
                self.start_new_game()
        else:
            if key == pygame.K_ESCAPE:
                self.running = False
            elif 48 <= key <= 57:
                self.prompt.add_digit(key - 48)
            elif key == pygame.K_BACKSPACE:
                self.prompt.delete_digit()
            elif key == pygame.K_RETURN:
                self.solution = int(self.prompt.value)
                self.prompt.value = ""

    def change_game_state(self):
        self.check_spawn()
        if self.solution:
            self.solve_problems()
            self.solution = None
        for problem in self.problems:
            if problem.active:
                problem.move()
        self.check_life_loss()

    def check_spawn(self):
        if self.tick % (120 // BUBBLE_FREQUENCY) == 0:
            self.problems.append(Problem())

    def solve_problems(self):
        for problem in self.problems:
            if problem.solution == self.solution:
                problem.active = False
                self.score += self.level * 100
                self.check_for_new_life()

    def check_for_new_life(self):
        if self.score >= self.next_life_score and self.lives < 3:
            self.lives += 1
            self.next_life_score += SCORE_NEW_LIFE

    def check_life_loss(self):
        for problem in self.problems:
            if not TARGET_RECT.collidepoint(problem.x, problem.y - 40):
                self.lives -= 1
                problem.active = False
                self.start_new_life()
                break
        if self.lives == 0:
            self.game_over_screen = True

    def draw(self):
        self.screen.fill(ORANGE)
        if self.start_screen:
            self.draw_start_screen()
        elif self.game_over_screen:
            self.draw_game_over_screen()
        else:
            background = pygame.image.load("puziriki.jpg")
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            self.screen.blit(background, (0, 0))
            for problem in self.problems:
                if problem.active:
                    problem.draw(self.screen, self.font)
            self.print_score()
            self.print_lives()
            self.prompt.draw(self.screen, self.font)
            pygame.draw.rect(self.screen, ORANGE, TARGET_RECT, 5)
        pygame.display.flip()

    def draw_start_screen(self):
        bubble_image = pygame.image.load('puzirik.png')
        bubble_image = pygame.transform.smoothscale(bubble_image, (600, 600))
        self.screen.blit(bubble_image, (215, 74))
        start_text_1 = self.big_font.render(f'FUNNY BUBBLES', True, WHITE)
        start_text_2 = self.font.render(f'Press ENTER to begin', True, WHITE)
        start_text_rect_1 = start_text_1.get_rect()
        start_text_rect_2 = start_text_2.get_rect()
        start_text_rect_1.centerx = WIDTH // 2
        start_text_rect_1.y = HEIGHT // 2 - 50
        start_text_rect_2.centerx = WIDTH // 2
        start_text_rect_2.y = HEIGHT // 2 + 50
        self.screen.blit(start_text_1, start_text_rect_1)
        self.screen.blit(start_text_2, start_text_rect_2)

    def draw_game_over_screen(self):
        game_over_text_1 = self.big_font.render(f'GAME OVER', True, WHITE)
        game_over_text_2 = self.font.render(f'FINAL SCORE: {self.score}', True, WHITE)
        game_over_rect_1 = game_over_text_1.get_rect()
        game_over_rect_2 = game_over_text_2.get_rect()
        game_over_rect_1.centerx = WIDTH // 2
        game_over_rect_1.y = HEIGHT // 2 - 50
        game_over_rect_2.centerx = WIDTH // 2
        game_over_rect_2.y = HEIGHT // 2 + 50
        self.screen.blit(game_over_text_1, game_over_rect_1)
        self.screen.blit(game_over_text_2, game_over_rect_2)

    def print_score(self):
        score_text = self.font.render(f'SCORE: {self.score}', True, ORANGE)
        score_text_rect = score_text.get_rect()
        score_text_rect.x, score_text_rect.y = 20, 20
        self.screen.blit(score_text, score_text_rect)

    def print_lives(self):
        heart_image = pygame.image.load('Pics.png')
        heart_sprite = heart_image.convert_alpha()
        heart_sprite = pygame.transform.smoothscale(heart_sprite, (HEART_SIZE, HEART_SIZE))
        heart_x = STARTING_HEART_X
        for _ in range(self.lives):
            self.screen.blit(heart_sprite, (heart_x, HEART_Y))
            heart_x += int(HEART_SIZE * 1.1)

    def __del__(self):
        pygame.quit()


def main():
    game = Game()
    game.launch()


if __name__ == '__main__':
    main()
