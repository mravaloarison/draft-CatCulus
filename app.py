import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

capture = cv2.VideoCapture(1)

def count_fingers(hand_landmarks):
    finger_count = 0
    for idx, landmark in enumerate(hand_landmarks.landmark):
        is_right_thumb_up = idx == 4 and landmark.x < hand_landmarks.landmark[3].x
        is_left_thumb_up = idx == 4 and landmark.x > hand_landmarks.landmark[3].x
        is_other_finger_up = idx in [8, 12, 16, 20] and landmark.y < hand_landmarks.landmark[idx - 1].y

        is_finger_up = is_right_thumb_up or is_left_thumb_up or is_other_finger_up
        if is_finger_up:
            finger_count += 1
    return finger_count

def hand_tracker(frame, results):
    ...


    