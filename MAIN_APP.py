import mediapipe as mp
import cv2
import numpy as np
import time
import datetime
from ASL_LEARNER import hands
from ASL_LEARNER import mp_hands
from ASL_LEARNER import mp_drawing
from ASL_LEARNER import mp_drawing_styles
from ASL_FUNCTION import get_hand_state
from ASL_FUNCTION import recognize_asl
cap=cv2.VideoCapture(0)
prev_time = time.time()
letter="?"
mode = "recognize"  or "learn"
print("ASL Learner Started!")
print("Press 'L' for Learn Mode | 'R' for Recognize Mode | 'Q' to Quit")
while cap.isOpened():
    ret,frame=cap.read()
    if not ret:
        break
    flip=cv2.flip(frame,1)
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            fingers=get_hand_state(hand_landmarks)
            letter=recognize_asl(fingers,hand_landmarks)
    color=(0,255,0) if letter!="?" else(0,0,255)
    cv2.putText(frame,f" letter={letter}",(30,80),
         cv2.FONT_HERSHEY_COMPLEX,2.5,color,5)
    mode_text = "LEARN MODE - Practice the letter" if mode == "learn" else "RECOGNIZE MODE"
    cv2.putText(frame, mode_text, (30, 130),
    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
 # FPS
    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time))
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {fps}", (30, 170),
    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow('ASL Sign Language Learner - A to Z', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('l'):
          mode = "learn"
    elif key == ord('r'):
          mode = "recognize" 
    elif key==ord('s'):
         import datetime
    # Time ke sath unique filename banayega
         filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
         cv2.imwrite(filename, frame)
         print(f"Screenshot saved as {filename}")    
cap.release()
cv2.destroyAllWindows()

