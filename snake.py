import pygame
import random
import os
import sys

# ===============================
# Cấu hình
# ===============================
WIDTH, HEIGHT = 600, 400
BLOCK = 20
FPS = 10
FONT_NAME = "consolas"

# Mốc điểm để qua màn theo độ khó
LEVELS = {
    "easy": [10, 20, 30],
    "medium": [15, 30, 45],
    "hard": [20, 40, 60]
}

# File lưu high score
HS_FILE = "highscore.txt"

# ===============================
# Hàm hỗ trợ
# ===============================
def load_highscore():
    if os.path.exists(HS_FILE):
        with open(HS_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def save_highscore(score):
    hs = load_highscore()
    if score > hs:
        with open(HS_FILE, "w") as f:
            f.write(str(score))

def draw_text(surf, text, size, x, y, color=(255,255,255)):
    font = pygame.font.SysFont(FONT_NAME, size)
    label = font.render(text, True, color)
    rect = label.get_rect()
    rect.center = (x, y)
    surf.blit(label, rect)

# ===============================
# Hàm chính game
# ===============================
def game_loop(mode="endless", difficulty="easy"):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐍 Snake Game Python")

    clock = pygame.time.Clock()
    snake = [(100, 50), (80, 50), (60, 50)]
    direction = (BLOCK, 0)
    food = (random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK))
    score = 0
    highscore = load_highscore()

    # Biến cho level mode
    level_index = 0
    bg_color = (0, 0, 0)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highscore(score)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, BLOCK):
                    direction = (0, -BLOCK)
                elif event.key == pygame.K_DOWN and direction != (0, -BLOCK):
                    direction = (0, BLOCK)
                elif event.key == pygame.K_LEFT and direction != (BLOCK, 0):
                    direction = (-BLOCK, 0)
                elif event.key == pygame.K_RIGHT and direction != (-BLOCK, 0):
                    direction = (BLOCK, 0)

        # Tính vị trí mới
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        # Ăn mồi
        if head == food:
            score += 1
            food = (random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK))
        else:
            snake.pop()

        # Kiểm tra va chạm
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:]):
            save_highscore(score)
            return score

        # Qua màn nếu chơi level
        if mode == "level":
            goals = LEVELS[difficulty]
            if level_index < len(goals) and score >= goals[level_index]:
                level_index += 1
                if level_index >= len(goals):
                    # Thắng game
                    screen.fill((0, 128, 0))
                    draw_text(screen, "🎉 Bạn đã thắng!", 40, WIDTH//2, HEIGHT//2, (255,255,0))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    save_highscore(score)
                    return score
                else:
                    # Tăng tốc & đổi màu nền
                    FPS += 2
                    bg_color = (random.randint(50,255), random.randint(50,255), random.randint(50,255))

        # Vẽ màn hình
        screen.fill(bg_color)
        for s in snake:
            pygame.draw.rect(screen, (0,255,0), (s[0], s[1], BLOCK, BLOCK))
        pygame.draw.rect(screen, (255,0,0), (food[0], food[1], BLOCK, BLOCK))
        draw_text(screen, f"Score: {score}", 20, 50, 10)
        draw_text(screen, f"High: {highscore}", 20, WIDTH-60, 10)
        pygame.display.flip()

# ===============================
# Menu chọn
# ===============================
def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐍 Snake Game Python")

    while True:
        screen.fill((0,0,50))
        draw_text(screen, "🐍 Snake Game", 40, WIDTH//2, HEIGHT//4)
        draw_text(screen, "1 - Chế độ Vô tận", 25, WIDTH//2, HEIGHT//2 - 30)
        draw_text(screen, "2 - Chế độ Theo màn", 25, WIDTH//2, HEIGHT//2)
        draw_text(screen, "3 - Thoát", 25, WIDTH//2, HEIGHT//2 + 30)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty_menu("endless")
                elif event.key == pygame.K_2:
                    difficulty_menu("level")
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def difficulty_menu(mode):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    while True:
        screen.fill((50,0,0))
        draw_text(screen, "Chọn độ khó", 35, WIDTH//2, HEIGHT//4)
        draw_text(screen, "1 - Dễ", 25, WIDTH//2, HEIGHT//2 - 30)
        draw_text(screen, "2 - Trung bình", 25, WIDTH//2, HEIGHT//2)
        draw_text(screen, "3 - Khó", 25, WIDTH//2, HEIGHT//2 + 30)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop(mode, "easy")
                    return
                elif event.key == pygame.K_2:
                    game_loop(mode, "medium")
                    return
                elif event.key == pygame.K_3:
                    game_loop(mode, "hard")
                    return

# ===============================
# Chạy game
# ===============================
if __name__ == "__main__":
    pygame.init()
    main_menu()
# ===============================