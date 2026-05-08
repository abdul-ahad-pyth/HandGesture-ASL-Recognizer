# ASL Alphabet Recognizer using MediaPipe

This is a real-time American Sign Language (ASL) alphabet recognition system built with Python, OpenCV, and MediaPipe.

## 🚀 Features
- **Real-time Detection:** 26 letters of the ASL alphabet.
- **Dual Modes:** Press `r` for Recognition and `l` for Learning mode.
- **Hand Landmark Tracking:** High precision tracking using MediaPipe.

# ASL Sign Language Recognition System

This repository contains a real-time American Sign Language (ASL) recognition system powered by **MediaPipe** and **OpenCV**.

## 🖐️ Hand Positions & Signs Guide

Niche di gayi table aapko batati hai ke har letter ko kaise detect kiya jata hai aur hath ki position kya honi chahiye:

| Letter | Hand Position (Kaise banayein) | Detection Logic |
| :--- | :--- | :--- |
| **A** | Muthi (Fist) band karein, angutha (Thumb) side par upar ho. | `up_fingers == 0` + `t` (Thumb) raised |
| **S** | Muthi band, angutha baaki ungliyon ke samne (front) ho. | `up_fingers == 0` + `lm[4].y < lm[3].y` |
| **E** | Muthi band, angutha ungliyon ke niche (tucked) ho. | `up_fingers == 0` + `not t` |
| **B** | Hatheli kholi rakhein, charon ungliyan upar aur sath judi hon. | `up_fingers == 4` + `not t` |
| **D** | Sirf Index finger upar, baaki ungliyan anguthe ke sath mili hon. | `up_fingers == 1` + `i` raised |
| **I** | Sirf sabse choti ungli (Pinky) upar rakhein. | `up_fingers == 1` + `p` raised |
| **L** | Index finger aur Thumb se "L" shape banayein. | `i` aur `t` raised |
| **V** | Index aur Middle finger se "V" ya Peace sign banayein. | `i` aur `m` raised |
| **Y** | Angutha aur Pinky ungli bahar, beech ki ungliyan band. | `p` aur `t` raised |
| **W** | Index, Middle aur Ring finger ko upar "W" shape mein kholien. | `i`, `m`, `r` raised |
| **F** | Index aur Thumb ke tips ko mila kar "OK" sign banayein. | `Distance(4, 8) < 0.05` |
| **G** | Index finger ko ufuqi (horizontal) rukh mein point karein. | `i` up + `not m` (Orientation check) |
| **H** | Index aur Middle finger dono ko horizontal rukh mein rakhein. | `i` + `m` up (Orientation check) |
| **X** | Index finger ko upar karke thoda sa mod (hook) dein. | `i` up + `lm[8].y > lm[6].y` |
| **C** | Poore hath ko "C" ki shape mein curve karein. | `all(fingers)` + `Thumb-Index distance` |

---

## 🚧 Future Roadmap (Missing Letters)

Abhi ye letters code mein add nahi hain aur future updates mein ayenge:
*   **Motion-based:** **J** aur **Z** (Inke liye movement track karni hogi).
*   **Complex Placements:** **K, M, N, O, P, Q, R, T, U**. (Inke liye thumb aur palm ki mazeed barik logic chahiye).

---

## 🛠️ Tech Stack
- Python, OpenCV, MediaPipe

## 🔮 Future Improvements
- Add a **Majority Voting Buffer** to reduce flickering.
- Integrate **Deep Learning (CNN)** for 99% accuracy.
- Motion tracking for dynamic letters like **J** and **Z**.

## 🏁 How to Run
1. `pip install opencv-python mediapipe`
2. `python MAIN_APP.py`

---
Developed by [abdul-ahad-pyth]
