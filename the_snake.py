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

    def draw_cell(self, screen, grid_position):
        """Метод отрисовки ячейки"""
        rect = pygame.Rect(grid_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс объекта яблоко"""

    def __init__(self):
        """Инициализация атрибутов яблока, постановка яблока в рандомном месте
        на игровом поле
        """
        GameObject.__init__(self, body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Функция для определения яблока в рандомном месте на игровом поле"""
        self.position = [
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        ]
        while self.position in Snake().positions:
            self.position = [
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            ]

    def draw(self):
        """Функция для отрисовки яблока на игровом поле"""
        self.draw_cell(screen, self.position)


class Snake(GameObject):
    """Дочерний класс объекта змейки"""

    def __init__(self, position=None):
        """Инициализация объекта змейка, установка дополнительных
        атрибутов змейки
        """
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT
                         // 2] if position is None else position
        self.reset()
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления движения на игровом поле"""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Метод, двигающий змейку на игровом поле"""
        direction_x, direction_y = self.direction
        self.last = self.positions[-1]
        self.head = self.get_head_position()
        new_position = [
            self.head[0] % SCREEN_WIDTH,
            self.head[1] % SCREEN_HEIGHT
        ]
        self.positions[0] = new_position
        self.positions.insert(
            0, [self.get_head_position()[0] + direction_x * GRID_SIZE,
                self.get_head_position()[1] + direction_y * GRID_SIZE])
        if self.length == len(self.positions) - 1:
            self.positions.pop()

    def draw(self):
        """Метод отрисовки тела змейки, её головы и затирание
        последнего следа
        """
        for position in self.positions:
            self.draw_cell(screen, position)
        self.draw_cell(screen, self.get_head_position())
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> list[int]:
        """Метод, возвращающий позицию головы змейки"""
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
    apple = Apple()
    while True:
        clock.tick(SPEED)
        apple.draw()
        if apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()
            snake.reset()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
