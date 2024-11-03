import pygame
import cv2
from hand_tracker import HandTracker

WIDTH, HEIGHT = 1440, 966

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

capture = cv2.VideoCapture(1)
hand_tracker = HandTracker(capture)

font = pygame.font.Font(None, 36)
running = True

background_image = pygame.image.load("bg.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  

while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame = hand_tracker.track_hands()
    left_count, right_count = hand_tracker.get_finger_count() 

    if frame is not None:
        frame_surface = pygame.surfarray.make_surface(cv2.transpose(frame)) 
        screen.blit(frame_surface, (0, 0))  

    left_text = font.render(f"Left: {left_count}", True, (255, 255, 255))
    right_text = font.render(f"Right: {right_count}", True, (255, 255, 255))

    screen.blit(left_text, (WIDTH - left_text.get_width() - 10, 10)) 
    screen.blit(right_text, (WIDTH - right_text.get_width() - 10, 40))  

    pygame.display.update()

pygame.quit()
capture.release()
