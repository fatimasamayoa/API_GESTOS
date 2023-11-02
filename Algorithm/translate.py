import base64
import math
from os import abort
import mediapipe as mp
import cv2

diccionarioPalabras = {
    "01000": "ARRIBA O UNO",
}

def translate(content):
    palabra = ''
    image = content
    imgdata = base64.b64decode(image)
    filename = './some_image.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        with mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=1,
                min_detection_confidence=0.5) as hands:
            image = cv2.imread("some_image.jpg")
            height, width, _ = image.shape
            image = cv2.flip(image, 1)  # Comentar si se usa la camara frontal
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = hands.process(image_rgb)
            if results.multi_handedness is None:
                return 'NOT_HANDS'
            label = results.multi_handedness[0].classification[0].label
            print(results.multi_handedness[0].classification[0].label)

            if results.multi_hand_landmarks is not None:

                label = results.multi_handedness[0].classification[0].label  # label gives if hand is left or right
                print(label)
                for handLandmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, handLandmarks, mp_hands.HAND_CONNECTIONS)
                    thumbIsOpen = "0"
                    indexIsOpen = "0"
                    middelIsOpen = "0"
                    ringIsOpen = "0"
                    pinkyIsOpen = "0"

                    pseudoFixKeyPoint = handLandmarks.landmark[5].x

                    if label == 'Right':
                        if handLandmarks.landmark[3].x < pseudoFixKeyPoint and handLandmarks.landmark[4].x < pseudoFixKeyPoint:
                            thumbIsOpen = "1"
                    elif label == 'Left':
                        if handLandmarks.landmark[3].x > pseudoFixKeyPoint and handLandmarks.landmark[4].x > pseudoFixKeyPoint:
                            thumbIsOpen = "1"
                    pseudoFixKeyPoint = handLandmarks.landmark[6].y
                    if handLandmarks.landmark[7].y < pseudoFixKeyPoint and handLandmarks.landmark[8].y < pseudoFixKeyPoint:
                        indexIsOpen = "1"
                    pseudoFixKeyPoint = handLandmarks.landmark[10].y
                    if handLandmarks.landmark[11].y < pseudoFixKeyPoint and handLandmarks.landmark[12].y < pseudoFixKeyPoint:
                        middelIsOpen = "1"

                    pseudoFixKeyPoint = handLandmarks.landmark[14].y
                    if handLandmarks.landmark[15].y < pseudoFixKeyPoint and handLandmarks.landmark[16].y < pseudoFixKeyPoint:
                        ringIsOpen = "1"

                    pseudoFixKeyPoint = handLandmarks.landmark[18].y
                    if handLandmarks.landmark[19].y < pseudoFixKeyPoint and handLandmarks.landmark[20].y < pseudoFixKeyPoint:
                        pinkyIsOpen = "1"

                    resultadoValidacion = thumbIsOpen + indexIsOpen + middelIsOpen + ringIsOpen + pinkyIsOpen
                    if resultadoValidacion in diccionarioPalabras:
                        palabra = diccionarioPalabras[resultadoValidacion]
                    if resultadoValidacion == '10000':
                        if handLandmarks.landmark[4].y < handLandmarks.landmark[5].y:
                            palabra = 'BIEN O DIEZ'
                        else:
                            palabra = 'MAL'
                    elif resultadoValidacion == '11000':
                        if handLandmarks.landmark[4].y < handLandmarks.landmark[5].y:
                            palabra = 'FEBRERO'
                        else:
                            palabra = 'LUNES'
    return palabra
