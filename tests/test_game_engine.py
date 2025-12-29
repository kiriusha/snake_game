"""
Тесты для игрового движка.
"""

import unittest
from unittest.mock import Mock, patch
import pygame
from game.game_engine import GameEngine


class TestGameEngine(unittest.TestCase):
    """Тесты для класса GameEngine."""

    def setUp(self):
        """Подготовка тестовой среды."""
        pygame.init = Mock()
        pygame.display = Mock()
        pygame.display.set_mode = Mock(return_value=Mock())
        pygame.display.set_caption = Mock()
        pygame.font = Mock()
        pygame.font.SysFont = Mock(return_value=Mock())

        self.engine = GameEngine(
            width=400,
            height=300,
            grid_size=20,
            fps=60,
            snake_speed=10,
            player_name="ТестовыйИгрок"
        )

        # Мокаем pygame методы
        self.engine.screen = Mock()
        self.engine.clock = Mock()
        self.engine.clock.tick = Mock(return_value=16.67)
        self.engine.font.render = Mock(return_value=Mock())
        self.engine.big_font.render = Mock(return_value=Mock())

    def test_initialization(self):
        """Тест инициализации движка."""
        self.assertEqual(self.engine.width, 400)
        self.assertEqual(self.engine.height, 300)
        self.assertEqual(self.engine.grid_size, 20)
        self.assertEqual(self.engine.fps, 60)
        self.assertEqual(self.engine.snake_speed, 10)
        self.assertEqual(self.engine.player_name, "ТестовыйИгрок")
        self.assertEqual(self.engine.score, 0)
        self.assertEqual(self.engine.high_score, 0)
        self.assertFalse(self.engine.game_over)
        self.assertFalse(self.engine.paused)

    @patch('pygame.event.get')
    def test_handle_events_quit(self, mock_event_get):
        """Тест обработки события выхода."""
        mock_event = Mock()
        mock_event.type = pygame.QUIT
        mock_event_get.return_value = [mock_event]

        result = self.engine.handle_events()
        self.assertFalse(result)

    @patch('pygame.event.get')
    def test_handle_events_pause(self, mock_event_get):
        """Тест обработки паузы."""
        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_SPACE
        mock_event_get.return_value = [mock_event]

        self.engine.handle_events()
        self.assertTrue(self.engine.paused)

        # Повторное нажатие снимает паузу
        self.engine.handle_events()
        self.assertFalse(self.engine.paused)

    def test_update_game_over(self):
        """Тест обновления при завершенной игре."""
        self.engine.game_over = True
        self.engine.update(0.016)

        # Движок не должен ничего обновлять
        self.assertTrue(self.engine.game_over)

    @patch('builtins.open')
    def test_save_result(self, mock_open):
        """Тест сохранения результата."""
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file

        self.engine.score = 150
        self.engine.snake.get_length = Mock(return_value=12)

        self.engine._save_result()

        mock_file.write.assert_called_once()
        args, _ = mock_file.write.call_args
        self.assertIn("ТестовыйИгрок", args[0])
        self.assertIn("150", args[0])
        self.assertIn("12", args[0])


if __name__ == '__main__':
    unittest.main()