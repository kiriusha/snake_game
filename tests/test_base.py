"""
Тесты для базового класса GameObject.
"""

import unittest
import pygame
from game.base import GameObject


class TestGameObject(unittest.TestCase):
    """Тесты для класса GameObject."""

    def setUp(self):
        """Подготовка тестовой среды."""
        pygame.init()
        self.obj = GameObject(100, 150, 50, 60, (255, 0, 0))

    def test_initialization(self):
        """Тест инициализации объекта."""
        self.assertEqual(self.obj.x, 100)
        self.assertEqual(self.obj.y, 150)
        self.assertEqual(self.obj.width, 50)
        self.assertEqual(self.obj.height, 60)
        self.assertEqual(self.obj.color, (255, 0, 0))

    def test_rect_property(self):
        """Тест свойства rect."""
        rect = self.obj.rect
        self.assertIsInstance(rect, pygame.Rect)
        self.assertEqual(rect.x, 100)
        self.assertEqual(rect.y, 150)
        self.assertEqual(rect.width, 50)
        self.assertEqual(rect.height, 60)

    def test_move(self):
        """Тест перемещения объекта."""
        self.obj.move(10, -5)
        self.assertEqual(self.obj.x, 110)
        self.assertEqual(self.obj.y, 145)

    def test_check_collision(self):
        """Тест проверки столкновений."""
        other = GameObject(120, 160, 30, 40)
        self.assertTrue(self.obj.check_collision(other))

        other_far = GameObject(300, 400, 30, 40)
        self.assertFalse(self.obj.check_collision(other_far))


if __name__ == '__main__':
    unittest.main()