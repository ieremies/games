#!/usr/bin/env python3
import pygame
import random
import os

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
    global deck
    deck = deck.copy()
    random.shuffle(deck)
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


# Main game loop
deck, player_hand, dealer_hand = start_game()
game_over = False
player_turn = True
dealer_turn = False
font = pygame.font.SysFont(None, 36)

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
        elif dealer_score > 21:
            result = "Dealer busts! Player wins."
        elif player_score > dealer_score:
            result = "Player wins!"
        elif dealer_score > player_score:
            result = "Dealer wins!"
        else:
            result = "It's a tie!"

        result_text = font.render(result, True, (255, 255, 255))
        screen.blit(result_text, (50, 350))

    pygame.display.flip()
    clock.tick(30)
