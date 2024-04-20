import cv2
import mediapipe as mp
from DroneBlocksTelloSimulator import SimulatedDrone

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

sim_key = '6b1c8aa2-db2b-40cd-acaf-8dbdf8307bdc'#key that you can find on https://coding-sim.droneblocks.io/
drone = SimulatedDrone(sim_key)

cap = cv2.VideoCapture(0)
hands = mp_hands.Hands()

while True:
    ret, image = cap.read()
    if not ret:
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    finger_status = [0, 0, 0, 0, 0]  # Initialize finger status array

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


    if finger_status == [0, 0, 0, 0, 0]:
        pass  #Do nothing
    elif finger_status == [0, 1, 0, 0, 0]:
        drone.fly_up(50, 'cm')  #akeoff
    elif finger_status == [0, 1, 1, 0, 0]:
        drone.land()  #Land
    elif finger_status ==[0, 1, 0, 0, 1]:
        drone.fly_left(50, 'cm') #backflip
    elif finger_status == [0, 0, 0, 0, 1]:
        drone.fly_forward(50, 'cm')  #fly forward
    elif finger_status == [0, 0, 1, 0, 1]:
        drone.fly_backward(50, 'cm')  #fly forward
    elif finger_status == [1, 1, 1, 1, 1]:
        drone.fly_right(50, 'cm')  #Land
    elif finger_status == [0, 0, 1, 0, 0]:
        drone.flip_right()  #Land

    print(finger_status)  #Print fingers

    cv2.imshow("Hand Tracker", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()