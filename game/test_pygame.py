import pygame
import sys

# 初始化 pygame
pygame.init()

# 设置窗口尺寸
window_width = 800
window_height = 600

# 创建游戏窗口
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 游戏循环
game_exit = False
while not game_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 处理关闭窗口事件
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # 处理按键按下事件
            if event.key == pygame.K_SPACE:
                # 处理空格键按下事件
                print("正确响应空格事件")
            elif event.key == pygame.K_LEFT:
                # 处理向左键按下事件
                print("正确响应向左键事件")    
            elif event.key == pygame.K_RIGHT:
                # 处理向右键按下事件
                print("正确响应向右键事件")     
            elif event.key == pygame.K_UP:
                # 处理向上键按下事件
                print("正确响应向上键事件") 
            elif event.key == pygame.K_DOWN:
                # 处理向下键按下事件
                print("正确响应向下键事件") 
# 退出游戏
pygame.quit()
quit()