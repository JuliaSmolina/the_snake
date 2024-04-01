import random

APPLE_COLOR = (255,0,0)
SNAKE_COLOR = (0, 255, 0)
SNAKE_POSITION = [310,230]
SNAKE_POSITIONS = [[309,229],[310,230]]
LENGTH = 1

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


class GameObject():

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color
    
    def draw(self):
        pass

class Apple(GameObject):

        def __init__(self, body_color, position):
            super().__init__(position, body_color)
            pass

        def randomize_position(self, position):
            self.position = position.random.randint(0, 210)

        def draw(self) -> None:
            pass

    
class Snake(GameObject):

    
    def __init__(self, position, body_color, segment_positions, direction, length):
        self.segment_positions = segment_positions
        self.direction = direction
        self.length = length
        super().__init__(position, body_color)
        
        
    def draw(self):
        direction_1, direction_2 = self.direction 
        for segment in self.segment_positions:
            segment[0] = segment[0] + direction_1
            segment[1] = segment[1] + direction_2
        
        # for position in self.positions[:-1]:
            

        # Отрисовка головы змейки


        # Затирание последнего сегмента


    # def update_direction(self):
    #     if self.next_direction:
    #         self.direction = self.next_direction
    #         self.next_direction = None

green_snake = Snake(SNAKE_POSITION, SNAKE_COLOR, SNAKE_POSITIONS, RIGHT, LENGTH)
print(green_snake.direction)
print(green_snake.segment_positions)
green_snake.draw()
print(green_snake.segment_positions)

red_apple = Apple(APPLE_COLOR, [0, 0])
print(red_apple.position)