import cv2
import mediapipe as mp
from buttons import Button
import time

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Define calculator button layout
button_values = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+'],
    ['(', ')', 'ANS', 'CLR'],
    ['BCK', '', '', '']  # BCK properly placed
]

# Create Button instances
buttons = []
for y_idx, row in enumerate(button_values):
    for x_idx, val in enumerate(row):
        if val.strip() == '':
            continue  # Skip empty spaces
        x = 100 + x_idx * 120
        y = 120 + y_idx * 120
        buttons.append(Button((x, y), 100, 100, val))

# Expression memory
expression = ""
last_result = ""

# Helper: Get index finger tip
def get_index_tip(hand_landmarks):
    if hand_landmarks:
        lm = hand_landmarks[0].landmark[8]
        return int(lm.x * 1280), int(lm.y * 720)
    return None

# Hover delay before registering tap
HOVER_TRIGGER_FRAMES = 15

# Startup delay or key
print("🕐 Waiting 5 seconds or press 's' to start...")
start_time = time.time()
started = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    if not started:
        cv2.putText(img, "Waiting to Start... (Press 's' or wait 5 sec)", (150, 360),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.imshow("Virtual Calculator", img)

        key = cv2.waitKey(1) & 0xFF
        if time.time() - start_time > 5 or key == ord('s'):
            print("✅ Starting gesture detection...")
            started = True
        elif key == ord('q'):
            break
        continue

    # Hand detection
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    index_tip = None
    if results.multi_hand_landmarks:
        index_tip = get_index_tip(results.multi_hand_landmarks)
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # Draw expression bar
    cv2.rectangle(img, (90, 30), (1010, 100), (20, 20, 20), -1)
    cv2.rectangle(img, (90, 30), (1010, 100), (200, 200, 200), 2)
    cv2.putText(img, expression, (110, 85), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 150), 4)

    # Draw and check buttons
    for button in buttons:
        img = button.draw(img)

        if index_tip and button.is_hover(*index_tip):
            button.hover_counter += 1
            cv2.rectangle(img, button.pos,
                          (button.pos[0] + button.width, button.pos[1] + button.height),
                          (0, 255, 0), 4)

            if button.hover_counter == HOVER_TRIGGER_FRAMES:
                val = button.text
                button.pressed = True

                if val == "=":
                    try:
                        result = str(eval(expression))
                        last_result = result
                        expression = result
                    except:
                        expression = "ERROR"
                elif val == "ANS":
                    expression += last_result
                elif val == "CLR":
                    expression = ""
                elif val == "BCK":
                    expression = expression[:-1]
                else:
                    expression += val
        else:
            button.hover_counter = 0

    # Reset buttons
    for button in buttons:
        if button.pressed:
            button.pressed = False
            button.hover_counter = 0

    # Display window
    cv2.imshow("Virtual Calculator", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()