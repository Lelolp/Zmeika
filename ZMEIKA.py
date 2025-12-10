import pygame
import random
from collections import deque

# ---------------------------
# Настройки игры
# ---------------------------
CELL = 32            # размер клетки в пикселях
GRID_W = 30          # ширина поля (в клетках)
GRID_H = 15          # высота поля (в клетках)
SPEED = 8            # тики в секунду

WIDTH = GRID_W
HEIGHT = GRID_H
SCREEN_W = GRID_W * CELL
SCREEN_H = GRID_H * CELL

# Цвета
BG = (20, 24, 28)
WALL = (80, 80, 90)
SNAKE = (40, 200, 80)
HEAD = (20, 160, 60)
FOOD = (230, 120, 60)
TEXT = (240, 240, 240)
PAUSE_OVERLAY = (0, 0, 0, 120)

# Направления
DIRS = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def next_position(head, direction):
    x, y = head
    dx, dy = direction
    return x + dx, y + dy


def place_food(occupied):
    """Вернуть позицию еды, не совпадающую со змеёй и не на стене."""
    candidates = [(x, y) for x in range(1, WIDTH - 1) for y in range(1, HEIGHT - 1)
                  if (x, y) not in occupied]
    if not candidates:
        return None
    return random.choice(candidates)


def draw_grid(surface):
    surface.fill(BG)
    # Рамка (стены)
    for x in range(WIDTH):
        pygame.draw.rect(surface, WALL, (x * CELL, 0, CELL, CELL))
        pygame.draw.rect(surface, WALL, (x * CELL, (HEIGHT - 1) * CELL, CELL, CELL))
    for y in range(HEIGHT):
        pygame.draw.rect(surface, WALL, (0, y * CELL, CELL, CELL))
        pygame.draw.rect(surface, WALL, ((WIDTH - 1) * CELL, y * CELL, CELL, CELL))


def draw_snake(surface, body):
    for i, (x, y) in enumerate(body):
        color = HEAD if i == 0 else SNAKE
        pygame.draw.rect(surface, color, (x * CELL, y * CELL, CELL, CELL), border_radius=6)


def draw_food(surface, pos):
    if pos is None:
        return
    x, y = pos
    pygame.draw.rect(surface, FOOD, (x * CELL + 6, y * CELL + 6, CELL - 12, CELL - 12), border_radius=6)


def draw_text(surface, text, size, x, y, center=True):
    font = pygame.font.SysFont("consolas", size)
    img = font.render(text, True, TEXT)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)


def step_game(body, direction, food):
    """Выполнить один шаг. Возвращает (новое_тело, новое_направление, новое_еда, съели, проигрыш)."""
    head = body[0]
    new_head = next_position(head, direction)
    x, y = new_head

    # Столкновение со стенами
    if x <= 0 or x >= WIDTH - 1 or y <= 0 or y >= HEIGHT - 1:
        return body, direction, food, False, True

    # Столкновение с собой
    if new_head in body:
        return body, direction, food, False, True

    ate = food is not None and new_head == food
    new_body = deque(body)
    new_body.appendleft(new_head)
    if not ate:
        new_body.pop()

    new_food = food
    if ate:
        occupied = set(new_body)
        new_food = place_food(occupied)
    return deque(new_body), direction, new_food, ate, False


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Zmeika")
    clock = pygame.time.Clock()

    # Стартовые значения
    start_len = 4
    start_x = WIDTH // 2
    start_y = HEIGHT // 2
    body = deque([(start_x - i, start_y) for i in range(start_len)])
    direction = (1, 0)
    food = place_food(set(body))

    score = 0
    paused = False
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_p and not game_over:
                    paused = not paused
                if event.key == pygame.K_r and game_over:
                    # Рестарт
                    body = deque([(start_x - i, start_y) for i in range(start_len)])
                    direction = (1, 0)
                    food = place_food(set(body))
                    score = 0
                    paused = False
                    game_over = False
                if event.key in DIRS and not paused and not game_over:
                    nd = DIRS[event.key]
                    # Запрет мгновенного разворота в себя
                    if len(body) <= 1 or (nd[0] != -direction[0] or nd[1] != -direction[1]):
                        direction = nd

        if not paused and not game_over:
            body, direction, food, ate, dead = step_game(body, direction, food)
            if ate:
                score += 1
            if dead:
                game_over = True

        # Рендер
        draw_grid(screen)
        draw_snake(screen, body)
        draw_food(screen, food)
        draw_text(screen, f"Score: {score}", 20, 8, 6, center=False)

        if paused and not game_over:
            draw_text(screen, "PAUSED (P)", 28, SCREEN_W // 2, SCREEN_H // 2)
        if game_over:
            draw_text(screen, "GAME OVER", 42, SCREEN_W // 2, SCREEN_H // 2 - 30)
            draw_text(screen, f"Score: {score}", 28, SCREEN_W // 2, SCREEN_H // 2 + 10)
            draw_text(screen, "R - restart, ESC - exit", 20, SCREEN_W // 2, SCREEN_H // 2 + 40)

        pygame.display.flip()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()
