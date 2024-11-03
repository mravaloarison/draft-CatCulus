import pygame 
import sys
import random
import math

from generate_quiz import generate_quiz

# Initialize Pygame
pygame.init()

# Set up the screen dimensions and other parameters
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cat and Ghost Animation")

# Load and scale the background
background = pygame.image.load("/Users/jasminaabdullaeva/hackNJIT24/ui_in_process/HackNJIT2024/Background Images/orangebackground.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load the cat sprite sheet
cat_sprite_sheet = pygame.image.load("/Users/jasminaabdullaeva/hackNJIT24/ui_in_process/HackNJIT2024/4 Cat 2/Walk.png").convert_alpha()

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

# Load the ghost sprite sheet
ghost_sprite_sheet = pygame.image.load("/Users/jasminaabdullaeva/hackNJIT24/ui_in_process/HackNJIT2024/opponents/Bonus Character/Ghost_Death.png").convert_alpha()

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

# Load the ghost death sprite sheet
ghost_death_sprite_sheet = pygame.image.load("/Users/jasminaabdullaeva/hackNJIT24/ui_in_process/HackNJIT2024/opponents/Bonus Character/Ghost_Death.png").convert_alpha()

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

# Load results data from result_sample.js
# results = [item["instructions"] for item in generate_quiz()]
    

# print(results)\\\\\\

# Extract the instructions from the results
results = generate_quiz()

messages = [item["instructions"] for item in results]

for items in messages:
    print(items)

# Set up initial instruction display
current_message = random.choice(messages)
message_change_timer = 0
message_change_interval = 3000  # interval for changing questions

# Animation settings
clock = pygame.time.Clock()
frame_index_cat = 0
frame_index_ghost = 0
frame_speed = 0.35  # Animation speed

# Define speech bubble settings (if not already defined)
bubble_padding = 20  # Space between text and bubble edges
bubble_height = 60   # Height of the speech bubble

# Main game loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(background, (0, 0))

    # Draw the platform
    platform_x = screen_width // 2 - platform_width // 2
    screen.blit(platform_surface, (platform_x, platform_y))

    # Update the cat animation frame
    frame_index_cat += frame_speed
    if frame_index_cat >= len(cat_frames):
        frame_index_cat = 0

    # Calculate cat position
    cat_x = screen_width // 2 - scaled_width // 2
    cat_y = platform_y - scaled_height + 10  # Position cat on top of platform

    # Draw the current frame of the cat
    screen.blit(cat_frames[int(frame_index_cat)], (cat_x, cat_y))

    # Move and draw each ghost toward the cat or play death animation if "dead"
    for ghost in ghosts:
        ghost_x, ghost_y = ghost["x"], ghost["y"]
        target_x, target_y = ghost["target_x"], ghost["target_y"]

        # Check if the ghost is dead
        if ghost["is_dead"]:
            # Play death animation
            if ghost["death_frame_index"] < len(ghost_death_frames):
                screen.blit(ghost_death_frames[ghost["death_frame_index"]], (int(ghost_x), int(ghost_y)))
                ghost["death_frame_index"] += 1  # Progress to the next frame in the death animation
            continue  # Skip movement for dead ghosts

        # Calculate distance and move ghost toward target
        distance = math.hypot(target_x - ghost_x, target_y - ghost_y)
        if distance > ghost_stop_distance:
            ghost["x"] += (target_x - ghost_x) / distance * ghost_speed
            ghost["y"] += (target_y - ghost_y) / distance * ghost_speed
        else:
            # Trigger death animation when the ghost reaches the cat
            ghost["is_dead"] = True

        # Draw the current frame of the ghost's walking animation if not dead
        screen.blit(ghost_frames[int(frame_index_ghost)], (int(ghost["x"]), int(ghost["y"])))

    # Update the ghost walking animation frame
    frame_index_ghost += frame_speed
    if frame_index_ghost >= len(ghost_frames):
        frame_index_ghost = 0

    # Change message periodically
    if current_time - message_change_timer > message_change_interval:
        current_message = random.choice(messages)
        message_change_timer = current_time

    # Draw speech bubble
    text_surface = font.render(current_message, True, (0, 0, 0))
    bubble_width = text_surface.get_width() + bubble_padding * 2

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
    text_x = bubble_rect.x + bubble_padding
    text_y = bubble_rect.y + (bubble_height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Set frame rate to 60 FPS

# Clean up and exit the game
pygame.quit()
sys.exit()

