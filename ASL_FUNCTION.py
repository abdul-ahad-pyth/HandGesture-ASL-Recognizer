

def get_hand_state(hand_landmarks):
    landmarks = hand_landmarks.landmark
    
    tips=[4,8,12,16,20]
    pips=[3,6,10,14,18]
    fingers=[]
    thumb_up=(landmarks[4].x<landmarks[3].x) if (landmarks[0].x<landmarks[9].x) else(landmarks[4].x>landmarks[3].x)
    fingers.append(thumb_up)
    for tip,pip in zip (tips[1:],pips[1:]):
        fingers.append(landmarks[tip].y<landmarks[pip].y)
    return fingers
def recognize_asl(fingers,landmarks):
    t,i,m,r,p=fingers
    lm=landmarks.landmark
    up_count=sum(fingers)
    
    # F (OK Sign)
    dist_f = ((lm[8].x - lm[4].x)**2 + (lm[8].y - lm[4].y)**2)**0.5
    if dist_f < 0.05 and m and r and p: return "F"

    # O (Circle) - Saari ungliyan thumb ke qareeb
    dist_o = ((lm[8].x - lm[4].x)**2 + (lm[12].y - lm[4].y)**2)**0.5
    if dist_o < 0.06 and up_count == 0: return "O"

    # C (Cup Shape)
    if not any(fingers) and lm[8].x > lm[6].x and lm[4].x < lm[2].x: return "C"

    # X (Hooked Index)
    if i and not m and lm[8].y > lm[6].y: return "X"

    # K (V with Thumb in middle)
    if i and m and abs(lm[4].y - lm[10].y) < 0.05: return "K"

    # U (Joined Fingers)
    dist_u = abs(lm[8].x - lm[12].x)
    if i and m and dist_u < 0.03: return "U"

    # --- 2. Fist Variations (A, E, M, N, S, T) ---
    if up_count == 0:
        # E (Fingers tucked in)
        if lm[8].y > lm[6].y and lm[12].y > lm[10].y: return "E"
        # A (Thumb on side)
        if lm[4].x < lm[3].x and lm[4].y < lm[6].y: return "A"
        # S (Thumb over fingers)
        if lm[4].y > lm[10].y and lm[4].x > lm[6].x: return "S"
        # T (Thumb between Index and Middle)
        if lm[4].x > lm[6].x and lm[4].x < lm[10].x: return "T"
        # N (Thumb under Middle)
        if lm[4].x > lm[10].x and lm[4].x < lm[14].x: return "N"
        # M (Thumb under Ring)
        return "M"

    # --- 3. Straight Up Logic ---
    if fingers == [False, True, True, True, True]: return "B"
    if fingers == [False, True, False, False, False]: return "D"
    if fingers == [False, False, False, False, True]: 
        # J (Pinky with a slight curve/motion - Static approximation)
        if lm[20].x < lm[18].x: return "J" 
        return "I"
    if fingers == [True, True, False, False, False]: return "L"
    if fingers == [False, True, True, False, False]:
        if lm[12].x < lm[8].x: return "R"
        return "V"
    if fingers == [False, True, True, True, False]: return "W"
    if fingers == [True, False, False, False, True]: return "Y"

    # --- 4. Pointing & Directional (G, H, P, Q, Z) ---
    
    # Sideways (G, H)
    if abs(lm[8].y - lm[5].y) < 0.05:
        if i and m: return "H"
        if i: return "G"

    # Downwards (P, Q)
    if lm[8].y > lm[5].y:
        if i and m: return "P"
        if i: return "Q"

    # Z (Index pointing and moving - Static approximation)
    if i and not m and not r and not p and abs(lm[8].z) > 0.02: return "Z"

    return "?"
   
   