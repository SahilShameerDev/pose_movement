import cv2
import mediapipe as mp
import pyautogui

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
# Optimize Mediapipe for faster processing
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=0  # Use a simpler model for faster processing
)
cap = cv2.VideoCapture(0)

# Create a named window first so we can resize it
cv2.namedWindow('Jump Detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Jump Detection', 640, 480)

# Initial Y position
baseline_y = None
triggered = False
left_pressed = False
right_pressed = False

THRESHOLD = 10
H_THRESHOLD = -10

# Track whether keys are currently held down
a_key_down = False
d_key_down = False

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Process image without unnecessary operations
    frame = cv2.flip(frame, 1)
    # Convert to RGB efficiently
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process with MediaPipe
    results = pose.process(rgb)

    # Draw the pose landmarks on the image
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        
        l_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        r_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        l_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        r_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        avg_y = l_shoulder.y

        if baseline_y is None:
            baseline_y = avg_y

        y_diff = baseline_y - avg_y  # how much user moved up

        # Draw visualization elements
        h, w, _ = frame.shape
        baseline_y_px = int(baseline_y * h)
        cv2.line(frame, (0, baseline_y_px), (w, baseline_y_px), (255, 0, 0), 2)
        
        threshold_y_px = int((baseline_y - THRESHOLD/100) * h)
        cv2.line(frame, (0, threshold_y_px), (w, threshold_y_px), (0, 0, 255), 2)
        
        h_threshold_y_px = int((baseline_y - H_THRESHOLD/100) * h)
        cv2.line(frame, (0, h_threshold_y_px), (w, h_threshold_y_px), (0, 255, 255), 2)
        
        # Debug info
        cv2.putText(frame, f"Y Diff: {y_diff:.2f}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show jump status
        status = "JUMPING!" if triggered else "Ready"
        cv2.putText(frame, status, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if triggered else (255, 0, 0), 2)

        # FIXING THE JUMP LOGIC: When user moves up, press space
        if y_diff > THRESHOLD / 100 and not triggered:
            pyautogui.press('space')
            triggered = True
        elif y_diff < THRESHOLD / 200:  # reset when user comes down
            triggered = False
            
        # FIXING THE HAND MOVEMENT LOGIC:
        # Left hand raised - press A
        left_hand_raised = l_wrist.y < l_shoulder.y - H_THRESHOLD/100
        # Right hand raised - press D
        right_hand_raised = r_wrist.y < r_shoulder.y - H_THRESHOLD/100

        # Handle the A key (left)
        if left_hand_raised and not a_key_down:
            pyautogui.keyDown('d')
            a_key_down = True
            h_status_left = "Moving Left"
        elif not left_hand_raised and a_key_down:
            pyautogui.keyUp('d')
            a_key_down = False
            h_status_left = ""
        else:
            h_status_left = "Moving Left" if a_key_down else ""

        # Handle the D key (right)
        if right_hand_raised and not d_key_down:
            pyautogui.keyDown('a')
            d_key_down = True
            h_status_right = "Moving Right"
        elif not right_hand_raised and d_key_down:
            pyautogui.keyUp('a')
            d_key_down = False
            h_status_right = ""
        else:
            h_status_right = "Moving Right" if d_key_down else ""

        # Display movement status
        h_status = h_status_left + (" & " if h_status_left and h_status_right else "") + h_status_right
        if not h_status:
            h_status = "No Movement"
        cv2.putText(frame, h_status, (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Jump Detection', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Ensure all keys are released when exiting
if a_key_down:
    pyautogui.keyUp('a')
if d_key_down:
    pyautogui.keyUp('d')

cap.release()
cv2.destroyAllWindows()
