import pygame
import cv2
from hand_tracker import HandTracker
from generate_quiz import generate_quiz
from objects.quiz import Quiz

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

count = 5
index = 0

generated_quiz = generate_quiz() 
quiz = Quiz(generated_quiz[index])

clock = pygame.time.Clock()

message_change_timer = 0
message_change_interval = 3000 

bubble_padding = 20  
bubble_height = 60  

clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame = hand_tracker.track_hands()
    left_count, right_count = hand_tracker.get_finger_count() 

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
        # TODO: 
        # Ghost Dies and Generate new quiz

    text_surface = font.render(quiz.instructions, True, (0, 0, 0))
    bubble_width = text_surface.get_width() + bubble_padding * 2

    bubble_surface = pygame.Surface((bubble_width, bubble_height))
    bubble_surface.fill((255, 255, 255))
    bubble_surface.set_alpha(230)
    
    bubble_rect = pygame.Rect(
        (WIDTH - bubble_width) // 2,
        (HEIGHT - bubble_height) //2,
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
