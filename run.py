import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

delay = 150
MIN_DELAY = 50
STEP = 10

snake = [(400, 300), (380, 300), (360, 300)]

direction_x = 1
direction_y = 0

# Еда
food = (
    random.randrange(0, WIDTH, CELL_SIZE),
    random.randrange(0, HEIGHT, CELL_SIZE)
)

MOVE_EVENT = pygame.USEREVENT
pygame.time.set_timer(MOVE_EVENT, delay)

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_e, pygame.K_PLUS,
                             pygame.K_EQUALS, pygame.K_KP_PLUS):
                delay = max(MIN_DELAY, delay - STEP)
                pygame.time.set_timer(MOVE_EVENT, delay)

            if event.key in (pygame.K_q, pygame.K_MINUS,
                             pygame.K_KP_MINUS):
                delay += STEP
                pygame.time.set_timer(MOVE_EVENT, delay)

            if event.key == pygame.K_UP and direction_y != 1:
                direction_x = 0
                direction_y = -1

            elif event.key == pygame.K_DOWN and direction_y != -1:
                direction_x = 0
                direction_y = 1

            elif event.key == pygame.K_LEFT and direction_x != 1:
                direction_x = -1
                direction_y = 0

            elif event.key == pygame.K_RIGHT and direction_x != -1:
                direction_x = 1
                direction_y = 0

        if event.type == MOVE_EVENT:

            head_x = snake[0][0] + direction_x * CELL_SIZE
            head_y = snake[0][1] + direction_y * CELL_SIZE

            new_head = (head_x, head_y)

            snake.insert(0, new_head)

            if new_head == food:
                food = (
                    random.randrange(0, WIDTH, CELL_SIZE),
                    random.randrange(0, HEIGHT, CELL_SIZE)
                )
            else:
                snake.pop()

            if (head_x < 0 or head_x >= WIDTH or
                head_y < 0 or head_y >= HEIGHT or
                new_head in snake[1:]):
                running = False

    screen.fill(BLACK)

    pygame.draw.rect(
        screen, WHITE,
        (food[0], food[1], CELL_SIZE, CELL_SIZE)
    )

    for part in snake:
        pygame.draw.rect(
            screen, GREEN,
            (part[0], part[1], CELL_SIZE, CELL_SIZE)
        )
 
    head_x, head_y = snake[0]

    if direction_x == 1:
        eyes = [(head_x + 14, head_y + 5),
                (head_x + 14, head_y + 14)]
        pupils = [(head_x + 16, head_y + 5),
                  (head_x + 16, head_y + 14)]

    elif direction_x == -1:
        eyes = [(head_x + 6, head_y + 5),
                (head_x + 6, head_y + 14)]
        pupils = [(head_x + 4, head_y + 5),
                  (head_x + 4, head_y + 14)]

    elif direction_y == -1:
        eyes = [(head_x + 5, head_y + 6),
                (head_x + 14, head_y + 6)]
        pupils = [(head_x + 5, head_y + 4),
                  (head_x + 14, head_y + 4)]

    else:
        eyes = [(head_x + 5, head_y + 14),
                (head_x + 14, head_y + 14)]
        pupils = [(head_x + 5, head_y + 16),
                  (head_x + 14, head_y + 16)]

    for eye in eyes:
        pygame.draw.circle(screen, WHITE, eye, 4)

    for pupil in pupils:
        pygame.draw.circle(screen, BLACK, pupil, 2)

    font = pygame.font.SysFont(None, 30)
    speed_text = font.render(
        f"Speed: {1000 // delay}",
        True, WHITE
    )
    screen.blit(speed_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
