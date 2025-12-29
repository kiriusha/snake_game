"""
Игровой движок для Змейки.
"""

import pygame
import sys
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from .snake import Snake
from .apple import Apple


class GameEngine:
    """
    Управляет игровым процессом.

    Attributes:
        width (int): Ширина игрового поля.
        height (int): Высота игрового поля.
        grid_size (int): Размер сетки.
        fps (int): Кадров в секунду.
        snake_speed (int): Скорость движения змейки.
        player_name (str): Имя игрока.
        fullscreen (bool): Режим полноэкранный или оконный.
    """

    def __init__(self, width: int = 800, height: int = 600,
                 grid_size: int = 40, fps: int = 60,
                 snake_speed: int = 10, player_name: str = "Игрок",
                 fullscreen: bool = True):
        """
        Инициализирует игровой движок.

        Args:
            width (int): Ширина поля.
            height (int): Высота поля.
            grid_size (int): Размер сетки.
            fps (int): Кадров в секунду.
            snake_speed (int): Скорость змейки.
            player_name (str): Имя игрока.
            fullscreen (bool): Режим полноэкранный.
        """
        pygame.init()

        # Получаем разрешение экрана
        self.fullscreen = fullscreen
        screen_info = pygame.display.Info()

        # Сохраняем РЕАЛЬНЫЕ размеры игрового поля из настроек
        self.original_width = width
        self.original_height = height
        self.grid_size = grid_size  # Фиксированный размер сетки 40

        # Выравниваем размеры под сетку
        self.game_width = (self.original_width // self.grid_size) * self.grid_size
        self.game_height = (self.original_height // self.grid_size) * self.grid_size

        # Разделяем экран на игровое поле и панель статистики
        self.ui_height = 120  # Высота панели статистики
        self.display_width = self.game_width
        self.display_height = self.game_height + self.ui_height

        self.fps = fps  # Фиксированная частота кадров 60
        self.snake_speed = snake_speed
        self.player_name = player_name

        # Создаем окно
        if self.fullscreen:
            self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
            self.screen_width = screen_info.current_w
            self.screen_height = screen_info.current_h
        else:
            self.screen = pygame.display.set_mode((self.display_width, self.display_height))
            self.screen_width = self.display_width
            self.screen_height = self.display_height

        pygame.display.set_caption(f'Змейка - {self.player_name}')
        self.clock = pygame.time.Clock()

        # Поверхность для отрисовки игры (с фиксированным размером ИЗ НАСТРОЕК)
        self.game_surface = pygame.Surface((self.display_width, self.display_height))

        # Загружаем шрифты
        try:
            self.font = pygame.font.Font(None, 28)
            self.big_font = pygame.font.Font(None, 42)
            self.title_font = pygame.font.Font(None, 72)
        except:
            self.font = pygame.font.SysFont('arial', 28)
            self.big_font = pygame.font.SysFont('arial', 42)
            self.title_font = pygame.font.SysFont('arial', 72)

        # Цвета игрового поля (шахматный порядок)
        self.color1 = pygame.Color('#4682B4')  # Стальной синий
        self.color2 = pygame.Color('#B0E0E6')  # Голубой порошок

        # Цвета UI
        self.ui_bg_color = pygame.Color('#2C3E50')  # Темно-синий
        self.ui_text_color = pygame.Color('#ECF0F1')  # Светло-серый
        self.ui_accent_color = pygame.Color('#3498DB')  # Голубой
        self.ui_button_color = pygame.Color('#1ABC9C')  # Бирюзовый
        self.ui_button_hover_color = pygame.Color('#16A085')  # Темный бирюзовый

        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False

        self._init_game()

    def _init_game(self) -> None:
        """
        Инициализирует игровые объекты.
        """
        # Создаем змейку в центре игрового поля (ИСПОЛЬЗУЕМ game_width и game_height)
        start_x = (self.game_width // 2) // self.grid_size * self.grid_size
        start_y = (self.game_height // 2) // self.grid_size * self.grid_size

        # Цвета змейки (зеленая гамма)
        head_color = pygame.Color('#00FF00')  # Ярко-зеленый
        body_color1 = pygame.Color('#32CD32')  # Лаймовый зеленый
        body_color2 = pygame.Color('#228B22')  # Лесной зеленый

        self.snake = Snake(
            x=start_x,
            y=start_y,
            size=self.grid_size,
            length=3,
            head_color=head_color,
            body_colors=[body_color1, body_color2]  # Чередующиеся цвета
        )

        # Создаем яблоко (ИСПОЛЬЗУЕМ game_width и game_height)
        self.apple = Apple.create_random(
            max_x=self.game_width,
            max_y=self.game_height,
            size=self.grid_size,
            grid_size=self.grid_size
        )

        # Таймер для движения змейки
        self.move_timer = 0
        self.move_delay = 1000 // self.snake_speed  # мс между движениями

    def handle_events(self) -> bool:
        """
        Обрабатывает события.

        Returns:
            bool: True если игра должна продолжаться, иначе False.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                elif event.key == pygame.K_f:  # Переключение полноэкранного режима
                    self._toggle_fullscreen()

                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self._init_game()
                        self.game_over = False
                        self.score = 0
                    else:
                        self.paused = not self.paused

                elif not self.game_over and not self.paused:
                    self.snake.change_direction(event.key)

        return True

    def _toggle_fullscreen(self):
        """Переключает полноэкранный режим."""
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            screen_info = pygame.display.Info()
            self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.display_width, self.display_height))

    def update(self, dt: float) -> None:
        """
        Обновляет игровое состояние.

        Args:
            dt (float): Время с последнего обновления в секундах.
        """
        if self.game_over or self.paused:
            return

        # Обновляем таймер движения
        self.move_timer += dt * 1000  # Преобразуем в миллисекунды

        if self.move_timer >= self.move_delay:
            self.move_timer = 0

            # Двигаем змейку
            self.snake.move()

            # Проверяем столкновение с яблоком (ИСПОЛЬЗУЕМ game_width и game_height)
            if self.snake.check_collision(self.apple):
                self.snake.grow()
                self.score += self.apple.value
                self.apple.respawn(self.game_width, self.game_height, self.grid_size)

                # Обновляем рекорд
                if self.score > self.high_score:
                    self.high_score = self.score

            # Проверяем столкновения (ИСПОЛЬЗУЕМ game_width и game_height)
            if (self.snake.check_self_collision() or
                self.snake.check_wall_collision(self.game_width, self.game_height)):
                self.game_over = True
                self._save_result()

    def _save_result(self) -> None:
        """
        Сохраняет результат игры в файл.
        """
        result = {
            'player': self.player_name,
            'score': self.score,
            'length': self.snake.get_length(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'speed': self.snake_speed,
            'field_size': f"{self.original_width}x{self.original_height}",
            'grid_size': self.grid_size
        }

        with open('results.txt', 'a', encoding='utf-8') as f:
            f.write(f"{result['timestamp']} | {result['player']} | "
                   f"Очки: {result['score']} | "
                   f"Длина: {result['length']} | "
                   f"Скорость: {result['speed']} | "
                   f"Поле: {result['field_size']} | "
                   f"Сетка: {result['grid_size']}\n")

    def draw(self) -> None:
        """
        Отрисовывает игровое поле.
        """
        # Очищаем игровую поверхность
        self.game_surface.fill((0, 0, 0))

        # Рисуем игровое поле (шахматный порядок)
        self._draw_game_board()

        # Рисуем игровые объекты
        self.apple.draw(self.game_surface)
        self.snake.draw(self.game_surface)

        # Рисуем панель статистики
        self._draw_ui_panel()

        # Рисуем сообщения поверх всего
        self._draw_messages()

        # Масштабируем и центрируем на основном экране
        self._draw_to_screen()

    def _draw_to_screen(self):
        """Рисует игровую поверхность на основном экране."""
        # Очищаем основной экран
        self.screen.fill((0, 0, 0))

        if self.fullscreen:
            # В полноэкранном режиме масштабируем всю поверхность целиком
            scale_factor = min(
                self.screen_width / self.display_width,
                self.screen_height / self.display_height
            )

            scaled_width = int(self.display_width * scale_factor)
            scaled_height = int(self.display_height * scale_factor)

            scaled_surface = pygame.transform.scale(self.game_surface, (scaled_width, scaled_height))

            # Центрируем отмасштабированную поверхность
            x_pos = (self.screen_width - scaled_width) // 2
            y_pos = (self.screen_height - scaled_height) // 2

            self.screen.blit(scaled_surface, (x_pos, y_pos))
        else:
            # В оконном режиме просто отображаем
            self.screen.blit(self.game_surface, (0, 0))

        # Обновляем экран
        pygame.display.flip()

    def _draw_game_board(self) -> None:
        """
        Рисует игровое поле в шахматном порядке.
        """
        cols = self.game_width // self.grid_size  # ИСПОЛЬЗУЕМ game_width
        rows = self.game_height // self.grid_size  # ИСПОЛЬЗУЕМ game_height

        for row in range(rows):
            for col in range(cols):
                # Определяем цвет клетки (шахматный порядок)
                if (row + col) % 2 == 0:
                    color = self.color1
                else:
                    color = self.color2

                # Рисуем клетку
                rect = pygame.Rect(
                    col * self.grid_size,
                    row * self.grid_size,
                    self.grid_size,
                    self.grid_size
                )
                pygame.draw.rect(self.game_surface, color, rect)

                # Добавляем легкую обводку
                pygame.draw.rect(self.game_surface, (40, 40, 40), rect, 1)

    def _draw_ui_panel(self) -> None:
        """
        Рисует панель статистики.
        """
        # Фон панели статистики (ИСПОЛЬЗУЕМ display_width)
        ui_rect = pygame.Rect(0, self.game_height, self.display_width, self.ui_height)
        pygame.draw.rect(self.game_surface, self.ui_bg_color, ui_rect)

        # Разделительная линия
        pygame.draw.line(
            self.game_surface, self.ui_accent_color,
            (0, self.game_height), (self.display_width, self.game_height), 3
        )

        # Текст статистики
        y_offset = self.game_height + 10

        # Имя игрока и скорость
        player_text = self.font.render(
            f'Игрок: {self.player_name}', True, self.ui_text_color
        )
        self.game_surface.blit(player_text, (20, y_offset))

        speed_text = self.font.render(
            f'Скорость: {self.snake_speed}', True, self.ui_text_color
        )
        self.game_surface.blit(speed_text, (self.display_width // 3, y_offset))

        # Размер поля (показываем РЕАЛЬНЫЕ размеры)
        field_text = self.font.render(
            f'Поле: {self.original_width}x{self.original_height}', True, self.ui_text_color
        )
        self.game_surface.blit(field_text, (2 * self.display_width // 3, y_offset))

        # Счет и рекорд
        y_offset += 40

        score_text = self.font.render(
            f'Очки: {self.score}', True, (255, 255, 100)
        )
        self.game_surface.blit(score_text, (20, y_offset))

        high_score_text = self.font.render(
            f'Рекорд: {self.high_score}', True, (255, 200, 50)
        )
        self.game_surface.blit(high_score_text, (self.display_width // 3, y_offset))

        # Длина змейки
        length_text = self.font.render(
            f'Длина: {self.snake.get_length()}', True, (100, 255, 100)
        )
        self.game_surface.blit(length_text, (2 * self.display_width // 3, y_offset))

        # Убраны подсказки по управлению

    def _draw_messages(self) -> None:
        """
        Рисует сообщения поверх игрового поля.
        """
        if self.paused:
            # Полупрозрачный фон (ИСПОЛЬЗУЕМ game_width и game_height)
            overlay = pygame.Surface((self.game_width, self.game_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Полупрозрачный черный
            self.game_surface.blit(overlay, (0, 0))

            pause_text = self.big_font.render('ПАУЗА', True, (255, 255, 0))
            text_rect = pause_text.get_rect(center=(self.game_width//2, self.game_height//2))
            self.game_surface.blit(pause_text, text_rect)

            hint_text = self.font.render(
                'Нажмите ПРОБЕЛ чтобы продолжить',
                True, (200, 200, 200)
            )
            hint_rect = hint_text.get_rect(center=(self.game_width//2, self.game_height//2 + 50))
            self.game_surface.blit(hint_text, hint_rect)

        elif self.game_over:
            # Полупрозрачный фон (ИСПОЛЬЗУЕМ game_width и game_height)
            overlay = pygame.Surface((self.game_width, self.game_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Полупрозрачный черный
            self.game_surface.blit(overlay, (0, 0))

            game_over_text = self.big_font.render('ИГРА ОКОНЧЕНА', True, (255, 50, 50))
            text_rect = game_over_text.get_rect(center=(self.game_width//2, self.game_height//2 - 50))
            self.game_surface.blit(game_over_text, text_rect)

            score_text = self.font.render(
                f'Ваш счет: {self.score} | Длина: {self.snake.get_length()}',
                True, (255, 255, 255)
            )
            score_rect = score_text.get_rect(center=(self.game_width//2, self.game_height//2))
            self.game_surface.blit(score_text, score_rect)

            restart_text = self.font.render(
                'Нажмите ПРОБЕЛ чтобы начать заново',
                True, (200, 200, 200)
            )
            restart_rect = restart_text.get_rect(center=(self.game_width//2, self.game_height//2 + 50))
            self.game_surface.blit(restart_text, restart_rect)

    def run(self) -> None:
        """
        Запускает основной игровой цикл.
        """
        running = True

        while running:
            dt = self.clock.tick(self.fps) / 1000.0

            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()


class GameLauncher:
    """
    Класс для настройки и запуска игры с меню выбора параметров.
    """

    def __init__(self):
        """Инициализирует лаунчер игры."""
        pygame.init()

        # Получаем разрешение экрана для полноэкранного режима
        screen_info = pygame.display.Info()

        # Используем 90% от размера экрана для лаунчера
        self.screen_width = int(screen_info.current_w * 0.9)
        self.screen_height = int(screen_info.current_h * 0.9)

        # Стандартные параметры
        self.config = {
            'width': 800,
            'height': 600,
            'grid_size': 40,  # Фиксированный размер сетки 40
            'fps': 60,  # Фиксированная частота кадров 60
            'snake_speed': 10,
            'player_name': 'Игрок',
            'fullscreen': True  # По умолчанию полноэкранный режим
        }

        # Оконный режим для лаунчера
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Змейка - Настройка параметров')
        self.clock = pygame.time.Clock()

        # Загружаем шрифты с адаптивными размерами
        try:
            font_size_title = min(80, self.screen_height // 12)
            font_size_normal = min(34, self.screen_height // 26)
            font_size_button = min(38, self.screen_height // 24)

            self.title_font = pygame.font.Font(None, font_size_title)
            self.font = pygame.font.Font(None, font_size_normal)
            self.button_font = pygame.font.Font(None, font_size_button)
        except:
            self.title_font = pygame.font.SysFont('arial', 80)
            self.font = pygame.font.SysFont('arial', 34)
            self.button_font = pygame.font.SysFont('arial', 38)

        # Цвета
        self.bg_color = pygame.Color('#2C3E50')
        self.text_color = pygame.Color('#ECF0F1')
        self.accent_color = pygame.Color('#3498DB')
        self.button_color = pygame.Color('#1ABC9C')
        self.button_hover_color = pygame.Color('#16A085')
        self.input_color = pygame.Color('#34495E')
        self.input_text_color = pygame.Color('#FFFFFF')

        # Текущий редактируемый параметр
        self.editing_parameter = None

        # Кнопки выбора параметров
        self.buttons = []
        self._init_buttons()

        # Ввод имени игрока
        self.player_name_input = self.config['player_name']
        self.name_input_rect = pygame.Rect(
            self.screen_width // 2 - 200,
            200,
            400,
            50
        )

        # Параметры для быстрого выбора (только три уровня сложности)
        self.presets = [
            {'name': 'ЛЕГКАЯ', 'width': 600, 'height': 400, 'speed': 8, 'color': '#27AE60'},
            {'name': 'СРЕДНЯЯ', 'width': 800, 'height': 600, 'speed': 12, 'color': '#F39C12'},
            {'name': 'СЛОЖНАЯ', 'width': 1000, 'height': 800, 'speed': 15, 'color': '#E74C3C'}
        ]

        # Кнопки предустановок
        self.preset_buttons = []
        self._init_preset_buttons()

    def _init_buttons(self):
        """Инициализирует кнопки настройки параметров."""
        button_y = 280
        button_width = min(90, self.screen_width // 15)
        button_height = min(50, self.screen_height // 18)
        spacing = min(80, self.screen_height // 12)

        # Только три параметра: ширина, высота и скорость
        # Убраны: размер сетки (фиксирован 40) и частота кадров (фиксирована 60)
        parameters = [
            ('ШИРИНА ПОЛЯ:', 'width', ['400', '600', '800', '1000', '1200', '1400']),
            ('ВЫСОТА ПОЛЯ:', 'height', ['300', '400', '600', '800', '900', '1000']),
            ('СКОРОСТЬ:', 'snake_speed', ['5', '8', '10', '12', '15', '18', '20', '25'])
        ]

        for label, param_name, options in parameters:
            label_text = self.font.render(label, True, self.text_color)
            label_rect = label_text.get_rect(topleft=(100, button_y))

            # Кнопки для каждого значения
            option_buttons = []
            x_pos = self.screen_width // 2 - 200

            for option in options:
                btn_rect = pygame.Rect(x_pos, button_y, button_width, button_height)
                option_buttons.append({
                    'rect': btn_rect,
                    'text': option,
                    'value': int(option),
                    'param': param_name
                })
                x_pos += button_width + 15

            self.buttons.append({
                'label': label_text,
                'label_rect': label_rect,
                'options': option_buttons,
                'param': param_name
            })

            button_y += spacing

    def _init_preset_buttons(self):
        """Инициализирует кнопки предустановок."""
        button_y = self.screen_height - 180
        button_width = min(220, self.screen_width // 5)
        button_height = min(60, self.screen_height // 15)
        spacing = min(40, self.screen_width // 30)

        x_start = (self.screen_width - (len(self.presets) * button_width + (len(self.presets) - 1) * spacing)) // 2

        for i, preset in enumerate(self.presets):
            btn_rect = pygame.Rect(x_start + i * (button_width + spacing), button_y, button_width, button_height)
            self.preset_buttons.append({
                'rect': btn_rect,
                'text': preset['name'],
                'preset': preset,
                'color': pygame.Color(preset['color'])
            })

    def draw(self):
        """Отрисовывает экран настройки параметров."""
        self.screen.fill(self.bg_color)

        # Фоновый градиент или узор
        self._draw_background()

        # Заголовок
        title = self.title_font.render('НАСТРОЙКА ИГРЫ "ЗМЕЙКА"', True, self.accent_color)
        title_rect = title.get_rect(center=(self.screen_width // 2, 120))
        self.screen.blit(title, title_rect)

        # Имя игрока
        name_label = self.font.render('ВАШЕ ИМЯ:', True, self.text_color)
        name_label_rect = name_label.get_rect(midright=(self.name_input_rect.left - 20, self.name_input_rect.centery))
        self.screen.blit(name_label, name_label_rect)

        # Поле ввода имени
        pygame.draw.rect(self.screen, self.input_color, self.name_input_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.accent_color if self.editing_parameter == 'name' else self.text_color,
                        self.name_input_rect, 3, border_radius=8)

        name_text = self.font.render(self.player_name_input, True, self.input_text_color)
        text_rect = name_text.get_rect(midleft=(self.name_input_rect.left + 15, self.name_input_rect.centery))
        self.screen.blit(name_text, text_rect)

        # Индикатор редактирования
        if self.editing_parameter == 'name':
            cursor_x = text_rect.right + 5
            cursor_rect = pygame.Rect(cursor_x, self.name_input_rect.top + 10, 3, self.name_input_rect.height - 20)
            pygame.draw.rect(self.screen, self.text_color, cursor_rect)

        # Отображение параметров
        for button_group in self.buttons:
            # Метка параметра
            self.screen.blit(button_group['label'], button_group['label_rect'])

            # Кнопки значений
            for option in button_group['options']:
                # Определяем цвет кнопки
                current_value = self.config[button_group['param']]
                is_selected = (current_value == option['value'])
                is_hovered = option['rect'].collidepoint(pygame.mouse.get_pos())

                color = self.accent_color if is_selected else (
                    self.button_hover_color if is_hovered else self.button_color
                )

                # Рисуем кнопку с тенью
                shadow_rect = option['rect'].copy()
                shadow_rect.x += 3
                shadow_rect.y += 3
                pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=5)

                # Основная кнопка
                pygame.draw.rect(self.screen, color, option['rect'], border_radius=5)

                # Текст на кнопке
                text = self.button_font.render(option['text'], True, self.text_color)
                text_rect = text.get_rect(center=option['rect'].center)
                self.screen.blit(text, text_rect)

        # Предустановки
        for preset_btn in self.preset_buttons:
            is_hovered = preset_btn['rect'].collidepoint(pygame.mouse.get_pos())
            color = pygame.Color('#FFFFFF') if is_hovered else preset_btn['color']

            # Тень
            shadow_rect = preset_btn['rect'].copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=8)

            # Основная кнопка
            pygame.draw.rect(self.screen, color, preset_btn['rect'], border_radius=8)

            # Обводка
            pygame.draw.rect(self.screen, self.text_color, preset_btn['rect'], 3, border_radius=8)

            # Текст
            text = self.button_font.render(preset_btn['text'], True, self.bg_color)
            text_rect = text.get_rect(center=preset_btn['rect'].center)
            self.screen.blit(text, text_rect)

            # Информация о пресете
            if is_hovered:
                preset = preset_btn['preset']
                info_text = self.font.render(
                    f"{preset['width']}x{preset['height']} | Скорость: {preset['speed']}",
                    True, self.text_color
                )
                info_rect = info_text.get_rect(midtop=(preset_btn['rect'].centerx, preset_btn['rect'].bottom + 10))
                self.screen.blit(info_text, info_rect)

        # Кнопка запуска игры
        start_btn = pygame.Rect(self.screen_width // 2 - 150, self.screen_height - 100, 300, 80)
        is_hovered = start_btn.collidepoint(pygame.mouse.get_pos())
        start_color = self.button_hover_color if is_hovered else self.button_color

        # Тень кнопки запуска
        shadow_rect = start_btn.copy()
        shadow_rect.x += 5
        shadow_rect.y += 5
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=12)

        # Основная кнопка запуска
        pygame.draw.rect(self.screen, start_color, start_btn, border_radius=12)

        # Обводка кнопки запуска
        pygame.draw.rect(self.screen, self.accent_color, start_btn, 4, border_radius=12)

        # Текст кнопки запуска
        start_text = self.title_font.render('ИГРАТЬ', True, self.text_color)
        start_rect = start_text.get_rect(center=start_btn.center)
        self.screen.blit(start_text, start_rect)

        pygame.display.flip()

    def _draw_background(self):
        """Рисует фоновый узор."""
        # Простой узор из линий
        for i in range(0, self.screen_width, 50):
            pygame.draw.line(self.screen, (40, 50, 60), (i, 0), (i, self.screen_height), 1)
        for i in range(0, self.screen_height, 50):
            pygame.draw.line(self.screen, (40, 50, 60), (0, i), (self.screen_width, i), 1)

    def handle_events(self):
        """Обрабатывает события в лаунчере."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit'

                elif self.editing_parameter == 'name':
                    if event.key == pygame.K_RETURN:
                        self.editing_parameter = None
                        self.config['player_name'] = self.player_name_input
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name_input = self.player_name_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.editing_parameter = None
                    else:
                        if len(self.player_name_input) < 20 and event.unicode.isprintable():
                            self.player_name_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    mouse_pos = event.pos

                    # Проверка поля ввода имени
                    if self.name_input_rect.collidepoint(mouse_pos):
                        self.editing_parameter = 'name'
                        return 'continue'
                    else:
                        self.editing_parameter = None

                    # Проверка кнопок параметров
                    for button_group in self.buttons:
                        for option in button_group['options']:
                            if option['rect'].collidepoint(mouse_pos):
                                self.config[option['param']] = option['value']
                                return 'continue'

                    # Проверка кнопок предустановок
                    for preset_btn in self.preset_buttons:
                        if preset_btn['rect'].collidepoint(mouse_pos):
                            preset = preset_btn['preset']
                            self.config['width'] = preset['width']
                            self.config['height'] = preset['height']
                            self.config['snake_speed'] = preset['speed']
                            # grid_size и fps остаются фиксированными
                            return 'continue'

                    # Проверка кнопки запуска игры
                    start_btn = pygame.Rect(self.screen_width // 2 - 150, self.screen_height - 100, 300, 80)
                    if start_btn.collidepoint(mouse_pos):
                        # Обновляем имя игрока из поля ввода
                        self.config['player_name'] = self.player_name_input
                        return 'start'

        return 'continue'

    def run(self) -> Dict[str, Any]:
        """
        Запускает лаунчер и возвращает настройки игры.

        Returns:
            Dict[str, Any]: Словарь с настройками игры.
        """
        running = True

        while running:
            dt = self.clock.tick(60) / 1000.0

            result = self.handle_events()

            if result == 'quit':
                pygame.quit()
                return None
            elif result == 'start':
                pygame.quit()
                return self.config

            self.draw()

        return None