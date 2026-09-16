from modules.constants import *  

def classify_fingers_and_hands(landmarks, hand_label):
    fingers = []

    # Polegar
    is_thumb_left_side = landmarks[5].x < landmarks[17].x
    if is_thumb_left_side:
        fingers.append(landmarks[THUMB_TIP].x < landmarks[THUMB_TIP - 1].x)
    else:
        fingers.append(landmarks[THUMB_TIP].x > landmarks[THUMB_TIP - 1].x)

    # Demais dedos (Indicador, Médio, Anelar, Mínimo)
    for tip in FINGER_TIPS:
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)

    total_fingers = fingers.count(True)

    return total_fingers, fingers

def classify_gesture(landmarks, hand_label):
    total_fingers, fingers = classify_fingers_and_hands(landmarks, hand_label)

    if total_fingers == 0:
        return "Pedra"
    
    elif total_fingers == 5:
        return "Papel"

    elif fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
        return "Tesoura"

    elif fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and fingers[4]:
        return 'Rock'

    elif fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return 'Faz o L'

    elif fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return 'Beleza, pô'
    
    elif fingers[2] and not fingers[3] and not fingers[4] and not fingers[1] or fingers[0] and not fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
        return "Ban"
    
    else:
        return "Sinal não identificado"   