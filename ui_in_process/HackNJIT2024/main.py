import pygame 
import sys
import random
import math

from generate_quiz import generate_quiz
from tkinter import *
from PIL import Image
import os

# Initialize Pygame
pygame.init()

# Set up the screen dimensions and other parameters
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cat and Ghost Animation")

def load_gif_frames(gif_path):
    """Load all frames of a GIF file"""
    frames = []
    gif = Image.open(gif_path)
    try:
        while True:
            # Convert each frame to pygame surface
            current_frame = pygame.image.fromstring(
                gif.convert("RGBA").tobytes(), gif.size, "RGBA")
            frames.append(pygame.transform.scale(current_frame, (screen_width, screen_height)))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

# Load welcome screen assets and game assets
try:
    # Load welcome GIF frames
    welcome_gif_frames = load_gif_frames("/Users/jasminaabdullaeva/hackNJIT24-1/ui_in_process/HackNJIT2024/Background Images/steampunkwelcomegif.gif")
    # Load background GIF frames for the game screen
    background_gif_frames = load_gif_frames("/Users/jasminaabdullaeva/hackNJIT24-1/ui_in_process/HackNJIT2024/blimp/blimpanimation.gif")
    
    # Load the cat sprite sheet
    cat_sprite_sheet = pygame.image.load("/Users/jasminaabdullaeva/hackNJIT24/ui_in_process/HackNJIT2024/4 Cat 2/Walk.png").convert_alpha()
    
    # Load the ghost sprite sheet
    ghost_sprite_sheet = pygame.image.load("/Users/jasminaabdullaeva/hackNJIT24/ui_in_process/HackNJIT2024/opponents/Bonus Character/Ghost_Death.png").convert_alpha()
    
    # Load the ghost death sprite sheet
    ghost_death_sprite_sheet = pygame.image.load("/Users/jasminaabdullaeva/hackNJIT24/ui_in_process/HackNJIT2024/opponents/Bonus Character/Ghost_Death.png").convert_alpha()
    
except Exception as e:
    print(f"Error loading image files: {e}")
    sys.exit(1)

# Animation control variables
welcome_frame_index = 0
background_frame_index = 0
frame_delay = 100  # milliseconds
last_frame_time = 0

# Welcome screen state
in_welcome_screen = True
transition_alpha = 0
transitioning = False

# Create transparent surface for fade transition
fade_surface = pygame.Surface((screen_width, screen_height))
fade_surface.fill((0, 0, 0))

# Define the cat sprite dimensions
sprite_width, sprite_height = 48, 48  # Original frame size
scale_factor = 4  # Scale factor to make the image bigger
scaled_width = sprite_width * scale_factor
scaled_height = sprite_height * scale_factor
num_frames_cat = 6  # Total number of frames in the sprite sheet

# Extract and scale each frame from the cat sprite sheet
cat_frames = []
for i in range(num_frames_cat):
    frame = cat_sprite_sheet.subsurface((i * sprite_width, 0, sprite_width, sprite_height))
    scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
    cat_frames.append(scaled_frame)

# Define ghost sprite dimensions
ghost_sprite_width, ghost_sprite_height = 48, 48  # Adjust based on actual frame size
ghost_scale_factor = 3  # Increased scale factor to make ghosts bigger
ghost_scaled_width = ghost_sprite_width * ghost_scale_factor
ghost_scaled_height = ghost_sprite_height * ghost_scale_factor
num_frames_ghost = 4  # Total number of frames in the ghost sprite sheet

# Extract and scale each frame from the ghost sprite sheet
ghost_frames = []
for i in range(num_frames_ghost):
    frame = ghost_sprite_sheet.subsurface((i * ghost_sprite_width, 0, ghost_sprite_width, ghost_sprite_height))
    scaled_frame = pygame.transform.scale(frame, (ghost_scaled_width, ghost_scaled_height))
    ghost_frames.append(scaled_frame)

# Define the dimensions for the death animation
death_num_frames = 5  # Adjust according to the number of frames in the death animation
ghost_death_frames = []
for i in range(death_num_frames):
    frame = ghost_death_sprite_sheet.subsurface((i * ghost_sprite_width, 0, ghost_sprite_width, ghost_sprite_height))
    scaled_frame = pygame.transform.scale(frame, (ghost_scaled_width, ghost_scaled_height))
    ghost_death_frames.append(scaled_frame)

