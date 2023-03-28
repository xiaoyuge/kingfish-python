import pygame
import random

# 初始化 pygame
pygame.init()

# 设置窗口尺寸
window_width = 800
window_height = 600

# 创建游戏窗口
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 颜色定义
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 155, 0)

# 定义每个块的大小
block_size = 20

# 蛇的速度
snake_speed = 20

# 蛇的初始位置和长度
snake_list = []
snake_length = 1
snake_head = [0, 0]

# 食物的初始位置
food_x = round(random.randrange(0, window_width-block_size) / 10.0) * 10.0
food_y = round(random.randrange(0, window_height-block_size) / 10.0) * 10.0

# 时钟对象，用于控制游戏速度
clock = pygame.time.Clock()

# 定义蛇的移动函数
def move_snake(snake_head, snake_list):
    x_change = 0
    y_change = 0
    # 处理键盘事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 如果用户点击了窗口的关闭按钮，退出游戏
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -block_size
                y_change = 0
            elif event.key == pygame.K_RIGHT:
                x_change = block_size
                y_change = 0
            elif event.key == pygame.K_UP:
                y_change = -block_size
                x_change = 0
            elif event.key == pygame.K_DOWN:
                y_change = block_size
                x_change = 0
    # 计算蛇头的位置
    snake_head[0] += x_change
    snake_head[1] += y_change
    # 将新的蛇头加入到蛇身列表的末尾
    snake_list.append(snake_head.copy())
    # 如果蛇身长度大于蛇的长度，则将蛇尾删除
    if len(snake_list) > snake_length:
        del snake_list[0]
    return snake_head, snake_list

# 游戏循环
game_exit = False
while not game_exit:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 如果用户点击了窗口的关闭按钮，退出游戏
            game_exit = True

    # 填充白色背景
    game_display.fill(white)

    # 画食物
    pygame.draw.rect(game_display, green, [food_x, food_y, block_size, block_size])

    # 移动蛇
    snake_head, snake_list = move_snake(snake_head, snake_list)
    # 画蛇
    for segment in snake_list:
        pygame.draw.rect(game_display, black, [segment[0], segment[1], block_size, block_size])

    # 判断是否吃到食物
    if snake_head[0] == food_x and snake_head[1] == food_y:
        # 食物位置随机
        food_x = round(random.randrange(0, window_width-block_size) / 10.0) * 10.0
        food_y = round(random.randrange(0, window_height-block_size) / 10.0) * 10.0
        # 蛇身长度加1
        snake_length += 1

    # 更新窗口
    pygame.display.update()

    # 控制游戏速度
    clock.tick(snake_speed)

# 退出游戏
pygame.quit()
quit()

