"""
Базовый класс для игровых объектов.
"""

import pygame
from typing import Tuple


class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Attributes:
        x (int): Координата X левого верхнего угла.
        y (int): Координата Y левого верхнего угла.
        width (int): Ширина объекта.
        height (int): Высота объекта.
        color (Tuple[int, int, int]): Цвет объекта в формате RGB.
    """

    def __init__(self, x: int, y: int, width: int, height: int,
                 color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Инициализирует игровой объект.

        Args:
            x (int): Координата X.
            y (int): Координата Y.
            width (int): Ширина.
            height (int): Высота.
            color (Tuple[int, int, int]): Цвет в формате RGB.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    @property
    def rect(self) -> pygame.Rect:
        """
        Возвращает прямоугольник Pygame, представляющий объект.

        Returns:
            pygame.Rect: Прямоугольник объекта.
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Отрисовывает объект на поверхности.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, dx: int, dy: int) -> None:
        """
        Перемещает объект на заданное смещение.

        Args:
            dx (int): Смещение по оси X.
            dy (int): Смещение по оси Y.
        """
        self.x += dx
        self.y += dy

    def check_collision(self, other: 'GameObject') -> bool:
        """
        Проверяет столкновение с другим объектом.

        Args:
            other (GameObject): Другой игровой объект.

        Returns:
            bool: True если объекты пересекаются, иначе False.
        """
        return self.rect.colliderect(other.rect)