"""
Вспомогательные функции для игры.
"""

import argparse
from typing import Dict, Any


def parse_arguments() -> Dict[str, Any]:
    """
    Парсит аргументы командной строки (альтернативный способ запуска).

    Returns:
        Dict[str, Any]: Словарь с аргументами.
    """
    parser = argparse.ArgumentParser(
        description='Игра Змейка',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Примеры использования:\n'
               '  python main.py --прямой-запуск --имя Вася --скорость 15 --ширина 800 --высота 600\n'
               '  python main.py --прямой-запуск --сложная\n'
    )

    parser.add_argument(
        '--прямой-запуск', '--direct',
        dest='direct_launch',
        action='store_true',
        help='Прямой запуск без меню (используйте аргументы ниже)'
    )

    parser.add_argument(
        '--имя', '--player',
        dest='player_name',
        type=str,
        default='Игрок',
        help='Имя игрока (по умолчанию: Игрок)'
    )

    parser.add_argument(
        '--скорость', '--speed',
        dest='snake_speed',
        type=int,
        default=10,
        choices=range(5, 31),
        help='Скорость змейки (5-30, по умолчанию: 10)'
    )

    parser.add_argument(
        '--ширина', '--width',
        dest='width',
        type=int,
        default=800,
        choices=range(400, 2001),
        help='Ширина игрового поля (400-2000, по умолчанию: 800)'
    )

    parser.add_argument(
        '--высота', '--height',
        dest='height',
        type=int,
        default=600,
        choices=range(300, 1501),
        help='Высота игрового поля (300-1500, по умолчанию: 600)'
    )


    args = parser.parse_args()

    return {
        'player_name': args.player_name,
        'snake_speed': args.snake_speed,
        'width': args.width,
        'height': args.height,
        'grid_size': 40,
        'fps': 60,
        'direct_launch': args.direct_launch
    }