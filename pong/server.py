#!/usr/bin/env python3

import socket
import pickle
import pygame

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED_X, BALL_SPEED_Y = 5, 5
FPS = 60

# Initialize Pygame clock (for controlling FPS on the server)
clock = pygame.time.Clock()

# Game state
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

left_score = 0
right_score = 0
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y


def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1


def handle_ball_movement():
    global ball_speed_x, ball_speed_y, left_score, right_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball out of bounds
    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball()

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1


def handle_paddle_movement(data):
    if "left" in data:
        left_paddle.y = data["left"]
    if "right" in data:
        right_paddle.y = data["right"]


# Setup server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.0.109", 5555))
server.listen(2)
print("Server started, waiting for connections...")

clients = []
while len(clients) < 2:
    client, addr = server.accept()
    clients.append(client)
    print(f"Connected to: {addr}")
    # send side to clients
    if len(clients) == 1:
        client.send(pickle.dumps({"side": "left"}))
    else:
        client.send(pickle.dumps({"side": "right"}))

# Main game loop
while True:
    # Receive paddle movement data from both clients
    data1 = pickle.loads(clients[0].recv(1024))
    data2 = pickle.loads(clients[1].recv(1024))

    handle_paddle_movement(data1)
    handle_paddle_movement(data2)

    # Move the ball
    handle_ball_movement()

    # Prepare game state to send back to clients
    game_state = {
        "left_paddle": left_paddle.y,
        "right_paddle": right_paddle.y,
        "ball_x": ball.x,
        "ball_y": ball.y,
        "left_score": left_score,
        "right_score": right_score,
    }
    print(game_state)

    # Send game state to both clients
    for client in clients:
        client.send(pickle.dumps(game_state))

    # Control frame rate
    clock.tick(FPS)