# Define ghost starting positions and directions
ghosts = [
    {"x": -ghost_scaled_width, "y": screen_height // 2, "target_x": screen_width // 2, "target_y": screen_height // 2},  # Left
    {"x": screen_width, "y": screen_height // 2, "target_x": screen_width // 2, "target_y": screen_height // 2},  # Right
    {"x": screen_width, "y": 0, "target_x": screen_width // 2, "target_y": screen_height // 2},  # Top-right diagonal
    {"x": -ghost_scaled_width, "y": 0, "target_x": screen_width // 2, "target_y": screen_height // 2},  # Top-left diagonal
]

# Adding additional fields to ghost dictionaries to track state
for ghost in ghosts:
    ghost["is_dead"] = False  # Track if the ghost has reached the cat
    ghost["death_frame_index"] = 0  # Frame index for the death animation

ghost_speed = 2  # Speed of ghost movement
ghost_stop_distance = 9  # Distance at which the ghost stops near the cat

# Platform settings
platform_width = 400
platform_height = 40
platform_color = (205, 170, 125)  # Warm wooden color
platform_border_color = (139, 69, 19)  # Dark brown border
platform_y = screen_height // 2 + scaled_height // 2  # Position platform under cat's feet

# Create platform surface with rounded corners
platform_surface = pygame.Surface((platform_width, platform_height), pygame.SRCALPHA)
pygame.draw.rect(platform_surface, platform_color, (0, 0, platform_width, platform_height), border_radius=15)
pygame.draw.rect(platform_surface, platform_border_color, (0, 0, platform_width, platform_height), 3, border_radius=15)

# Font setup for speech bubble
font = pygame.font.Font(None, 36)

# Load results data
results = generate_quiz()
messages = [item["instructions"] for item in results]

# Set up initial instruction display
current_message = random.choice(messages)
message_change_timer = 0
message_change_interval = 3000  # interval for changing questions

def handle_welcome_screen():
    global in_welcome_screen, transitioning, transition_alpha, welcome_frame_index, last_frame_time

    current_time = pygame.time.get_ticks()
    
    # Update GIF frame
    if current_time - last_frame_time > frame_delay:
        welcome_frame_index = (welcome_frame_index + 1) % len(welcome_gif_frames)
        last_frame_time = current_time

    # Draw current frame of welcome GIF
    screen.blit(welcome_gif_frames[welcome_frame_index], (0, 0))
    
    # Get mouse position and check for clicks
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    # Create a clickable region in the center of the screen
    click_rect = pygame.Rect(
        screen_width // 4,
        screen_height // 4,
        screen_width // 2,
        screen_height // 2
    )
    
    # Check if mouse is over the clickable region
    if click_rect.collidepoint(mouse_pos):
        # Add hover effect
        pygame.draw.rect(screen, (255, 255, 255, 50), click_rect, 2)
        
        if mouse_clicked:
            transitioning = True

    # Handle transition
    if transitioning:
        transition_alpha += 5
        if transition_alpha >= 255:
            in_welcome_screen = False
            return
            
        fade_surface.set_alpha(transition_alpha)
        screen.blit(fade_surface, (0, 0))

def run_game():
    global current_message, message_change_timer, background_frame_index, last_frame_time
    current_time = pygame.time.get_ticks()

    # Update background GIF frame
    if current_time - last_frame_time > frame_delay:
        background_frame_index = (background_frame_index + 1) % len(background_gif_frames)
        last_frame_time = current_time

    # Draw the animated background
    screen.blit(background_gif_frames[background_frame_index], (0, 0))

    # Draw the platform
    platform_x = screen_width // 2 - platform_width // 2
    screen.blit(platform_surface, (platform_x, platform_y))

    # Update the cat animation frame
    frame_index_cat = (pygame.time.get_ticks() // 100) % num_frames_cat

    # Calculate cat position
    cat_x = screen_width // 2 - scaled_width // 2
    cat_y = platform_y - scaled_height + 10  # Position cat on top of platform

    # Draw the current frame of the cat
    screen.blit(cat_frames[int(frame_index_cat)], (cat_x, cat_y))

    # Move and draw each ghost
    frame_index_ghost = (pygame.time.get_ticks() // 100) % num_frames_ghost
    for ghost in ghosts:
        ghost_x, ghost_y = ghost["x"], ghost["y"]
        target_x, target_y = ghost["target_x"], ghost["target_y"]

        # Check if the ghost is dead
        if ghost["is_dead"]:
            # Play death animation
            if ghost["death_frame_index"] < len(ghost_death_frames):
                screen.blit(ghost_death_frames[ghost["death_frame_index"]], (int(ghost_x), int(ghost_y)))
                ghost["death_frame_index"] += 1
            continue

        # Calculate distance and move ghost toward target
        distance = math.hypot(target_x - ghost_x, target_y - ghost_y)
        if distance > ghost_stop_distance:
            ghost["x"] += (target_x - ghost_x) / distance * ghost_speed
            ghost["y"] += (target_y - ghost_y) / distance * ghost_speed
        else:
            ghost["is_dead"] = True

        # Draw the current frame of the ghost's walking animation if not dead
        screen.blit(ghost_frames[int(frame_index_ghost)], (int(ghost["x"]), int(ghost["y"])))

    # Change message periodically
    if current_time - message_change_timer > message_change_interval:
        current_message = random.choice(messages)
        message_change_timer = current_time

    # Draw speech bubble
    text_surface = font.render(current_message, True, (0, 0, 0))
    bubble_width = text_surface.get_width() + 40
    bubble_height = 60

    # Draw bubble background with semi-transparency
    bubble_surface = pygame.Surface((bubble_width, bubble_height))
    bubble_surface.fill((255, 255, 255))
    bubble_surface.set_alpha(230)
    
    bubble_rect = pygame.Rect(
        (screen_width - bubble_width) // 2,
        cat_y - bubble_height - 20,
        bubble_width,
        bubble_height,
    )

    # Draw the speech bubble background and text
    screen.blit(bubble_surface, bubble_rect.topleft)
    text_x = bubble_rect.x + 20
    text_y = bubble_rect.y + (bubble_height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))

def main():
    global in_welcome_screen, last_frame_time
    
    clock = pygame.time.Clock()
    running = True
    last_frame_time = pygame.time.get_ticks()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        if in_welcome_screen:
            handle_welcome_screen()
        else:
            run_game()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()