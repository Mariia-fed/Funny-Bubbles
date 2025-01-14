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

'''Изображение на фон, есл нужно просто фон - это убрать'''
# window = pygame.display.set_mode((WIDTH, HEIGHT))
#
# background = pygame.image.load("bubbles2.jpg")
# background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# all_sprites = pygame.sprite.Group()
'''И это'''

HEART_SIZE = 35
STARTING_HEART_X = int(WIDTH - HEART_SIZE * 3.6)
HEART_Y = 20


PROMPT_WIDTH = WIDTH // 2
PROMPT_HEIGHT = 50


class Game:
    """Создаем игровое окошко"""

    def __init__(self):
        self.problems = None
        self.lives = None
        self.score = None
        self.prompt = None
        self.font = None
        self.screen = None
        pygame.init()
        self.set_up_canvas()
        self.running = True
        self.clock = pygame.time.Clock()
        self.tick = 0
        self.start_new_game()

    def set_up_canvas(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Funny Bubbles')
        icon = pygame.image.load('bubbles.jpg')
        pygame.display.set_icon(icon)
        self.font = pygame.font.SysFont('Arial bolt', 32)
        self.prompt = Prompt()

    def start_new_game(self):
        self.score = 0
        self.lives = STARTING_LIVES
        self.problems = []

    def launch(self):
        while self.running:
            self.handle_events()
            self.change_game_states()
            self.draw()
            self.clock.tick(FPS)
            # Это изображение на фон
            # window.blit(background, (0, 0))
            # all_sprites.draw(window)
            # pygame.display.update()
            self.tick += 1

    """Возращает список всех событий, который произошли за последний фрейм
    Когда закрываем окно игра останавливается"""

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event == pygame.KEYDOWN:
                self.handle_key_press(event.key)

    def handle_key_press(self, key):
        if key == pygame.K_ESCAPE:
            self.running = False
        elif 48 <= key <= 57:
            ...
        elif key == pygame.K_BACKSPACE:
            ...
        elif key == pygame.K_RETURN:
            ...

    def change_game_states(self):
        self.check_spawn()
        self.solve_problems()
        self.move_problems()
        self.check_life_loss()

    def check_spawn(self):
        pass

    def solve_problems(self):
        pass

    def move_problems(self):
        pass

    def check_life_loss(self):
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_problems()
        self.print_score()
        self.print_lives()
        self.prompt.draw(self.screen, self.font)
        pygame.display.flip()

    def draw_problems(self):
        pass

    def print_score(self):
        score_text = self.font.render(f'SCORE: {self.score}', True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.x, score_text_rect.y = 20, 20
        self.screen.blit(score_text, score_text_rect)

    def print_lives(self,  colorkey=None):
        # heart_image = pygame.image.load('heart.png')
        # heart_sprite = heart_image.convert_alpha()
        # heart_sprite = pygame.transform.smoothscale(heart_sprite, (HEART_SIZE, HEART_SIZE))
        # heart_x = STARTING_HEART_X
        # for _ in range(self.lives):
        #     self.screen.blit(heart_sprite, (heart_x, HEART_Y))
        #     heart_x += int(HEART_SIZE * 1.1)
        heart_image = pygame.image.load('Heart.png')
        if colorkey is not None:
            heart_image = heart_image.convert()
            if colorkey == -1:
                colorkey = heart_image.get_at((0, 0))
            heart_image.set_colorkey(colorkey)
        else:
            heart_image = heart_image.convert_alpha()
        heart_sprite = pygame.transform.scale(heart_image, (HEART_SIZE, HEART_SIZE))
        heart_x = STARTING_HEART_X
        for _ in range(self.lives):
            self.screen.blit(heart_sprite, (heart_x, HEART_Y))
            heart_x += int(HEART_SIZE * 1.1)

    def __del__(self):
        pygame.quit()


class Problem:
    def __init__(self):
        pass


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
        pygame.draw.rect(screen, ORANGE, (int(WIDTH * 0.1), int(HEIGHT * 0.1),
                                          WIDTH * 0.8, HEIGHT * 0.8), 5)


def main():
    game = Game()
    game.launch()


if __name__ == '__main__':
    main()

