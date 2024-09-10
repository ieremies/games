#!/usr/bin/env python3
import socket
import pickle
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
FPS = 60

# Rectangles for paddles and ball
left_paddle = pygame.Rect(
    30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
)
right_paddle = pygame.Rect(
    WIDTH - 30 - PADDLE_WIDTH,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)
ball = pygame.Rect(
    WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE
)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Multiplayer")

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))
# receive side
my_side = pickle.loads(client.recv(1024))["side"]
print(my_side)


def draw_objects(game_state):
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw score
    font = pygame.font.Font(None, 36)
    left_score_text = font.render(f"{game_state['left_score']}", True, WHITE)
    right_score_text = font.render(f"{game_state['right_score']}", True, WHITE)
    screen.blit(left_score_text, (WIDTH // 4, 20))
    screen.blit(right_score_text, (3 * WIDTH // 4, 20))


def send_paddle_position(paddle_y, side):
    # Send paddle position to server
    data = {side: paddle_y}
    print(data)
    client.send(pickle.dumps({side: paddle_y}))


# Main game loop
clock = pygame.time.Clock()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Move paddle
    if my_side == "left":
        if keys[pygame.K_UP] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED

    if my_side == "right":
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

    # Send paddle positions to server
    if my_side == "left":
        send_paddle_position(left_paddle.y, "left")
    else:
        send_paddle_position(right_paddle.y, "right")

    # Receive updated game state from server
    game_state = pickle.loads(client.recv(1024))

    # Update positions based on game state
    if my_side == "right":
        left_paddle.y = game_state["left_paddle"]
    else:
        right_paddle.y = game_state["right_paddle"]
    ball.x = game_state["ball_x"]
    ball.y = game_state["ball_y"]

    # Draw everything
    draw_objects(game_state)

    pygame.display.flip()
    clock.tick(FPS)
