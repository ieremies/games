#!/usr/bin/env python3


import pygame
import os


def combine_npc_images(head_image, body_image):
    # Create a new surface large enough to hold both head and body
    # Assuming the body image is the base, create a surface the size of the body
    combined_image = pygame.Surface(body_image.get_size(), pygame.SRCALPHA)

    # Blit the body onto the new surface
    combined_image.blit(body_image, (0, 0))

    # Calculate the position for the head on top of the body
    head_x = (body_image.get_width() - head_image.get_width()) // 2
    head_y = 0  # Adjust depending on where the head should be placed

    # Blit the head on top of the body
    combined_image.blit(head_image, (head_x, head_y))

    return combined_image


def load_images_from_folder(folder_path):
    """Helper function to load all images from a folder."""
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):  # Adjust if you use other formats
            img_path = os.path.join(folder_path, filename)
            img = pygame.image.load(img_path).convert_alpha()
            images.append(img)
    return images
