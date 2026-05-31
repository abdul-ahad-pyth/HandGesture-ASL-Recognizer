import cv2
import time
import datetime
from collections import Counter

from ASL_LEARNER import hands, mp_hands, mp_drawing, mp_drawing_styles
from ASL_FUNCTION import get_hand_state, recognize_asl

# ─────────────────────────────────────────────
#  LEVEL 3 — STABILITY BUFFER
#  Pehle: har frame mein letter badalta tha (flickering)
#  Ab   : last 10 frames ka sabse common letter dikhao
# ─────────────────────────────────────────────
BUFFER_SIZE  = 10
letter_buffer = []

cap       = cv2.VideoCapture(0)
prev_time = time.time()
letter    = "?"
mode      = "recognize"

print("ASL Learner Started!")
print("Press 'L' for Learn Mode | 'R' for Recognize Mode | 'Q' to Quit | 'S' for Screenshot")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror flip — natural feel ke liye
    frame     = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results   = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Hand skeleton draw karo
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            # ── UPGRADED: fingers + extras dono aate hain ──
            fingers, extras = get_hand_state(hand_landmarks)
            detected        = recognize_asl(fingers, extras)

            # ── BUFFER: flickering band karo ──────────────
            letter_buffer.append(detected)
            if len(letter_buffer) > BUFFER_SIZE:
                letter_buffer.pop(0)

            # Sabse zyada baar aane wala letter dikhao
            letter = Counter(letter_buffer).most_common(1)[0][0]

    else:
        # Hath nahi dikh raha — buffer clear karo
        letter_buffer.clear()
        letter = "?"

    # ── Display ───────────────────────────────────────────
    color = (0, 255, 0) if letter != "?" else (0, 0, 255)

    cv2.putText(frame, f"Letter: {letter}", (30, 80),
                cv2.FONT_HERSHEY_COMPLEX, 2.5, color, 5)

    mode_text = "LEARN MODE - Practice the letter" if mode == "learn" else "RECOGNIZE MODE"
    cv2.putText(frame, mode_text, (30, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # FPS counter
    curr_time = time.time()
    fps       = int(1 / (curr_time - prev_time + 1e-6))
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {fps}", (30, 170),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Buffer mein kitne unique letters hain — debug ke liye
    cv2.putText(frame, f"Buffer: {list(letter_buffer)}", (30, 210),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

    cv2.imshow("ASL Sign Language Learner - A to Z", frame)

    # ── Key Controls ──────────────────────────────────────
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('l'):
        mode = "learn"
        print("Switched to LEARN MODE")
    elif key == ord('r'):
        mode = "recognize"
        print("Switched to RECOGNIZE MODE")
    elif key == ord('s'):
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Screenshot saved: {filename}")

cap.release()
cv2.destroyAllWindows()
print("ASL Session Ended.")