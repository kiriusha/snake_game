"""
Класс для яблока в игре Змейка.
"""

import random
from typing import Tuple
from .base import GameObject


class Apple(GameObject):
    """
    Представляет яблоко в игре.

    Attributes:
        value (int): Количество очков за съедение.
    """

    def __init__(self, x: int, y: int, size: int = 20,
                 color: Tuple[int, int, int] = (255, 50, 50),
                 value: int = 1):
        """
        Инициализирует яблоко.

        Args:
            x (int): Координата X.
            y (int): Координата Y.
            size (int): Размер яблока.
            color (Tuple[int, int, int]): Цвет яблока.
            value (int): Количество очков.
        """
        super().__init__(x, y, size, size, color)
        self.value = value

    @classmethod
    def create_random(cls, max_x: int, max_y: int, size: int = 20,
                      grid_size: int = 20,
                      color: Tuple[int, int, int] = None,
                      value: int = 1) -> 'Apple':
        """
        Создает яблоко в случайной позиции.

        Args:
            max_x (int): Максимальная координата X.
            max_y (int): Максимальная координата Y.
            size (int): Размер яблока.
            grid_size (int): Размер сетки для выравнивания.
            color (Tuple[int, int, int]): Цвет яблока.
            value (int): Количество очков.

        Returns:
            Apple: Созданное яблоко.
        """
        if color is None:
            color = (255, 50, 50)

        cols = max_x // grid_size
        rows = max_y // grid_size
        x = random.randint(0, cols - 1) * grid_size
        y = random.randint(0, rows - 1) * grid_size
        return cls(x, y, size, color, value)

    def respawn(self, max_x: int, max_y: int, grid_size: int = 20) -> None:
        """
        Перемещает яблоко в новую случайную позицию.

        Args:
            max_x (int): Максимальная координата X.
            max_y (int): Максимальная координата Y.
            grid_size (int): Размер сетки.
        """
        cols = max_x // grid_size
        rows = max_y // grid_size
        self.x = random.randint(0, cols - 1) * grid_size
        self.y = random.randint(0, rows - 1) * grid_size