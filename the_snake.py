from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480  # Размер поля
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Центр поля
GRID_SIZE = 20  # Размер сетки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Высота поля в сетках
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # Ширина поля сетках


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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Описывается базовый игровой объект."""

    def __init__(
            self,
            position=SCREEN_CENTER,
            body_color=None
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Отрисовка базового игрового объекта"""


class Apple(GameObject):
    """Описываем класс "Яблоко"."""

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self) -> tuple[int, int]:
        """Генератор координат яблока"""
        while True:
            apple_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

            # Проверяем, чтобы яблоко не создалось по середине экрана
            if apple_position != SCREEN_CENTER:
                break
        return apple_position

    def draw(self) -> None:
        """Отрисовка яблока на экране"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описываем класс "Змея"."""

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [SCREEN_CENTER]
        self.direction = 1
        self.next_direction = None
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
        # Задаем начальное направление змейки вправо.
        if self.next_direction is None:
            next_head_position = (
                (head_position[0] + GRID_SIZE * self.direction) % SCREEN_WIDTH,
                head_position[1] % SCREEN_HEIGHT
            )

        # Направление движения змейки в зависимости
        # от нажатой кнопки пользователем.
        else:
            next_head_position = (
                (
                    head_position[0] + GRID_SIZE * self.next_direction[0]
                ) % SCREEN_WIDTH,
                (
                    head_position[1] + GRID_SIZE * self.next_direction[1]
                ) % SCREEN_HEIGHT
            )

        # Добавляем координаты головы змейки в начало списка
        list.insert(self.positions, 0, (next_head_position))

        # Проверяем пересечение головы змейки с телом змейки
        if head_position in self.positions[2:]:
            self.reset()  # Сбрасываем змейку
        else:
            # Удаляем последнюю координату в списке и
            # передаем для затирки следа
            self.last = list.pop(self.positions)

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное положение"""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.next_direction = choice([UP, LEFT, RIGHT, DOWN])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object) -> None:
    """Обработка действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Главный код игры"""
    # Инициализация pg:
    pg.init()
    # Создаем экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(2)  # Исправить на SPEED
        handle_keys(snake)
        snake.move()

        # Поедание яблока змеей.
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position()
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
            list.append(snake.positions, apple.position)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
