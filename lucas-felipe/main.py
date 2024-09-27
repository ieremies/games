#!/usr/bin/env python3
import pygame
import random
import os

from utils.life import Lifebar
from utils.sound import Sound
from utils.score import Score

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((750, 480))
pygame.display.set_caption("Pygame 21 (Blackjack)")
clock = pygame.time.Clock()

# Define card values and deck
CARD_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "jack": 10,
    "queen": 10,
    "king": 10,
    "ace": [1, 11],
}
SUITS = ["hearts", "diamonds", "clubs", "spades"]
deck = [f"{value}_of_{suit}" for value in CARD_VALUES.keys() for suit in SUITS]


# Load card images
def load_card_images():
    card_images = {}
    for card in deck:
        image_path = os.path.join("img/", f"{card}.png")
        if os.path.exists(image_path):
            card_images[card] = pygame.image.load(image_path)
    return card_images


card_images = load_card_images()


def reset_deck():
    deck = [f"{value}_of_{suit}" for value in CARD_VALUES.keys() for suit in SUITS]
    return deck


# Helper functions
def draw_card(deck):
    card = deck.pop(random.randint(0, len(deck) - 1))
    return card


def calculate_score(hand):
    total, aces = 0, 0
    for card in hand:
        value = card.split("_")[0]
        if value == "ace":
            aces += 1
            total += 11
        else:
            total += CARD_VALUES[value]

    # Handle ace as 1 or 11
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


# Game initialization
def start_game():
    global deck, game_over, player_turn, dealer_turn, player_hand, dealer_hand, life_taken
    deck = deck.copy()
    random.shuffle(deck)
    game_over = False
    player_turn = True
    dealer_turn = False
    life_taken = False
    player_hand = [draw_card(deck), draw_card(deck)]
    dealer_hand = [draw_card(deck), draw_card(deck)]
    return deck, player_hand, dealer_hand


# Draw the hands on the screen
def display_hand(screen, hand, pos, label):
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"{label} Hand:", True, (255, 255, 255))
    screen.blit(text, pos)

    x_offset = 0
    for card in hand:
        card_image = card_images.get(card)
        if card_image:
            card_image = pygame.transform.scale(
                card_image, (80, 120)
            )  # Resize if necessary
            screen.blit(card_image, (pos[0] + x_offset, pos[1] + 30))
            x_offset += 90  # Adjust spacing between cards


def win():
    pygame.mixer.music.stop()
    win_snd = Sound("snd/win.wav")
    win_snd.play()
    # Write "Você venceu, sua alma foi salva."
    font = pygame.font.Font(None, 36)
    text = font.render("Você venceu, sua alma foi salva.", True, (255, 255, 255))
    screen.blit(text, (50, 350))


def lose():
    pygame.mixer.music.stop()
    lose_snd = Sound("snd/lose.wav")
    lose_snd.play()
    # Write "Você perdeu, sua alma foi condenada."
    font = pygame.font.Font(None, 36)
    text = font.render("Você perdeu, sua alma foi condenada.", True, (255, 255, 255))
    screen.blit(text, (50, 350))


def controls():
    # Write the controls on the screen:
    font = pygame.font.Font(None, 26)
    text = font.render("Pressione H para pedir carta", True, (255, 255, 255))
    screen.blit(text, (50, 390))
    text = font.render("Pressione S para parar", True, (255, 255, 255))
    screen.blit(text, (50, 420))
    text = font.render("Pressione R para próxima mão", True, (255, 255, 255))
    screen.blit(text, (50, 450))


# Main game loop
deck, player_hand, dealer_hand = start_game()
game_over = False
player_turn = True
dealer_turn = False
life_taken = False
font = pygame.font.SysFont(None, 36)
life = Lifebar(start_value=3, max_value=7, icon=None)
pygame.mixer.init()
pygame.mixer.music.load("snd/music.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)

story = []
for i in range(1, 7):
    story.append(pygame.image.load(f"img/story{i}.jpg"))
    story[i - 1] = pygame.transform.scale(story[i - 1], (750, 480))

i = 1
while True:
    screen.fill((0, 128, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h and player_turn:  # Player hits
                player_hand.append(draw_card(deck))
                if calculate_score(player_hand) > 21:
                    player_turn = False
                    dealer_turn = True
                    game_over = True
            if event.key == pygame.K_s and player_turn:  # Player stands
                player_turn = False
                dealer_turn = True

            if event.key == pygame.K_r and game_over:
                deck = reset_deck()
                deck, player_hand, dealer_hand = start_game()
                game_over = False
                player_turn = True
                dealer_turn = False

    if i < 7:
        screen.blit(story[i - 1], (0, 0))
        pygame.display.flip()
        pygame.time.wait(1000)
        i += 1
        continue

    if life.value >= 7:
        win()
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        exit()
    if life.value <= 0:
        lose()
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        exit()

    # Dealer logic
    if dealer_turn and not game_over:
        while calculate_score(dealer_hand) < 17:
            dealer_hand.append(draw_card(deck))
        dealer_turn = False
        game_over = True

    # Display cards
    display_hand(screen, player_hand, (50, 50), "Player")
    display_hand(
        screen, dealer_hand if game_over else dealer_hand[:1], (400, 50), "Dealer"
    )

    # Score calculation and check game over
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    # Display scores
    player_text = font.render(f"Player Score: {player_score}", True, (255, 255, 255))
    screen.blit(player_text, (50, 300))

    if game_over:
        dealer_text = font.render(
            f"Dealer Score: {dealer_score}", True, (255, 255, 255)
        )
        screen.blit(dealer_text, (350, 300))

        # Determine winner
        if player_score > 21:
            result = "Player busts! Dealer wins."
            if not life_taken:
                life.value -= 1
                life_taken = True
        elif dealer_score > 21:
            result = "Dealer busts! Player wins."
            if not life_taken:
                life.value += 1
                life_taken = True
        elif player_score > dealer_score:
            result = "Player wins!"
            if not life_taken:
                life.value += 1
                life_taken = True
        elif dealer_score > player_score:
            result = "Dealer wins!"
            if not life_taken:
                life.value -= 1
                life_taken = True
        else:
            result = "It's a tie!"

        result_text = font.render(result, True, (255, 255, 255))
        screen.blit(result_text, (50, 350))

    life.draw(screen)

    controls()

    pygame.display.flip()
    clock.tick(30)
