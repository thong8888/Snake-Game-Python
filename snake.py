import pygame
import random
import os
from typing import List, Tuple

# ========== KHỞI TẠO ==========
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Rắn săn mồi — Endless & Level Mode")
clock = pygame.time.Clock()

# ========== MÀU SẮC ==========
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (220, 60, 60)
GREEN = (60, 200, 60)
BLUE  = (70, 140, 220)
YELLOW= (230, 200, 40)
PURPLE= (150, 90, 200)
TEAL  = (50, 180, 170)
ORANGE= (240, 140, 60)

BG_CYCLE = [BLUE, TEAL, PURPLE, ORANGE]  # sẽ đổi theo màn

# ========== CẤU HÌNH GAME ==========
SNAKE_BLOCK = 20  # kích thước ô lưới
START_COLORSNAKE = (240, 240, 240)

DIFFICULTY_SPEED = {  # tốc độ khung hình/giây
    "easy": 10,
    "medium": 15,
    "hard": 25,
}

# Mốc điểm theo độ khó cho Level Mode
LEVELS = {
    "easy":   [10, 20, 30],
    "medium": [15, 30, 45],
    "hard":   [20, 40, 60],
}

# ========== FONT ==========
def load_font():
    # Ưu tiên file Roboto trong cùng thư mục; nếu thiếu, fallback font hệ thống có hỗ trợ tiếng Việt
    if os.path.exists("Roboto-Regular.ttf"):
        return pygame.font.Font("Roboto-Regular.ttf", 24)
    try:
        return pygame.font.SysFont("tahoma", 24)
    except:
        return pygame.font.SysFont(None, 24)

font = load_font()

# ========== HỖ TRỢ VẼ ==========
def draw_text(text, color, pos):
    surf = font.render(text, True, color)
    screen.blit(surf, pos)

def draw_snake(snake: List[Tuple[int,int]], color=START_COLORSNAKE):
    for x, y in snake:
        pygame.draw.rect(screen, color, (x, y, SNAKE_BLOCK, SNAKE_BLOCK))

def random_food():
    fx = random.randrange(0, WIDTH - SNAKE_BLOCK, SNAKE_BLOCK)
    fy = random.randrange(0, HEIGHT - SNAKE_BLOCK, SNAKE_BLOCK)
    return fx, fy

# ========== HIGH SCORE ==========
def hs_path(mode_name: str) -> str:
    return f"highscore_{mode_name}.txt"   # ví dụ: highscore_endless.txt, highscore_level.txt

def load_highscore(mode_name: str) -> int:
    path = hs_path(mode_name)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("0")
        return 0
    with open(path, "r", encoding="utf-8") as f:
        try:
            return int(f.read().strip())
        except:
            return 0

def save_highscore(mode_name: str, score: int):
    cur = load_highscore(mode_name)
    if score > cur:
        with open(hs_path(mode_name), "w", encoding="utf-8") as f:
            f.write(str(score))

# ========== NHẬN SỐ 1/2/3 ỔN ĐỊNH ==========
def number_pressed(event, n: str) -> bool:
    return (
        (hasattr(event, "unicode") and event.unicode == n) or
        (event.key == getattr(pygame, f"K_{n}")) or
        (event.key == getattr(pygame, f"K_KP{n}"))
    )

