#!/usr/bin/env python3
"""
Скрипт для генерации документации.
"""

import os
import shutil
import subprocess
import sys


def setup_docs():
    """Настраивает структуру документации."""

    print("=" * 60)
    print("НАСТРОЙКА ДОКУМЕНТАЦИИ")
    print("=" * 60)

    # Создаем папки
    os.makedirs('docs/source/game', exist_ok=True)
    os.makedirs('docs/source/_static', exist_ok=True)
    os.makedirs('docs/source/_templates', exist_ok=True)

    # Файлы которые нужно создать
    docs_files = {
        'docs/source/conf.py': conf_py_content(),
        'docs/source/index.rst': index_rst_content(),
        'docs/source/modules.rst': modules_rst_content(),
        'docs/source/game/game_engine.rst': module_rst_content('game_engine'),
        'docs/source/game/snake.rst': module_rst_content('snake'),
        'docs/source/game/apple.rst': module_rst_content('apple'),
        'docs/source/game/base.rst': module_rst_content('base'),
        'docs/source/game/utils.rst': module_rst_content('utils'),
    }

    # Создаем файлы
    for filepath, content in docs_files.items():
        print(f"Создаем {filepath}...")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    print("\n✓ Структура документации создана!")


def conf_py_content():
    """Возвращает содержимое conf.py."""
    return '''import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

project = 'Змейка'
copyright = '2024, Ваше имя'
author = 'Ваше имя'
release = '1.0'
language = 'ru'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
templates_path = ['_templates']
exclude_patterns = []
'''


def index_rst_content():
    """Возвращает содержимое index.rst."""
    return '''Документация игры "Змейка"
==========================

.. toctree::
   :maxdepth: 2
   :caption: Содержание:

   modules

Обзор
-----

Классическая игра "Змейка" на Python с использованием Pygame.

Установка
~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt

Запуск
~~~~~~

.. code-block:: bash

   python main.py

Структура проекта
~~~~~~~~~~~~~~~~~

.. code-block:: text

   snake_game/
   ├── main.py
   ├── game/
   │   ├── game_engine.py
   │   ├── snake.py
   │   ├── apple.py
   │   ├── base.py
   │   └── utils.py
   ├── tests/
   └── docs/

Тестирование
~~~~~~~~~~~~

.. code-block:: bash

   python -m pytest tests/ -v
'''


def modules_rst_content():
    """Возвращает содержимое modules.rst."""
    return '''Модули
======

.. toctree::
   :maxdepth: 4

   game/game_engine
   game/snake
   game/apple
   game/base
   game/utils
'''


def module_rst_content(module_name):
    """Возвращает содержимое файла документации модуля."""
    return f'''game.{module_name}
{"=" * (len(module_name) + 5)}

.. automodule:: game.{module_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__
'''


def generate_html():
    """Генерирует HTML-документацию."""

    print("\n" + "=" * 60)
    print("ГЕНЕРАЦИЯ HTML-ДОКУМЕНТАЦИИ")
    print("=" * 60)

    # Переходим в папку docs
    original_dir = os.getcwd()
    os.chdir('docs')

    try:
        # Генерируем документацию
        print("Выполняем make html...")
        result = subprocess.run(['make', 'html'],
                                capture_output=True,
                                text=True,
                                check=True)

        if result.returncode == 0:
            print("\n✓ HTML-документация успешно сгенерирована!")

            # Путь к сгенерированной документации
            html_path = os.path.abspath('build/html/index.html')
            print(f"\nФайлы находятся в: {os.path.abspath('build/html')}")
            print(f"Главная страница: {html_path}")

            # Открываем в браузере
            open_in_browser(html_path)

        else:
            print("✗ Ошибка при генерации документации")
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"✗ Ошибка: {e}")
        print("Убедитесь что Sphinx установлен:")
        print("  pip install sphinx sphinx-rtd-theme")
    except FileNotFoundError:
        print("✗ Команда 'make' не найдена")
        print("Для Windows используйте: make.bat html")
        # Пробуем использовать make.bat на Windows
        if sys.platform == 'win32':
            try:
                subprocess.run(['make.bat', 'html'], check=True)
                print("✓ Использован make.bat для Windows")
            except:
                print("✗ make.bat также не найден")
    finally:
        # Возвращаемся в исходную директорию
        os.chdir(original_dir)


def open_in_browser(filepath):
    """Открывает файл в браузере."""
    import webbrowser

    if os.path.exists(filepath):
        print(f"\nОткрываю в браузере...")
        webbrowser.open(f'file://{filepath}')
    else:
        print(f"✗ Файл не найден: {filepath}")


def main():
    """Основная функция."""

    # Проверяем наличие Sphinx
    try:
        import sphinx
        print(f"Sphinx установлен: {sphinx.__version__}")
    except ImportError:
        print("✗ Sphinx не установлен")
        print("Установите: pip install sphinx sphinx-rtd-theme")
        return

    # Спрашиваем что делать
    print("\nВыберите действие:")
    print("1. Настроить структуру документации")
    print("2. Сгенерировать HTML-документацию")
    print("3. Сделать всё")

    choice = input("\nВведите номер (1-3): ").strip()

    if choice == '1':
        setup_docs()
    elif choice == '2':
        generate_html()
    elif choice == '3':
        setup_docs()
        generate_html()
    else:
        print("Неверный выбор")


if __name__ == '__main__':
    main()