"""Модуль для запуска игры 'Змейка'"""

from random import randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

screen.fill(BOARD_BACKGROUND_COLOR)


class GameObject():
    """Родительский класс игровых объектов"""

    def __init__(self, position=None, body_color=None):
        """Инициализация атрибутов игрового объекта"""
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовывания объектов на игровом поле,
        будет переопределяться в дочерних классах
        """
        pass


class Apple(GameObject):
    """Дочерний класс объекта яблоко"""

    def __init__(self, snake):
        """Инициализация атрибутов яблока, постановка яблока в рандомном месте
        на игровом поле
        """
        self.snake = snake
        GameObject.__init__(self, body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Функция для определения яблока в рандомном месте на игровом поле"""
        while self.position in self.snake.positions:
            self.position = [
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            ]

    def draw(self):
        """Функция для отрисовки яблока на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс объекта змейки"""

    def __init__(self, position=None):
        """Инициализация объекта змейка, установка дополнительных
        атрибутов змейки
        """
    #
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT
                         // 2] if position is None else position
        self.reset()
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления движения на игровом поле"""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Метод, двигающий змейку на игровом поле (каждая последующая позиция
        элемента змейки сохраняется в предыдущую. Голову двигаем "вручную")
        """
        direction_x, direction_y = self.direction
        self.last = self.positions[-1]
        self.head = self.get_head_position()
        self.positions.insert(
            0, [self.head[0] + direction_x * GRID_SIZE, self.head[1]
                + direction_y * GRID_SIZE])
        self.positions.pop()

    def draw(self):
        """Метод отрисовки тела змейки, её головы и затирание
        последнего следа
        """
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> list[int]:
        """Метод, возвращающий позицию головый змейки"""
        return self.positions[0]

    def reset(self):
        """Метод, возвращающий змейку в начальное состояние"""
        self.positions = [[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
        self.direction = RIGHT
        self.length = 1
        self.last = None
        self.next_direction = None


def handle_keys(game_object):
    """Метод, изменяющий направление змейки при нажатии игроком клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция запуска основного цикла игры"""
    snake = Snake()
    apple = Apple(snake)
    while True:
        clock.tick(SPEED)
        if apple.position in snake.positions:
            snake_direction_x, snake_direction_y = snake.direction
            snake.positions.append(
                [apple.position[0] + snake_direction_x * 20, apple.position[1]
                    + snake_direction_y * 20])
            apple.randomize_position()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[-1][0] == 640:
            snake.positions[-1][0] = 0
        if snake.positions[-1][0] == -20:
            snake.positions[-1][0] = 640
        if snake.positions[-1][1] == 480:
            snake.positions[-1][1] = 0
        if snake.positions[-1][1] == -20:
            snake.positions[-1][1] = 480

        if snake.positions[-1] in snake.positions[:-1]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()
            snake.reset()

        snake.draw()
        apple.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        pygame.display.update()


if __name__ == '__main__':
    main()