# ========== CHỌN ĐỘ KHÓ ==========
def choose_difficulty() -> str:
    while True:
        screen.fill(BLACK)
        draw_text("Chọn độ khó:", WHITE, (220, 100))
        draw_text("1. Dễ (tốc độ 10)", WHITE, (200, 160))
        draw_text("2. Trung bình (tốc độ 15)", WHITE, (200, 200))
        draw_text("3. Khó (tốc độ 25)", WHITE, (200, 240))
        draw_text("ESC: Quay lại", YELLOW, (250, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if number_pressed(event, "1"): return "easy"
                if number_pressed(event, "2"): return "medium"
                if number_pressed(event, "3"): return "hard"
                if event.key == pygame.K_ESCAPE: return ""  # hủy lựa chọn

# ========== GAME LOOP: VÔ TẬN ==========
def game_endless(difficulty: str):
    mode_name = "endless"
    bg = BLUE
    speed = DIFFICULTY_SPEED[difficulty]
    high = load_highscore(mode_name)

    x = WIDTH // 2
    y = HEIGHT // 2
    dx, dy = 0, 0

    snake = [(x, y)]
    length = 1
    food = random_food()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:  dx, dy = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy =  SNAKE_BLOCK, 0
                elif event.key == pygame.K_UP and dy == 0:   dx, dy = 0, -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0,  SNAKE_BLOCK
                elif event.key == pygame.K_p:  # tạm dừng
                    pause_screen()

        x += dx; y += dy
        # va tường
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            break

        # cập nhật rắn
        snake.append((x, y))
        if len(snake) > length:
            snake.pop(0)

        # cắn trúng mình
        if (x, y) in snake[:-1]:
            break

        # ăn mồi
        if (x, y) == food:
            length += 1
            food = random_food()

        # vẽ
        screen.fill(bg)
        pygame.draw.rect(screen, RED, (*food, SNAKE_BLOCK, SNAKE_BLOCK))
        draw_snake(snake)
        score = length - 1
        draw_text(f"Điểm: {score}", WHITE, (10, 10))
        draw_text(f"High (Vô tận): {high}", YELLOW, (380, 10))
        pygame.display.flip()
        clock.tick(speed)

    # kết thúc
    score = length - 1
    save_highscore(mode_name, score)
    game_over_screen(score, load_highscore(mode_name), again_callback=lambda: game_endless(difficulty))

# ========== GAME LOOP: THEO MÀN ==========
def game_level(difficulty: str):
    mode_name = "level"
    thresholds = LEVELS[difficulty][:]
    current_level = 0
    bg_index = 0
    bg = BG_CYCLE[bg_index % len(BG_CYCLE)]
    base_speed = DIFFICULTY_SPEED[difficulty]
    speed = base_speed
    high = load_highscore(mode_name)

    x = WIDTH // 2
    y = HEIGHT // 2
    dx, dy = 0, 0

    snake = [(x, y)]
    length = 1
    food = random_food()

    running = True
    win = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:  dx, dy = -SNAKE_BLOCK, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy =  SNAKE_BLOCK, 0
                elif event.key == pygame.K_UP and dy == 0:   dx, dy = 0, -SNAKE_BLOCK
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0,  SNAKE_BLOCK
                elif event.key == pygame.K_p:
                    pause_screen()

        x += dx; y += dy
        # va tường
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            break

        # cập nhật rắn
        snake.append((x, y))
        if len(snake) > length:
            snake.pop(0)

        # cắn trúng mình
        if (x, y) in snake[:-1]:
            break

        # ăn mồi
        if (x, y) == food:
            length += 1
            food = random_food()

        score = length - 1

        # kiểm tra qua màn
        if current_level < len(thresholds) and score >= thresholds[current_level]:
            current_level += 1
            if current_level == len(thresholds):
                win = True
                running = False
            else:
                # tăng tốc & đổi nền
                speed += 5
                bg_index += 1
                bg = BG_CYCLE[bg_index % len(BG_CYCLE)]

        # vẽ
        screen.fill(bg)
        pygame.draw.rect(screen, RED, (*food, SNAKE_BLOCK, SNAKE_BLOCK))
        draw_snake(snake)
        draw_text(f"Điểm: {score}", WHITE, (10, 10))
        target = thresholds[-1]
        draw_text(f"Mục tiêu: {target}", YELLOW, (10, 40))
        draw_text(f"Level: {current_level+1}/{len(thresholds)}", WHITE, (10, 70))
        draw_text(f"High (Theo màn): {high}", WHITE, (380, 10))
        pygame.display.flip()
        clock.tick(speed)

    score = length - 1
    save_highscore(mode_name, score)

    if win:
        win_screen(score, load_highscore(mode_name), again_callback=lambda: game_level(difficulty))
    else:
        game_over_screen(score, load_highscore(mode_name), again_callback=lambda: game_level(difficulty))

# ========== MÀN HÌNH TẠM DỪNG / THẮNG / THUA ==========
def pause_screen():
    paused = True
    while paused:
        screen.fill(BLACK)
        draw_text("⏸ Đang tạm dừng", WHITE, (230, 160))
        draw_text("Nhấn P để tiếp tục | ESC để về menu", YELLOW, (130, 210))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    return_to_menu()

def game_over_screen(score, high, again_callback):
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_text("💀 Bạn thua!", RED, (260, 140))
        draw_text(f"Điểm của bạn: {score}", WHITE, (230, 180))
        draw_text(f"Kỷ lục: {high}", GREEN, (270, 220))
        draw_text("C: Chơi lại  |  M: Menu  |  Q: Thoát", YELLOW, (150, 270))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: waiting = False; again_callback()
                elif event.key == pygame.K_m: waiting = False; return_to_menu()
                elif event.key == pygame.K_q: pygame.quit(); raise SystemExit

def win_screen(score, high, again_callback):
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_text("🎉 Bạn đã hoàn thành các màn!", GREEN, (150, 140))
        draw_text(f"Điểm của bạn: {score}", WHITE, (230, 180))
        draw_text(f"Kỷ lục: {high}", YELLOW, (270, 220))
        draw_text("C: Chơi lại  |  M: Menu  |  Q: Thoát", YELLOW, (150, 270))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: waiting = False; again_callback()
                elif event.key == pygame.K_m: waiting = False; return_to_menu()
                elif event.key == pygame.K_q: pygame.quit(); raise SystemExit

# ========== MENU & ĐIỀU HƯỚNG ==========
def show_highscores():
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_text(f"🎯 Kỷ lục Vô tận: {load_highscore('endless')}", WHITE, (180, 170))
        draw_text(f"🎯 Kỷ lục Theo màn: {load_highscore('level')}", WHITE, (160, 210))
        draw_text("Nhấn phím bất kỳ để quay lại", YELLOW, (170, 260))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN: waiting = False

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("🐍 Rắn săn mồi — Chọn chế độ", GREEN, (150, 90))
        draw_text("1. Vô tận (Endless)", WHITE, (200, 160))
        draw_text("2. Theo màn (Level Mode)", WHITE, (200, 200))
        draw_text("3. Xem kỷ lục", WHITE, (200, 240))
        draw_text("4. Thoát", WHITE, (200, 280))
        draw_text("Mẹo: P = Tạm dừng, Mũi tên = Di chuyển", YELLOW, (150, 330))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if number_pressed(event, "1"):
                    diff = choose_difficulty()
                    if diff: game_endless(diff)
                elif number_pressed(event, "2"):
                    diff = choose_difficulty()
                    if diff: game_level(diff)
                elif number_pressed(event, "3"):
                    show_highscores()
                elif number_pressed(event, "4") or event.key == pygame.K_ESCAPE:
                    pygame.quit(); raise SystemExit

def return_to_menu():
    main_menu()

# ========== CHẠY ==========
if __name__ == "__main__":
    main_menu()
