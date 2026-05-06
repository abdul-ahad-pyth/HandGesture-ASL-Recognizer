# ASL Alphabet Recognizer using MediaPipe

This is a real-time American Sign Language (ASL) alphabet recognition system built with Python, OpenCV, and MediaPipe. The project uses hand landmark detection to identify 26 letters of the alphabet based on finger states and distance-based logic.

## 🚀 Features
- **Real-time Detection:** High-speed hand tracking using MediaPipe.
- **Full A-Z Support:** Logic included for all 26 English alphabets.
- **Dual Modes:** 
  - `Recognize Mode`: Detects signs in real-time.
  - `Learn Mode`: Practice specific letters.
- **Visual Feedback:** Dynamic color changes and FPS counter on the screen.

## 🛠️ Tech Stack
- **Python**
- **OpenCV** (Computer Vision)
- **MediaPipe** (Hand Tracking)

## 📂 Project Structure
- `MAIN_APP.py`: The entry point of the application.
- `ASL_FUNCTION.py`: Contains the logic for finger states and sign recognition.
- `l.py`: MediaPipe initialization and helper configurations.

## ⚠️ Known Issues & Accuracy
> **Note:** This project is a prototype based on static geometric logic.
- **Lighting Sensitivity:** Accuracy may drop in low-light environments.
- **Hand Orientation:** Works best when the hand is directly facing the camera.
- **Static J & Z:** Since J and Z are motion-based, they are currently mapped to their final static positions.
- **Flickering:** Due to raw landmark data, some letters might flicker between similar shapes (e.g., M, N, T).

## 🔮 Future Improvements
- [ ] Implement a **Temporal Buffer** (Majority Voting) to stop flickering.
- [ ] Train a **Deep Learning Model (CNN/LSTM)** for higher accuracy.
- [ ] Add **Motion Tracking** for dynamic letters (J and Z).
- [ ] Support for Left-Handed users.

## 🏁 How to Run
1. Install dependencies:
   ```bash
   pip install opencv-python mediapipe