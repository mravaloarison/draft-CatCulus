import pygame
import cv2
from hand_tracker import HandTracker

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([800, 600])

capture = cv2.VideoCapture(1)
hand_tracker = HandTracker(capture)

font = pygame.font.Font(None, 36)
running = True

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame = hand_tracker.track_hands()
    finger_count, handedness_str = hand_tracker.get_finger_count()

    if frame is not None:
        frame_surface = pygame.surfarray.make_surface(cv2.transpose(frame)) 
        screen.blit(frame_surface, (0, 0))  

    text = font.render(f"Hello, {handedness_str}, {finger_count}", True, (255, 255, 255))
    screen.blit(text, (10, 10))  

    pygame.display.update()

pygame.quit()
capture.release()
