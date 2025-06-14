

This application uses computer vision and pose detection to control the Chrome Dino game (or similar games) using body movements through your webcam. Jump, move left, and move right by moving your body instead of using your keyboard!

## Features

- **Jump Detection**: Jump in real life to make the game character jump
- **Left/Right Movement**: Raise your hands to move the character left or right
- **Visual Feedback**: See your movements tracked in real-time with helpful visual indicators

## Requirements

### Libraries Used

- **OpenCV** (`cv2`): For capturing and processing webcam video
- **MediaPipe**: For pose detection and tracking body landmarks
- **PyAutoGUI**: For simulating keyboard inputs to control the game

## Installation

1. Make sure you have Python installed (Python 3.7+ recommended)
2. Install the required libraries:

```
pip install opencv-python mediapipe pyautogui
```

## How to Run

1. Start the Chrome Dino game (or any game that uses space to jump, 'a' to move left, and 'd' to move right)
   - For Chrome Dino: Open Chrome and navigate to `chrome://dino/` or disconnect from the internet and try to visit any website
2. Run the application:

```
python app.py
```

3. Position yourself in front of the webcam so your upper body is visible
4. The application will open a window showing your webcam feed with pose landmarks

## How to Use

- **To Jump**: Stand up straight, then quickly crouch down and stand up again
- **To Move Left**: Raise your right hand above your shoulder
- **To Move Right**: Raise your left hand above your shoulder
- **To Exit**: Press the 'Esc' key while the webcam window is active

## Visual Indicators

- **Blue Line**: Your baseline position
- **Red Line**: Jump threshold - move above this line to trigger a jump
- **Yellow Line**: Hand movement threshold
- **Text Status**: Shows your current action (Jumping, Moving Left/Right)

## Notes

- Make sure you have good lighting for best pose detection
- Allow camera permissions when prompted
- Stand far enough from the camera so your full upper body is visible
- You might need to adjust the `THRESHOLD` and `H_THRESHOLD` variables in the code for better sensitivity based on your webcam and physical space

## Troubleshooting

- If the application doesn't detect your movements well, try adjusting your position or improving lighting
- If the game doesn't respond to the simulated keypresses, make sure the game window is active/focused
- If the application is slow, try closing other resource-intensive applications
