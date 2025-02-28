import random
import pygame
import sqlite3

# Создаем подключение к базе данных (файл my_database.db будет создан)
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER
)
''')
connection.commit()
connection.close()

WIDTH = 1024
HEIGHT = 768

STARTING_LIVES = 3
STARTING_LEVEL = 1
SCORE_NEW_LIFE = 5000

BUBBLE_SPEED = 30  # Увеличиваем скорость шариков
BUBBLE_FREQUENCY = 40  # Сколько раз за 5 сек появляется пример
BUBBLE_RADIUS = 50

FPS = 24

BG_COLOR = (142, 235, 232)
BUBBLE_COLOR1 = (255, 192, 203)
WHITE = (255, 255, 255)
ORANGE = (102, 195, 192)
BLACK = (0, 0, 0)

HEART_SIZE = 32
STARTING_HEART_X = int(WIDTH - HEART_SIZE * 3.6)
HEART_Y = 20

PROMPT_WIDTH = 200
PROMPT_HEIGHT = 50
MAX_PROMPT_LENGTH = 10

TARGET_RECT = pygame.Rect(int(WIDTH * 0.1), int(HEIGHT * 0.1), WIDTH * 0.8, HEIGHT * 0.8)


class Game:
    """Создаем игровое окошко"""

    def __init__(self):
        self.screen = None
        pygame.init()
        self.set_up_canvas()
        self.running = True
        self.clock = pygame.time.Clock()
        self.start_new_game()
        self.registration_screen = False
        self.registration_input = {"username": "", "email": "", "age": ""}
        self.current_input_field = "username"
        self.registration_message = ""

    def set_up_canvas(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Funny Bubbles')
        icon = pygame.image.load('bubbles.jpg')
        pygame.display.set_icon(icon)
        self.font = pygame.font.SysFont('Arial bolt', 32)
        self.big_font = pygame.font.SysFont('Arial bolt', 80)
        self.prompt = Prompt()

    def start_new_game(self):
        self.score = 0
        self.lives = STARTING_LIVES
        self.problems = []
        self.tick = 0
        self.solution = None
        self.level = STARTING_LEVEL
        self.next_life_score = SCORE_NEW_LIFE
        self.start_screen = True
        self.game_over_screen = False

    def start_new_life(self):
        self.problems = []
        self.tick = 0

    def launch(self):
        while self.running:
            self.handle_events()
            if not self.start_screen and not self.game_over_screen and not self.registration_screen:
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
            elif key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
                self.registration_screen = True
        elif self.game_over_screen:
            if key == pygame.K_RETURN:
                self.game_over_screen = False
                self.start_new_game()
        elif self.registration_screen:
            if key == pygame.K_RETURN:
                self.save_registration_data()
            elif key == pygame.K_TAB:
                self.switch_input_field()
            elif key == pygame.K_BACKSPACE:
                self.registration_input[self.current_input_field] = self.registration_input[self.current_input_field][:-1]
            else:
                char = pygame.key.name(key)
                if len(char) == 1:
                    self.registration_input[self.current_input_field] += char
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

    def switch_input_field(self):
        if self.current_input_field == "username":
            self.current_input_field = "email"
        elif self.current_input_field == "email":
            self.current_input_field = "age"
        else:
            self.current_input_field = "username"

    def save_registration_data(self):
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        # Проверяем, существует ли пользователь с такими же данными
        cursor.execute('SELECT * FROM Users WHERE username = ? OR email = ?',
                       (self.registration_input["username"], self.registration_input["email"]))
        existing_user = cursor.fetchone()

        if existing_user:
            self.registration_message = "Пользователь уже существует!"
        else:
            cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)',
                           (self.registration_input["username"], self.registration_input["email"], int(self.registration_input["age"])))
            connection.commit()
            self.registration_message = "Регистрация завершена!"
            self.registration_input = {"username": "", "email": "", "age": ""}

        connection.close()

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
        elif self.registration_screen:
            self.draw_registration_screen()
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
        start_text_3 = self.font.render(f'Press SHIFT and then ENTER to become a user', True, WHITE)
        start_text_rect_1 = start_text_1.get_rect()
        start_text_rect_2 = start_text_2.get_rect()
        start_text_rect_3 = start_text_3.get_rect()
        start_text_rect_1.centerx = WIDTH // 2
        start_text_rect_1.y = HEIGHT // 2 - 50
        start_text_rect_2.centerx = WIDTH // 2
        start_text_rect_2.y = HEIGHT // 2 + 50
        start_text_rect_3.centerx = WIDTH // 2
        start_text_rect_3.y = HEIGHT // 2 + 120
        self.screen.blit(start_text_1, start_text_rect_1)
        self.screen.blit(start_text_2, start_text_rect_2)
        self.screen.blit(start_text_3, start_text_rect_3)

    def draw_registration_screen(self):
        self.screen.fill(ORANGE)
        registration_text_1 = self.big_font.render(f'REGISTRATION', True, WHITE)
        registration_text_2 = self.font.render(f'Username: {self.registration_input["username"]}', True, WHITE)
        registration_text_3 = self.font.render(f'Email: {self.registration_input["email"]}', True, WHITE)
        registration_text_4 = self.font.render(f'Age: {self.registration_input["age"]}', True, WHITE)
        registration_text_5 = self.font.render(f'Press TAB to switch field, ENTER to save', True, WHITE)
        registration_text_6 = self.font.render(self.registration_message, True, WHITE)
        registration_text_rect_1 = registration_text_1.get_rect()
        registration_text_rect_2 = registration_text_2.get_rect()
        registration_text_rect_3 = registration_text_3.get_rect()
        registration_text_rect_4 = registration_text_4.get_rect()
        registration_text_rect_5 = registration_text_5.get_rect()
        registration_text_rect_6 = registration_text_6.get_rect()
        registration_text_rect_1.centerx = WIDTH // 2
        registration_text_rect_1.y = HEIGHT // 2 - 150
        registration_text_rect_2.centerx = WIDTH // 2
        registration_text_rect_2.y = HEIGHT // 2 - 50
        registration_text_rect_3.centerx = WIDTH // 2
        registration_text_rect_3.y = HEIGHT // 2
        registration_text_rect_4.centerx = WIDTH // 2
        registration_text_rect_4.y = HEIGHT // 2 + 50
        registration_text_rect_5.centerx = WIDTH // 2
        registration_text_rect_5.y = HEIGHT // 2 + 150
        registration_text_rect_6.centerx = WIDTH // 2
        registration_text_rect_6.y = HEIGHT // 2 + 200
        self.screen.blit(registration_text_1, registration_text_rect_1)
        self.screen.blit(registration_text_2, registration_text_rect_2)
        self.screen.blit(registration_text_3, registration_text_rect_3)
        self.screen.blit(registration_text_4, registration_text_rect_4)
        self.screen.blit(registration_text_5, registration_text_rect_5)
        self.screen.blit(registration_text_6, registration_text_rect_6)

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


def main():
    game = Game()
    game.launch()


if __name__ == '__main__':
    main()