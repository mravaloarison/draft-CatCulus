import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

capture = cv2.VideoCapture(0)

finger_count = 0

WIDTH, HEIGHT = 341, 195

class HandTracker:
    def __init__(self, capture):
        self.capture = capture
        self.mp_hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5
        )
        self.left_finger_count = 0
        self.right_finger_count = 0
        self.left_handedness_str = "Left"
        self.right_handedness_str = "Right"

    def count_fingers(self, hand_landmarks, handedness_str):
        finger_count = 0
        for idx, landmark in enumerate(hand_landmarks.landmark):
            is_thumb_up = (idx == 4 and
                           ((handedness_str == "Right" and landmark.x < hand_landmarks.landmark[3].x) or
                            (handedness_str == "Left" and landmark.x > hand_landmarks.landmark[3].x)))
            is_other_finger_up = idx in [8, 12, 16, 20] and landmark.y < hand_landmarks.landmark[idx - 1].y

            if is_thumb_up or is_other_finger_up:
                finger_count += 1
        return finger_count

    def track_hands(self):
        ret, frame = self.capture.read()
        if not ret:
            print("Ignoring empty camera frame.")
            return

        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame.flags.writeable = False
        results = self.mp_hands.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        self.left_finger_count = 0
        self.right_finger_count = 0

        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness_str = results.multi_handedness[i].classification[0].label
                finger_count = self.count_fingers(hand_landmarks, handedness_str)

                if handedness_str == "Right":
                    self.right_finger_count = finger_count
                elif handedness_str == "Left":
                    self.left_finger_count = finger_count

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
        return frame  

    def get_finger_count(self):
        return self.left_finger_count, self.right_finger_count

        
# def count_fingers(hand_landmarks, handedness_str):
#     finger_count = 0
#     for idx, landmark in enumerate(hand_landmarks.landmark):
#         is_right_thumb_up = idx == 4 and landmark.x < hand_landmarks.landmark[3].x and handedness_str == "Right"
#         is_left_thumb_up = idx == 4 and landmark.x > hand_landmarks.landmark[3].x and handedness_str == "Left"
#         is_other_finger_up = idx in [8, 12, 16, 20] and landmark.y < hand_landmarks.landmark[idx - 1].y

#         is_finger_up = is_right_thumb_up or is_left_thumb_up or is_other_finger_up
#         if is_finger_up:
#             finger_count += 1
#     return finger_count, handedness_str

# with mp_hands.Hands(
#     static_image_mode=False,
#     max_num_hands=2,
#     min_detection_confidence=0.5
# ) as hands:
#     while capture.isOpened():
#         ret, frame = capture.read()
#         if not ret:
#             print("Ignoring empty camera frame.")
#             continue
        
#         frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
#         size = frame.shape
#         frame = cv2.resize(frame, (WIDTH, HEIGHT))
#         frame.flags.writeable = False
#         results = hands.process(frame)
#         frame.flags.writeable = True
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 handedness_str = results.multi_handedness[0].classification[0].label
#                 finger_count = count_fingers(hand_landmarks, handedness_str)
#                 print(finger_count)
#                 mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#         cv2.imshow('MediaPipe Hands', frame)
#         if cv2.waitKey(5) & 0xFF == 27:
#             break

# capture.release()
# cv2.destroyAllWindows()