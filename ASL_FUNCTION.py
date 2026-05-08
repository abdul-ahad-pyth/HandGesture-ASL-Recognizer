def get_hand_state(hand_landmarks):
    landmarks = hand_landmarks.landmark
    
    tips = [4, 8, 12, 16, 20]
    pips = [3, 6, 10, 14, 18]
    fingers = []
    
    thumb_up = (landmarks[4].x < landmarks[3].x) if (landmarks[0].x < landmarks[9].x) else (landmarks[4].x > landmarks[3].x)
    fingers.append(thumb_up)
    
    for tip, pip in zip(tips[1:], pips[1:]):
        fingers.append(landmarks[tip].y < landmarks[pip].y)
        
    return fingers

def recognize_asl(fingers, landmarks):
    t, i, m, r, p = fingers
    lm = landmarks.landmark
    up_fingers = sum(fingers)
    
    # --- 0 Fingers Up ---
    if up_fingers == 0:
        if t:
            return "A"
        if lm[4].y < lm[3].y: # Thumb positioned over fingers
            return "S"
        return "E"

    # --- 4 or 5 Fingers Up (B or Open Hand) ---
    elif up_fingers == 4 and not t:
        return "B"
    elif all(fingers): # All 5 fingers up
        return "B"

    # --- 1 Finger Up ---
    elif up_fingers == 1:
        if p: return "I"
        if i: return "D"
        return "A"

    # --- 2 Fingers Up ---
    elif up_fingers == 2:
        if i and t: return "L"
        if i and m: return "V" # Basic V
        if p and t: return "Y"

    # --- Specific Logic for Complex Signs ---
    
    # C (Curved)
    elif i and m and r and p and t:
        if abs(lm[4].x - lm[8].x) > 0.1: 
            return "C"
            
    # F (Check distance between Thumb and Index)
    elif t and i and not any([m, r, p]):
        distance = ((lm[4].x - lm[8].x)**2 + (lm[4].y - lm[8].y)**2)**0.5
        if distance < 0.05:
            return "F"
        return "D"

    # G / H (Orientation based)
    elif i and m and not any([r, p]) and not t:
        return "H" if m else "G"

    # W (Index, Middle, Ring)
    elif i and m and r and not p and not t:
        return "W"

    # X (Hooked Index)
    elif i and not any([m, r, p, t]):
        if lm[8].y > lm[6].y: # Index tip is lower than the joint
            return "X"

    return "?"