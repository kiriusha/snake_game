Документация игры "Змейка"
==========================

Обзор
-----

Простая реализация классической игры "Змейка" на Python с использованием Pygame.

Установка
---------

1. Установите зависимости:

.. code-block:: bash

    pip install -r requirements.txt

2. Запустите игру:

.. code-block:: bash

    python main.py --имя Вася --скорость 12


Структура проекта
-----------------

.. code-block:: text

    snake_game/
    ├── main.py              # Главный файл
    ├── game/                # Пакет с игровой логикой
    │   ├── base.py          # Базовый класс GameObject
    │   ├── snake.py         # Класс Snake
    │   ├── apple.py         # Класс Apple
    │   ├── game_engine.py   # Игровой движок
    │   └── utils.py         # Утилиты
    ├── tests/               # Тесты
    └── docs/                # Документация

Тестирование
------------

Запуск тестов:

.. code-block:: bash

    python -m pytest tests/
    python -m unittest discover tests