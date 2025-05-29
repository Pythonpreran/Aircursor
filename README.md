# AirCursor: Gesture-Based Cursor Control

![Python](https://img.shields.io/badge/Python-3.11-blue)

AirCursor is a Python application that enables touchless cursor control using hand gestures captured via a webcam. It uses computer vision and hand tracking to move the mouse cursor, perform left and right clicks, and scroll based on specific hand gestures.

## Features
- **Cursor Movement**: Track the index finger tip to move the cursor across the screen.
- **Left Click**: Pinch gesture (thumb and index finger close together).
- **Right Click**: Index finger folded with thumb held horizontally.
- **Scroll**: Fist gesture with vertical hand movement.
- Real-time hand tracking with visual feedback via webcam feed.

## Demo
*(Add a screenshot or GIF of the application in action here, e.g., hand tracking with cursor movement or clicking. You can generate one using a screen recording tool and upload it to the repository.)*

## Requirements
- Python 3.11
- A webcam
- Required Python packages (see `requirements.txt` below)

### requirements.txt
```txt
opencv-python==4.9.0.80
PyAutoGUI==0.9.54
mediapipe==0.10.21
```

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pythonpreran/Aircursor.git
   cd Aircursor
   ```

2. **Set Up a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure Webcam Access**:
   - Connect a webcam and ensure it’s accessible.
   - Grant camera permissions as needed.

## Usage
1. **Run the Script**:
   ```bash
   python aircursor.py
   ```

2. **Gestures**:
   - **Move Cursor**: Point your index finger to move the cursor.
   - **Left Click**: Pinch thumb and index finger together (distance < 40 pixels).
   - **Right Click**: Fold index finger (tip below DIP joint) and keep thumb horizontal.
   - **Scroll**: Make a fist and move hand vertically to scroll (threshold > 15 pixels).
   - **Exit**: Press `ESC` to close the application.

3. **Visual Feedback**:
   - A window (`AirCursor`) shows the webcam feed with hand landmarks and gesture status (e.g., "Moving", "Left Click Down", "Scrolling").
   - Ensure your hand is well-lit and visible to the webcam.

## How It Works
- **Hand Tracking**: Utilizes [MediaPipe Hands](https://github.com/google/mediapipe) for real-time hand landmark detection.
- **Gesture Detection**:
  - Cursor movement maps the index finger tip’s position to screen coordinates.
  - Left click is triggered when thumb and index finger are close (distance < 40 pixels).
  - Right click requires a folded index finger and horizontal thumb.
  - Scrolling activates with a fist gesture, using vertical hand movement.
- **Dependencies**:
  - `opencv-python`: Handles webcam input and visual output.
  - `PyAutoGUI`: Controls mouse movements, clicks, and scrolling.
  - `mediapipe`: Provides hand tracking functionality.
  - `math.hypot`: Calculates distances between landmarks for gesture detection.

## Configuration
Adjust the following thresholds in `aircursor.py` for better performance:
- `CLICK_THRESHOLD` (default: 40): Distance for pinch-based left click.
- `SCROLL_DIST_THRESHOLD` (default: 15): Minimum vertical movement for scrolling.
- `FIST_DISTANCE_THRESHOLD` (default: 80): Distance to detect a fist for scrolling.

## Troubleshooting
- **Webcam Not Detected**: Verify webcam connection and permissions. Try a different USB port or webcam.
- **Poor Gesture Detection**: Improve lighting, keep hand in frame, or adjust `min_detection_confidence` (default: 0.8) in the code.
- **Lag or Performance Issues**: Reduce webcam resolution or tweak thresholds for responsiveness.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the [Apache 2.0 License](LICENSE).

## Acknowledgments
- [MediaPipe](https://github.com/google/mediapipe) for robust hand tracking.
- [PyAutoGUI](https://github.com/asweigart/pyautogui) for mouse and keyboard control.
- Inspired by innovative touchless interface solutions.

## Contact
For issues or suggestions, open an issue on [GitHub](https://github.com/Pythonpreran/Aircursor/issues) or contact [Pythonpreran](https://github.com/Pythonpreran).
