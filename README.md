# ASL Alphabet Recognizer using MediaPipe

This is a real-time American Sign Language (ASL) alphabet recognition system built with Python, OpenCV, and MediaPipe.

## 🚀 Features
- **Real-time Detection:** 26 letters of the ASL alphabet.
- **Dual Modes:** Press `r` for Recognition and `l` for Learning mode.
- **Hand Landmark Tracking:** High precision tracking using MediaPipe.

## 🖐️ How to Perform Signs (User Guide)
To get the best accuracy, please follow these specific hand orientations:

| Category | Letters | Hand Position |
| :--- | :--- | :--- |
| **Fist** | A, S, T, N, M | Full fist. Pay attention to Thumb placement. |
| **Flat** | B | Palm open, fingers together, thumb tucked. |
| **Circle** | O, C, F | Fingers curved or touching thumb (F is the OK sign). |
| **Point** | D, I, L, Y, Z | Specific fingers extended (e.g., L shape for 'L'). |
| **V-Shape** | V, W, R | Two or three fingers up. For 'R', cross Index and Middle. |
| **Directional**| G, H, P, Q | **G/H:** Point sideways. **P/Q:** Point downwards. |

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
