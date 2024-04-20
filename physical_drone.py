#Regular imports
import cv2, random, time, math
import mediapipe as mp

#Drone imports
from djitellopy import Tello

# #Drone setup
tello = Tello()
tello.connect()
print(tello.get_battery())
# tello.move_up(50) #test if drone can move up and forward without any problems
# tello.move_forward(100)

mp_drawing = mp.solutions.drawing_utils #imports utility library
mp_hands = mp.solutions.hands #imports "hands"

#global constants and window
window_name = 'Kinda Flying Drone'
window_width = 380
window_height = 220

# Initialize finger status array
finger_status = [0, 0, 0, 0, 0]

#Function to update circle position based on finger status
def update_circle_position():
    global tello
    if finger_status == [0, 1, 0, 0, 0]: #fingers structure [thumb, pointer, midle finger, ring, pinky]
        tello.move_up(20) #Move circle up
    elif finger_status == [0, 1, 1, 0, 0]:
        tello.move_down(20) #move circle down
    elif finger_status == [0, 0, 0, 0, 1]:
        tello.land() #move right
    elif finger_status == [0, 1, 0, 0, 1]:
        tello.takeoff()
    else:
        pass


cap = cv2.VideoCapture(0) #initialize camera
hands = mp_hands.Hands() #initialize hand

while True: #while loop that runs the code no matter an error
    ret, image = cap.read()
    if not ret:
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) #flip the image, Indian guy told me to
    results = hands.process(image)  #hand landmark detection
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #conversion to RGB

    finger_status = [0, 0, 0, 0, 0]  # Reset finger status array
    #Fx:
    #[0, 0, 0, 0, 0]for fist or no fingers is extended
    #[1, 0, 0, 0, 0] for thumb
    #[0, 1, 0, 0, 0] for index finger and so on

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Check thumb
            if hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y and hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                finger_status[0] = 1
            # Check index finger
            if hand_landmarks.landmark[8].y < hand_landmarks.landmark[5].y:
                finger_status[1] = 1
            # Check middle finger
            if hand_landmarks.landmark[12].y < hand_landmarks.landmark[9].y:
                finger_status[2] = 1
            # Check ring finger
            if hand_landmarks.landmark[16].y < hand_landmarks.landmark[13].y:
                finger_status[3] = 1
            # Check pinky finger
            if hand_landmarks.landmark[20].y < hand_landmarks.landmark[17].y:
                finger_status[4] = 1

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS)

    update_circle_position()  # Update circle position and color based on finger status
    # draw_circle(image)  # Draw circle on image

    #display the results in a window
    cv2.imshow(window_name, image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()