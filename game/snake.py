"""
Класс для змейки в игре.
"""

from typing import List, Tuple
import pygame
from .base import GameObject


class Snake(GameObject):
    """
    Представляет змейку в игре.

    Attributes:
        body (List[GameObject]): Сегменты тела змейки.
        direction (Tuple[int, int]): Текущее направление движения.
        next_direction (Tuple[int, int]): Следующее направление.
        grow_pending (int): Количество сегментов для добавления.
        body_colors (List[Tuple[int, int, int]]): Цвета для чередования.
    """

    DIRECTIONS = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_w: (0, -1),
        pygame.K_s: (0, 1),
        pygame.K_a: (-1, 0),
        pygame.K_d: (1, 0)
    }

    def __init__(self, x: int, y: int, size: int = 20,
                 length: int = 3,
                 head_color: Tuple[int, int, int] = (50, 255, 50),
                 body_colors: List[Tuple[int, int, int]] = None):
        """
        Инициализирует змейку.

        Args:
            x (int): Начальная координата X головы.
            y (int): Начальная координата Y головы.
            size (int): Размер сегмента.
            length (int): Начальная длина.
            head_color (Tuple[int, int, int]): Цвет головы.
            body_colors (List[Tuple[int, int, int]]): Цвета для чередования.
        """
        super().__init__(x, y, size, size, head_color)

        # Цвета тела
        if body_colors is None:
            body_colors = [(100, 200, 100), (50, 180, 50)]
        self.body_colors = body_colors

        self.direction = (1, 0)  # Начальное направление вправо
        self.next_direction = self.direction
        self.grow_pending = 0

        # Создаем тело змейки
        self.body: List[GameObject] = []
        for i in range(1, length):
            # Чередуем цвета для сегментов
            color_index = (i - 1) % len(self.body_colors)
            segment_color = self.body_colors[color_index]

            segment = GameObject(x - i * size, y, size, size, segment_color)
            self.body.append(segment)

    def change_direction(self, key: int) -> bool:
        """
        Изменяет направление движения.

        Args:
            key (int): Код клавиши.

        Returns:
            bool: True если направление изменено, иначе False.
        """
        if key in self.DIRECTIONS:
            new_dir = self.DIRECTIONS[key]
            # Не позволяем развернуться на 180 градусов
            if (new_dir[0] != -self.direction[0] or
                new_dir[1] != -self.direction[1]):
                self.next_direction = new_dir
                return True
        return False

    def move(self) -> None:
        """
        Перемещает змейку на один шаг.
        """
        self.direction = self.next_direction

        # Перемещаем тело
        if self.body:
            # Сдвигаем все сегменты тела
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i].x = self.body[i-1].x
                self.body[i].y = self.body[i-1].y

            # Первый сегмент тела занимает позицию головы
            self.body[0].x = self.x
            self.body[0].y = self.y

        # Перемещаем голову
        dx = self.direction[0] * self.width
        dy = self.direction[1] * self.height
        super().move(dx, dy)

        # Добавляем новые сегменты если нужно
        if self.grow_pending > 0:
            self._grow()
            self.grow_pending -= 1

    def _grow(self) -> None:
        """
        Добавляет новый сегмент к телу.
        """
        if self.body:
            last_segment = self.body[-1]
        else:
            last_segment = self

        # Чередуем цвета для нового сегмента
        color_index = len(self.body) % len(self.body_colors)
        new_color = self.body_colors[color_index]

        new_segment = GameObject(
            last_segment.x, last_segment.y,
            self.width, self.height,
            new_color
        )
        self.body.append(new_segment)

    def grow(self, amount: int = 1) -> None:
        """
        Запланировать рост змейки.

        Args:
            amount (int): Количество сегментов для добавления.
        """
        self.grow_pending += amount

    def check_self_collision(self) -> bool:
        """
        Проверяет столкновение головы с телом.

        Returns:
            bool: True если произошло столкновение, иначе False.
        """
        for segment in self.body:
            if self.check_collision(segment):
                return True
        return False

    def check_wall_collision(self, max_x: int, max_y: int) -> bool:
        """
        Проверяет столкновение со стенами.

        Args:
            max_x (int): Ширина поля.
            max_y (int): Высота поля.

        Returns:
            bool: True если произошло столкновение, иначе False.
        """
        return (self.x < 0 or self.x >= max_x or
                self.y < 0 or self.y >= max_y)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовывает всю змейку.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        # Отрисовываем тело с обводкой
        for i, segment in enumerate(self.body):
            # Основной прямоугольник
            segment.draw(surface)

            # Обводка сегмента
            pygame.draw.rect(
                surface,
                (0, 0, 0),  # Черная обводка
                segment.rect,
                1  # Толщина обводки
            )

        # Отрисовываем голову с более толстой обводкой
        head_rect = self.rect

        # Основной цвет головы
        pygame.draw.rect(surface, self.color, head_rect)

        # Толстая обводка для головы
        pygame.draw.rect(
            surface,
            (0, 0, 0),  # Черная обводка
            head_rect,
            2  # Более толстая обводка
        )

        # Глаза змейки
        eye_size = self.width // 5
        eye_offset = self.width // 4

        # Расположение глаз в зависимости от направления
        if self.direction == (1, 0):  # Вправо
            left_eye = (head_rect.right - eye_offset, head_rect.top + eye_offset)
            right_eye = (head_rect.right - eye_offset, head_rect.bottom - eye_offset)
        elif self.direction == (-1, 0):  # Влево
            left_eye = (head_rect.left + eye_offset, head_rect.top + eye_offset)
            right_eye = (head_rect.left + eye_offset, head_rect.bottom - eye_offset)
        elif self.direction == (0, 1):  # Вниз
            left_eye = (head_rect.left + eye_offset, head_rect.bottom - eye_offset)
            right_eye = (head_rect.right - eye_offset, head_rect.bottom - eye_offset)
        else:  # Вверх
            left_eye = (head_rect.left + eye_offset, head_rect.top + eye_offset)
            right_eye = (head_rect.right - eye_offset, head_rect.top + eye_offset)

        # Рисуем глаза
        pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_size)
        pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_size)

    def get_length(self) -> int:
        """
        Возвращает текущую длину змейки.

        Returns:
            int: Длина змейки (голова + тело).
        """
        return 1 + len(self.body)