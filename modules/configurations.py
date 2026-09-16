import cv2
import os
import pygame

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from time import time

from modules.constants import *
from app.classification import *


def configuration_hand_landmarker():
    # Configuração do Hand Landmarker (Nova API)
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_hands=2,
        min_hand_detection_confidence=0.7,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )
    detector = vision.HandLandmarker.create_from_options(options)

    return detector

def draw_point_lines(detection_result, frame):
        gesture = ""

        if detection_result.hand_landmarks:
            for hand_landmarks, handedness in zip(detection_result.hand_landmarks, detection_result.handedness):
                h, w, _ = frame.shape

                for p1_idx, p2_idx in HAND_CONNECTIONS:
                    pt1 = (int(hand_landmarks[p1_idx].x * w), int(hand_landmarks[p1_idx].y * h))
                    pt2 = (int(hand_landmarks[p2_idx].x * w), int(hand_landmarks[p2_idx].y * h))
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

                for landmark in hand_landmarks:
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

                hand_label = handedness[0].category_name
                gesture = classify_gesture(hand_landmarks, hand_label)

        return gesture

def ban(cap, gesture, frame, detector, ban_time):
        if gesture == 'Ban':
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            base_gray_bgr = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

            try:
                pygame.mixer.init()
                pygame.mixer.music.load("sons/ban.mp3")
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Erro ao tocar som: {e}")

            os.makedirs("screenshots", exist_ok=True)
            ban_count = 1
            while os.path.exists(f"screenshots/ban_{ban_count}.jpg"):
                ban_count += 1

            start_ban = time()
            saved = False
            
            while True:
                elapsed_time = time() - start_ban
                if elapsed_time >= ban_time:
                    break
                    
                time_left = ban_time - int(elapsed_time)
                
                cap.read()
                if cv2.waitKey(2) & 0xFF == ord('q') and 0xFF == ord('s'):
                    detector.close()
                    return 
                
                display_frame = base_gray_bgr.copy()
                
                cv2.putText(display_frame, "Esse sinal nao pode!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                cv2.putText(display_frame, f"Ban de: {time_left}s", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                
                if not saved:
                    cv2.imwrite(f"screenshots/ban_{ban_count}.jpg", display_frame)
                    saved = True
                    
                cv2.imshow("Pedra, Papel ou Tesoura - MediaPipe Tasks", display_frame)

            return True