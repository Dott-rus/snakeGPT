import pygame
import time
import random

pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Размеры экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Змейка - Счет: 0")

# Загрузка фонового изображения
background_image = pygame.image.load("background.png")

# Функция отрисовки змейки
def draw_snake(snake_block, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], snake_block, snake_block])

# Функция спавна яблока
def spawn_apple(snake_block):
    apple_x = random.randrange(0, width - snake_block, snake_block)
    apple_y = random.randrange(0, height - snake_block, snake_block)
    return apple_x, apple_y

# Основной игровой цикл
def game_loop():
    game_over = False
    game_close = False

    # Позиция и размеры змейки
    x = width // 2
    y = height // 2
    snake_block = 20
    snake_speed = 15

    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    score = 0

    # Спавн первого яблока
    apple_x, apple_y = spawn_apple(snake_block)

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            font_style = pygame.font.SysFont('Lucida Console', 20)
            game_over_text = font_style.render(
                f'''ЛОХ!  Результат: {score}   Q-Выйти C-Играть ещё раз''', True, RED
            )
            text_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))
            screen.blit(game_over_text, text_rect)

            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True
        x += x_change
        y += y_change

        # Создание поверхности для сетки
        grid_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        cell_size = 20  # Размер ячейки сетки

        # Рисование полупрозрачной сетки
        for gx in range(0, width, cell_size):
            pygame.draw.line(grid_surface, (255, 255, 255, 100), (gx, 0), (gx, height))
        for gy in range(0, height, cell_size):
            pygame.draw.line(grid_surface, (255, 255, 255, 100), (0, gy), (width, gy))

        # Наложение поверхности сетки на фоновое изображение
        screen.blit(pygame.transform.scale(background_image, (width, height)), (0, 0))
        screen.blit(grid_surface, (0, 0))

        # Отрисовка яблока
        pygame.draw.rect(screen, RED, [apple_x, apple_y, snake_block, snake_block])

        # Проверка столкновения с яблоком
        if x == apple_x and y == apple_y:
            score += 1
            length_of_snake += 1
            apple_x, apple_y = spawn_apple(snake_block)
            pygame.display.set_caption(f"Змейка - Счет: {score}")

        # Добавляем текущие координаты головы змейки в начало списка
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        # Если длина списка превышает длину змейки, удаляем лишние элементы
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Отрисовка змейки
        draw_snake(snake_block, snake_list)

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()

game_loop()
