"""
Тесты для класса Snake.
"""

import unittest
import pygame
from game.snake import Snake


class TestSnake(unittest.TestCase):
    """Тесты для класса Snake."""

    def setUp(self):
        """Подготовка тестовой среды."""
        pygame.init()
        self.snake = Snake(100, 100, size=20, length=3)

    def test_initialization(self):
        """Тест инициализации змейки."""
        self.assertEqual(self.snake.x, 100)
        self.assertEqual(self.snake.y, 100)
        self.assertEqual(self.snake.width, 20)
        self.assertEqual(self.snake.height, 20)
        self.assertEqual(self.snake.direction, (1, 0))
        self.assertEqual(len(self.snake.body), 2)  # Два сегмента тела

    def test_change_direction(self):
        """Тест изменения направления."""
        # Движение вправо по умолчанию
        self.assertTrue(self.snake.change_direction(pygame.K_UP))
        self.assertEqual(self.snake.next_direction, (0, -1))

        # Нельзя развернуться на 180 градусов
        self.snake.direction = (1, 0)
        self.assertFalse(self.snake.change_direction(pygame.K_LEFT))
        self.assertEqual(self.snake.next_direction, (0, -1))  # Осталось предыдущее

    def test_move(self):
        """Тест движения змейки."""
        initial_head_x = self.snake.x
        initial_head_y = self.snake.y

        self.snake.move()

        # Проверяем движение головы
        self.assertEqual(self.snake.x, initial_head_x + 20)  # dx=1, size=20
        self.assertEqual(self.snake.y, initial_head_y)

        # Проверяем движение тела
        self.assertEqual(self.snake.body[0].x, initial_head_x)
        self.assertEqual(self.snake.body[0].y, initial_head_y)

    def test_grow(self):
        """Тест роста змейки."""
        initial_length = len(self.snake.body)

        self.snake.grow(2)
        self.snake.move()  # Первое движение добавляет сегмент

        self.assertEqual(len(self.snake.body), initial_length + 1)
        self.assertEqual(self.snake.grow_pending, 1)

    def test_check_self_collision(self):
        """Тест проверки столкновения с собой."""
        # Новая змейка не должна сталкиваться сама с собой
        self.assertFalse(self.snake.check_self_collision())


if __name__ == '__main__':
    unittest.main()