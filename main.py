import cv2
import mediapipe as mp

from modules.constants import *    
from modules.configurations import *
from app.generate_response import *
from app.gameplay import init_gameplay, draw_and_update

def main(cap):
    detector = configuration_hand_landmarker()
    ban_time = 5
    
    window_name = "Pedra, Papel ou Tesoura - MediaPipe Tasks"
    cv2.namedWindow(window_name)
    game_state = init_gameplay(window_name)
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Erro ao acessar a webcam.")
            break

        frame = cv2.resize(frame, (0, 0), fx=1.5, fy=1.5)
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = detector.detect(mp_image)

        gesture = draw_point_lines(detection_result, frame)
        ban_verify = ban(cap, gesture, frame, detector, ban_time)
        status = draw_and_update(game_state, frame, gesture, ban_verify)
        if status == "BREAK":
            break

        if ban_verify == True:
            ban_time += 5
            continue
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            detector.close()
            break

        cv2.imshow(window_name, frame)

if __name__ == "__main__":
    try:
        cap = cv2.VideoCapture(0)
        main(cap)

        cap.release()
        cv2.destroyAllWindows()

    except Exception as error:
        cap.release()
        cv2.destroyAllWindows()
        print(f"Erro:{error}")