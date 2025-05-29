import cv2
import pyautogui
import mediapipe as mp
from math import hypot

# Setup
cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# State variables
left_clicking = False
right_clicking = False
scroll_mode = False
last_scroll_y = None

# Thresholds
CLICK_THRESHOLD = 40
SCROLL_DIST_THRESHOLD = 15
FIST_DISTANCE_THRESHOLD = 80

def get_coords(lm, idx, shape):
    h, w, _ = shape
    return int(lm[idx].x * w), int(lm[idx].y * h)

def distance(p1, p2):
    return hypot(p1[0] - p2[0], p1[1] - p2[1])

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

            index_tip = get_coords(lm, 8, img.shape)
            index_dip = get_coords(lm, 6, img.shape)
            thumb_tip = get_coords(lm, 4, img.shape)
            thumb_ip = get_coords(lm, 3, img.shape)
            base = get_coords(lm, 0, img.shape)

            # Calculate distances
            dist_thumb_index = distance(index_tip, thumb_tip)

            # Fist detection for scroll mode
            finger_indices = [8, 12, 16, 20]
            distances_to_base = [distance(get_coords(lm, i, img.shape), base) for i in finger_indices]
            is_fist = all(d < FIST_DISTANCE_THRESHOLD for d in distances_to_base)

            if is_fist:
                if not scroll_mode:
                    scroll_mode = True
                    last_scroll_y = base[1]
                else:
                    delta = last_scroll_y - base[1]
                    if abs(delta) > SCROLL_DIST_THRESHOLD:
                        pyautogui.scroll(int(delta))
                        last_scroll_y = base[1]
                cv2.putText(img, "Scrolling", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                continue
            else:
                scroll_mode = False

            # Movement only if not pinching
            if dist_thumb_index > CLICK_THRESHOLD:
                screen_x = int(lm[8].x * screen_w)
                screen_y = int(lm[8].y * screen_h)
                pyautogui.moveTo(screen_x, screen_y)
                cv2.putText(img, "Moving", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

            # Left click gesture: index and thumb near
            if dist_thumb_index < CLICK_THRESHOLD:
                if not left_clicking:
                    pyautogui.mouseDown()
                    left_clicking = True
                    cv2.putText(img, "Left Click Down", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            else:
                if left_clicking:
                    pyautogui.mouseUp()
                    left_clicking = False
                    cv2.putText(img, "Left Click Up", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 200), 2)

            # Right click gesture: index bent (tip below DIP) and thumb horizontal (not angled)
            index_folded = index_tip[1] > index_dip[1]
            thumb_horiz = abs(thumb_tip[1] - thumb_ip[1]) < 20

            if index_folded and thumb_horiz and dist_thumb_index > CLICK_THRESHOLD:
                if not right_clicking:
                    pyautogui.mouseDown(button='right')
                    right_clicking = True
                    cv2.putText(img, "Right Click Down", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                if right_clicking:
                    pyautogui.mouseUp(button='right')
                    right_clicking = False
                    cv2.putText(img, "Right Click Up", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 180), 2)

    cv2.imshow("AirCursor", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
