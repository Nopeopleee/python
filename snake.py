import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 視窗尺寸
width = 600
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("貪食蛇")

# 顏色定義
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# 蛇的初始位置和大小
snake_block_size = 20
snake_speed = 15

# 載入字體
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font_style = pygame.font.SysFont("SimHei", 35)  # 將字體改為 SimHei


def display_score(score):
    """顯示目前得分"""
    score_text = score_font_style.render("得分: " + str(score), True, blue)
    screen.blit(score_text, [0, 0])


def draw_snake(snake_block_size, snake_list):
    """繪製蛇"""
    for x in snake_list:
        pygame.draw.rect(
            screen, green, [x[0], x[1], snake_block_size, snake_block_size]
        )


def message(msg, color):
    """顯示訊息在畫面中央"""
    text_surface = font_style.render(msg, True, color)
    text_rect = text_surface.get_rect(center=(width / 2, height / 2))
    screen.blit(text_surface, text_rect)


def game_loop():
    """遊戲主迴圈"""
    game_over = False
    game_close = False

    # 蛇的初始位置
    x = width / 2
    y = height / 2

    # 蛇的位置變化
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    # 隨機生成食物位置
    food_x = round(random.randrange(0, width - snake_block_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block_size) / 10.0) * 10.0

    # 遊戲速度控制
    clock = pygame.time.Clock()

    score = 0  # 初始化分數
    while not game_over:

        while game_close:
            screen.fill(white)
            message("你輸了！按C-繼續 或 Q-離開", red)
            display_score(score)  # 顯示最終得分
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_loop()  # 重新開始遊戲
                    elif event.key == pygame.K_q:
                        game_over = True
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block_size
                    x_change = 0

        # 邊界檢查
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(white)
        pygame.draw.rect(
            screen, red, [food_x, food_y, snake_block_size, snake_block_size]
        )
        snake_head = [x, y]  # 將 x 和 y 放入一個列表中
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # 檢查是否咬到自己
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_block_size, snake_list)
        display_score(score)  # 顯示目前得分
        pygame.display.update()

        # 吃到食物
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - snake_block_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block_size) / 10.0) * 10.0
            snake_length += 1
            score += 10  # 更新分數

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()


game_loop()
