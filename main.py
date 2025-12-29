#!/usr/bin/env python3
"""
Основной файл игры Змейка.

Этот модуль запускает игру через меню настройки параметров.
"""

import sys
import os

# Добавляем папку game в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.game_engine import GameLauncher, GameEngine


def main() -> None:
    """
    Главная функция, запускающая игру через меню настроек.
    """
    print("=" * 60)
    print("          ИГРА 'ЗМЕЙКА' - МЕНЮ НАСТРОЙКИ ПАРАМЕТРОВ")
    print("=" * 60)

    try:
        # Запускаем лаунчер для настройки параметров
        launcher = GameLauncher()
        config = launcher.run()

        if config is None:
            print("\nВыход из программы.")
            sys.exit(0)

        print("\n" + "=" * 60)
        print("ПАРАМЕТРЫ ИГРЫ УСТАНОВЛЕНЫ:")
        print(f"  Игрок: {config['player_name']}")
        print(f"  Размер поля: {config['width']}x{config['height']}")
        print(f"  Скорость змейки: {config['snake_speed']}")
        print(f"  Размер сетки: {config['grid_size']}")
        print(f"  Частота кадров: {config['fps']} FPS")
        print("=" * 60)

        print("\n" + "─" * 60)
        print("Запуск игры...")
        print("─" * 60)

        # Запускаем игру с выбранными параметрами (всегда в полноэкранном режиме)
        game = GameEngine(
            width=config['width'],
            height=config['height'],
            grid_size=config['grid_size'],
            fps=config['fps'],
            snake_speed=config['snake_speed'],
            player_name=config['player_name'],
            fullscreen=True
        )

        game.run()

        print("\n" + "=" * 60)
        print("Игра завершена. Результаты сохранены в файл 'results.txt'")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nИгра прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nОШИБКА ПРИ ЗАПУСКЕ ИГРЫ: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()