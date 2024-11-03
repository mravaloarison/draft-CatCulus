import pygame
import cv2
from hand_tracker import HandTracker

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([800, 600])

finger_count, handedness_str = 0, "Right"

hand_tracker = HandTracker(capture=cv2.VideoCapture(1))

font = pygame.font.Font(None, 36)

running = True
while running:
    screen.fill((0, 0, 0))

    hand_tracker.track_hands()
    finger_count, handedness_str = hand_tracker.get_finger_count()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    text = font.render(f"Hello, {handedness_str}, {finger_count}", True, (255, 255, 255))
    screen.blit(text, (400, 300))

    pygame.display.update()

pygame.quit()
