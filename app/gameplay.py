import cv2
import os
from time import time
from app.generate_response import computer_choice

def init_gameplay(window_name):
    images = {}
    for choice_str in ["Pedra", "Papel", "Tesoura", "Ban"]:
        img_path = f"images/{choice_str.lower()}.jpg"
        if not os.path.exists(img_path):
            img_path = f"images/{choice_str.lower()}.png"
            
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            img = cv2.resize(img, (120, 120))
            images[choice_str] = img
        else:
            print(f"Aviso: Imagem {img_path} nao encontrada.")

    state = {
        "window_name": window_name,
        "computer_choice": "Nenhuma",
        "user_choice_locked": "Nenhuma",
        "result": "",
        "btn_rect": (0, 0, 0, 0),
        "is_counting_down": False,
        "countdown_start": 0,
        "countdown_duration": 3,
        "game_played": False,
        "images": images,
        "score_user": 0,
        "score_comp": 0
    }

    def mouse_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x1, y1, x2, y2 = state["btn_rect"]
            if x1 <= x <= x2 and y1 <= y <= y2:
                if not state["is_counting_down"]:
                    state["is_counting_down"] = True
                    state["countdown_start"] = time()
                    state["computer_choice"] = "Pensando..."
                    state["user_choice_locked"] = "Nenhuma"
                    state["result"] = ""
                    state["game_played"] = False

    cv2.setMouseCallback(window_name, mouse_click)
    return state

def get_winner(user_g, comp_c):
    if user_g == "" or user_g == "Nenhuma" or user_g == "Nenhuma mao":
        return "Computador (Nao jogou)"
        
    valid_gestures = ["Pedra", "Papel", "Tesoura"]
    if user_g not in valid_gestures:
        return "Invalido"
        
    if user_g == comp_c:
        return "Empate"
        
    if (user_g == "Pedra" and comp_c == "Tesoura") or \
       (user_g == "Papel" and comp_c == "Pedra") or \
       (user_g == "Tesoura" and comp_c == "Papel"):
        return "Voce"
        
    return "Computador"

def draw_and_update(state, frame, gesture, ban_verify):
    h, w, _ = frame.shape
    
    btn_x1, btn_y1, btn_x2, btn_y2 = w//2 - 100, h - 80, w//2 + 100, h - 20
    state["btn_rect"] = (btn_x1, btn_y1, btn_x2, btn_y2)
    
    cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (0, 200, 0), -1)
    cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), (0, 255, 0), 3)
    text_size = cv2.getTextSize("JOGAR", cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
    tx = btn_x1 + (btn_x2 - btn_x1 - text_size[0]) // 2
    ty = btn_y1 + (btn_y2 - btn_y1 + text_size[1]) // 2
    cv2.putText(frame, "JOGAR", (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

    font_scale = 0.9
    thickness = 2
    t1 = f"Voce: {state['score_user']} "
    t2 = "X "
    t3 = f"Computador: {state['score_comp']}"
    
    s1 = cv2.getTextSize(t1, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    s2 = cv2.getTextSize(t2, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    s3 = cv2.getTextSize(t3, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
    
    total_w = s1[0] + s2[0] + s3[0]
    start_x = w // 2 - total_w // 2
    text_y = btn_y1 - 20 
    
    cv2.putText(frame, t1, (start_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), thickness)
    cv2.putText(frame, t2, (start_x + s1[0], text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
    cv2.putText(frame, t3, (start_x + s1[0] + s2[0], text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)

    if ban_verify:
        state["score_comp"] += 1
        state["is_counting_down"] = False
        state["game_played"] = True
        state["computer_choice"] = "Ban"
        state["user_choice_locked"] = "Banido"
        state["result"] = "Computador (Ban)"
        return 

    if state["is_counting_down"]:
        elapsed = time() - state["countdown_start"]
        time_left = state["countdown_duration"] - int(elapsed)
        
        if elapsed >= state["countdown_duration"]:
            state["is_counting_down"] = False
            state["game_played"] = True
            
            state["computer_choice"] = computer_choice()
            state["user_choice_locked"] = gesture if gesture != "" else "Nenhuma"
            
            res = get_winner(state["user_choice_locked"], state["computer_choice"])
            state["result"] = res
            
            if "Voce" in res:
                state["score_user"] += 1
            elif "Computador" in res:
                state["score_comp"] += 1

        else:
            num_text = str(time_left)
            num_size = cv2.getTextSize(num_text, cv2.FONT_HERSHEY_SIMPLEX, 6, 15)[0]
            nx = (w - num_size[0]) // 2
            ny = (h + num_size[1]) // 2
            cv2.putText(frame, num_text, (nx, ny), cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 0, 0), 20)
            cv2.putText(frame, num_text, (nx, ny), cv2.FONT_HERSHEY_SIMPLEX, 6, (0, 165, 255), 10)

    if state["game_played"] and not state["is_counting_down"]:
        
        comp_choice = state["computer_choice"]
        if comp_choice in state["images"]:
            img_to_draw = state["images"][comp_choice]
            ih, iw, _ = img_to_draw.shape
            ix = w//2 - iw//2
            iy = 10
            frame[iy:iy+ih, ix:ix+iw] = img_to_draw
            cv2.rectangle(frame, (ix, iy), (ix+iw, iy+ih), (0, 255, 0), 2)
            
            comp_txt = f"Computador: {comp_choice}"
            t_size = cv2.getTextSize(comp_txt, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            tx = w//2 - t_size[0]//2
            ty = iy + ih + 30
            cv2.putText(frame, comp_txt, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            cv2.putText(frame, f"Computador: {comp_choice}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        
        res = state["result"]
        
        text1 = "Ganhador: " if res not in ["Invalido", "Empate"] else "Resultado: "
        color1 = (0, 0, 255) if "Ban" in res else (0, 255, 255) 
        
        text2 = res
        color2 = (0, 255, 255) 
        if "Voce" in res:
            color2 = (255, 0, 0) 
        elif "Computador" in res:
            color2 = (0, 0, 255) 
            
        if "Ban" in res:
            color2 = (0, 0, 255) 
            
        s1 = cv2.getTextSize(text1, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        s2 = cv2.getTextSize(text2, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        
        total_w = s1[0] + s2[0]
        start_x = w // 2 - total_w // 2
        text_y_ganhador = btn_y1 - 70
        
        cv2.putText(frame, text1, (start_x, text_y_ganhador), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color1, 3)
        cv2.putText(frame, text2, (start_x + s1[0], text_y_ganhador), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color2, 3)
