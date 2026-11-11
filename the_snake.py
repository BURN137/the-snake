from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Описывается базовый игровой объект."""
    def __init__(self, position: list[tuple[int, int]] | tuple[int, int], body_color: tuple[int, int, int]) -> None:
        self.position = position
        self.body_color = body_color


    def draw(self) -> None:
        pass


class Apple(GameObject):
    """Описываем класс "Яблоко"."""
    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR 


    def randomize_position(self)-> tuple[int, int]:
        """Генератор координат яблока"""
        while True:
            apple_position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if apple_position != (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2):
                break
        return apple_position


    def draw(self) -> None:
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описываем класс "Змея"."""
    


    def __init__(self) -> None:
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 1
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


    def move(self) -> None:
        """
        Обновляет позицию змейки,
        добавляя новую голову в начало списка и
        удаляя последний элемент, если длина змейки не увеличилась.
        """ 
        head_position = self.get_head_position()
        if self.next_direction is None:
            next_head_position = (
                (head_position[0] + GRID_SIZE * self.direction) % SCREEN_WIDTH,
                head_position[1] % SCREEN_HEIGHT
            )
        else:
            next_head_position = (
                (head_position[0] + GRID_SIZE * self.next_direction[0]) % SCREEN_WIDTH,
                (head_position[1] + GRID_SIZE * self.next_direction[1]) % SCREEN_HEIGHT
            )
        list.insert(self.positions, 0, (next_head_position))
        if head_position in self.positions[2:]:
            self.reset()
        else:
            self.last = self.positions[-1]
            del self.positions[-1]
            


    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return (self.positions[0])


    def reset(self):
        """Сбрасывает змейку в начальное положение"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.next_direction = choice([UP, LEFT, RIGHT, DOWN])
        screen.fill(BOARD_BACKGROUND_COLOR) 
        #pass     



# Функция обработки действий пользователя
def handle_keys(game_object) -> None:
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


def main() -> None:
    # Инициализация PyGame:
    pygame.init()
    # Создаем экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(2) # Исправить на SPEED
        handle_keys(snake)
        snake.move()
        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position()
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
            list.append(snake.positions, apple.position)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
