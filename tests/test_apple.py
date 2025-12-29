"""
Тесты для класса Apple.
"""

import unittest
from unittest.mock import patch
from game.apple import Apple


class TestApple(unittest.TestCase):
    """Тесты для класса Apple."""

    def test_initialization(self):
        """Тест инициализации яблока."""
        apple = Apple(100, 150, size=25, value=5)

        self.assertEqual(apple.x, 100)
        self.assertEqual(apple.y, 150)
        self.assertEqual(apple.width, 25)
        self.assertEqual(apple.height, 25)
        self.assertEqual(apple.value, 5)

    @patch('random.randint')
    def test_create_random(self, mock_randint):
        """Тест создания случайного яблока."""
        mock_randint.side_effect = [2, 3]  # x=2*20=40, y=3*20=60

        apple = Apple.create_random(
            max_x=800,
            max_y=600,
            size=20,
            grid_size=20,
            value=3
        )

        self.assertEqual(apple.x, 40)
        self.assertEqual(apple.y, 60)
        self.assertEqual(apple.width, 20)
        self.assertEqual(apple.height, 20)
        self.assertEqual(apple.value, 3)
        self.assertEqual(mock_randint.call_count, 2)

    @patch('random.randint')
    def test_respawn(self, mock_randint):
        """Тест перемещения яблока."""
        mock_randint.side_effect = [4, 5]  # x=4*20=80, y=5*20=100

        apple = Apple(0, 0, size=20)
        apple.respawn(800, 600, 20)

        self.assertEqual(apple.x, 80)
        self.assertEqual(apple.y, 100)
        self.assertEqual(mock_randint.call_count, 2)


if __name__ == '__main__':
    unittest.main()