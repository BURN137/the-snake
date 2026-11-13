from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480  # Размер поля
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Центр поля
GRID_SIZE = 20  # Размер сетки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Ширина поля в сетках
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # Высота поля сетках


# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Направления при нажатии кнопки на клавиатуре
# (текущее направление, event.key): нажатая_кнопка
DIRECTIONS = {
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

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
            position: tuple[int, int] = SCREEN_CENTER,
            body_color: tuple[int, int, int] | None = None
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Отрисовка базового игрового объекта"""

    def draw_cell(
            self,
            position: tuple[int, int],
            color: tuple[int, int, int] | None = None
    ) -> None:
        """Отрисовка базовой игровой ячейки"""
        body_color = color if color is not None else self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        if body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Описываем класс "Яблоко"."""

    def __init__(
            self,
            position: list[tuple[int, int]] | None = None,
            body_color: tuple[int, int, int] = APPLE_COLOR,
            occupied_cells: list[tuple[int, int]] = [SCREEN_CENTER]
    ) -> None:
        super().__init__(position, body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(
            self,
            occupied_cells: list[tuple[int, int]]
    ) -> None:
        """Генератор координат яблока вне змейки"""
        while True:
            apple_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

            # Проверяем, чтобы яблоко не создалось на змейке
            if apple_position not in occupied_cells:
                self.position = apple_position
                break

    def draw(self) -> None:
        """Отрисовка яблока на экране"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Описываем класс "Змея"."""

    def __init__(
            self,
            position: tuple[int, int] = SCREEN_CENTER,
            body_color: tuple[int, int, int] = SNAKE_COLOR
    ) -> None:
        super().__init__(position, body_color)
        self.reset()
        self.direction = RIGHT  # При первом запуске всегда двигаемся вправо

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        handle_keys(self)

    def move(self) -> None:
        """
        Обновляет позицию змейки,
        добавляя новую голову в начало списка и
        удаляя последний элемент, если длина змейки не увеличилась.
        """
        head_position_x, head_position_y = self.get_head_position()
        direction_x, direction_y = self.direction
        # Направление движения змейки в зависимости
        # от нажатой кнопки пользователем.
        next_head_position = (
            (
                head_position_x + GRID_SIZE * direction_x
            ) % SCREEN_WIDTH,
            (
                head_position_y + GRID_SIZE * direction_y
            ) % SCREEN_HEIGHT
        )

        # Добавляем координаты головы змейки в начало списка
        list.insert(self.positions, 0, (next_head_position))

    def draw(self) -> None:
        """Отрисовывает змейку на экране, затирая след."""
        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def grow(self) -> None:
        """Увеличивает длину змейки."""
        if self.last:
            list.append(self.positions, self.last)
            self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное положение"""
        self.positions = [self.position]
        self.direction = choice([UP, LEFT, RIGHT, DOWN])
        self.last = None


def handle_keys(game_object) -> None:
    """Обработка действий пользователя"""
    for event in pg.event.get():
        if (
            event.type == pg.QUIT
            or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
        ):
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            game_object.direction = DIRECTIONS.get(
                (game_object.direction, event.key),
                game_object.direction
            )


def main() -> None:
    """Главный код игры"""
    # Инициализация pygame:
    pg.init()
    # Создаем экземпляры классов.

    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)
    while True:
        clock.tick(2)  # Исправить на SPEED
        snake.update_direction()
        snake.move()

        # Поедание яблока змейкой.
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        # Проверяем пересечение головы змейки с телом змейки
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()  # Сбрасываем змейку
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            # Удаляем последнюю координату в списке и
            # передаем для затирки следа
            snake.last = list.pop(snake.positions)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
