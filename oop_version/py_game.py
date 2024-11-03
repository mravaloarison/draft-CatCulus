import pygame
import cv2
from hand_tracker import HandTracker
from generate_quiz import generate_quiz
from objects.quiz import Quiz
import math
import random

WIDTH, HEIGHT = 1440, 966

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

capture = cv2.VideoCapture(1)
hand_tracker = HandTracker(capture)

font = pygame.font.Font(None, 39)
hand_font = pygame.font.Font(None, 42)

running = True

background_image = pygame.image.load("bg.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

cat_sprite_sheet = pygame.image.load("assets/cat/Idle.png").convert_alpha()

ghost_sprite_sheet = pygame.image.load("assets/ghost/Ghost_Idle.png").convert_alpha()
ghost_death_sprite_sheet = pygame.image.load("assets/ghost/Ghost_Death.png").convert_alpha()

# Define the cat sprite dimensions
sprite_width, sprite_height = 48, 48  # Original frame size
scale_factor = 4  # Scale factor to make the image bigger
scaled_width = sprite_width * scale_factor
scaled_height = sprite_height * scale_factor
num_frames_cat = 4  # Total number of frames in the sprite sheet

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

# Function to generate ghosts
def generate_ghosts():
    side = random.choice(["left", "right", "top", "bottom"])
    if side == "left":
        return [
            {"x": -ghost_scaled_width, "y": random.randint(0, HEIGHT - ghost_scaled_height),
             "target_x": WIDTH // 2 - ghost_scaled_width // 2,
             "target_y": HEIGHT // 2 - ghost_scaled_height // 2, "is_dead": False, "death_frame_index": 0},
            {"x": -ghost_scaled_width, "y": random.randint(0, HEIGHT - ghost_scaled_height),
             "target_x": WIDTH // 2 - ghost_scaled_width // 2,
             "target_y": HEIGHT // 2 - ghost_scaled_height // 2, "is_dead": False, "death_frame_index": 0}
        ]
    elif side == "right":
        return [
            {"x": WIDTH, "y": random.randint(0, HEIGHT - ghost_scaled_height),
             "target_x": WIDTH // 2 - ghost_scaled_width // 2,
             "target_y": HEIGHT // 2 - ghost_scaled_height // 2, "is_dead": False, "death_frame_index": 0},
            {"x": WIDTH, "y": random.randint(0, HEIGHT - ghost_scaled_height),
             "target_x": WIDTH // 2 - ghost_scaled_width // 2,
             "target_y": HEIGHT // 2 - ghost_scaled_height // 2, "is_dead": False, "death_frame_index": 0}
        ]
    elif side == "top":
        return [
            {"x": random.randint(0, WIDTH - ghost_scaled_width), "y": -ghost_scaled_height,
             "target_x": WIDTH // 2 - ghost_scaled_width // 2,
             "target_y": HEIGHT // 2 - ghost_scaled_height // 2, "is_dead": False, "death_frame_index": 0},
            {"x": random.randint(0, WIDTH - ghost_scaled_width), "y": -ghost_scaled_height,
             "target_x": WIDTH // 2 - ghost_scaled_width // 2,
             "target_y": HEIGHT // 2 - ghost_scaled_height // 2, "is_dead": False, "death_frame_index": 0}
        ]
    else:  # bottom
        return [
            {"x": random.randint(0, WIDTH - ghost_scaled_width), "y": HEIGHT,
             "target_x": WIDTH // 2 - ghost_scaled_width // 2,
             "target_y": HEIGHT // 2 - ghost_scaled_height // 2, "is_dead": False, "death_frame_index": 0},
            {"x": random.randint(0, WIDTH - ghost_scaled_width), "y": HEIGHT,
             "target_x": WIDTH // 2 - ghost_scaled_width // 2,
             "target_y": HEIGHT // 2 - ghost_scaled_height // 2, "is_dead": False, "death_frame_index": 0}
        ]

# Initialize ghosts
ghosts = generate_ghosts()

# Adding additional fields to ghost dictionaries to track state
ghost_speed = 2  # Speed of ghost movement
ghost_stop_distance = 9  # Distance at which the ghost stops near the center

count = 5
index = 0

generated_quiz = generate_quiz() 
quiz = Quiz(generated_quiz[index])

clock = pygame.time.Clock()

message_change_timer = 0
message_change_interval = 3000 

bubble_padding = 20  
bubble_height = 60  

while running:
    current_time = pygame.time.get_ticks()
    screen.blit(background_image, (0, 0))

    # Move and draw each ghost
    frame_index_ghost = (pygame.time.get_ticks() // 100) % num_frames_ghost
    for ghost in ghosts:
        ghost_x, ghost_y = ghost["x"], ghost["y"]
        target_x, target_y = ghost["target_x"], ghost["target_y"]

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame = hand_tracker.track_hands()
    left_count, right_count = hand_tracker.get_finger_count()

    # Update the cat animation frame
    frame_index_cat = (pygame.time.get_ticks() // 100) % num_frames_cat

    # Calculate cat position
    cat_x = WIDTH // 2 - scaled_width // 2
    cat_y = HEIGHT // 2 - scaled_height // 2 - 100

    # Draw the current frame of the cat
    screen.blit(cat_frames[int(frame_index_cat)], (cat_x, cat_y))

    if frame is not None:
        frame_surface = pygame.surfarray.make_surface(cv2.transpose(frame)) 
        screen.blit(frame_surface, (0, 0))  

    left_text = hand_font.render(f"Left or X: {left_count}", True, (0, 255, 255))
    right_text = hand_font.render(f"Right or Y: {right_count}", True, (0, 0, 255))

    screen.blit(left_text, (WIDTH - left_text.get_width() - 10, 10)) 
    screen.blit(right_text, (WIDTH - right_text.get_width() - 10, 40))  

    f = quiz.is_correct(left_count, right_count)
    if f:
        generated_quiz = generate_quiz()
        index = 0
        quiz = Quiz(generated_quiz[index])
        message_change_timer = current_time

        # Generate new ghosts when a new quiz appears
        ghosts = generate_ghosts()

    text_surface = font.render(quiz.instructions, True, (0, 0, 0))
    bubble_width = text_surface.get_width() + bubble_padding * 2

    bubble_surface = pygame.Surface((bubble_width, bubble_height))
    bubble_surface.fill((255, 255, 255))
    bubble_surface.set_alpha(230)

    # Position the bubble above the cat's head
    bubble_rect = pygame.Rect(
        (WIDTH - bubble_width) // 2,
        cat_y - bubble_height,  # Position above the cat
        bubble_width,
        bubble_height,
    )

    screen.blit(bubble_surface, bubble_rect.topleft)
    text_x = bubble_rect.x + bubble_padding
    text_y = bubble_rect.y + (bubble_height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))
    # End bubbles

    pygame.display.update()
    clock.tick(60)

pygame.quit()
capture.release()


