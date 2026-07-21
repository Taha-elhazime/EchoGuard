import cv2 
import numpy as np
import time
import mediapipe as mp
import math
import serial

arduino = serial.Serial("COM3", 115200)
esp = serial.Serial("COM7", 115200)
time.sleep(2)

mode = 0
prKey = -1

position1X = 0
position1Y = 0
position2X = 0
position2Y = 0

round = 0
speed = 0

x = 1
y = 1
center_x = 2
center_y = 2
width = 1
height = 1
face_h = 1
face_w = 1
red = 1

sensor = 0

camera = cv2.VideoCapture(0)
cv2.VideoCapture("video.mp4")

mp_face_detection = mp.solutions.face_detection

detector = mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

print (str(camera.isOpened()))

if camera.read():
    print("Success")
else:
    print("nope")

while True:

    success, frame = camera.read()
    height, width, channels = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = detector.process(rgb_frame)
    tracking = results.detections is not None

   
    
    blue = speed // 5.8

    if results.detections:
        for detection in results.detections:

            bbox = detection.location_data.relative_bounding_box



            x = int(bbox.xmin * width)
            y = int(bbox.ymin * height)
            face_w = int(bbox.width * width)
            face_h = int(bbox.height * height)

            center_x = x + face_w // 2
            center_y = y + face_h // 2

        #Speed

            round = round + 1

            if round == 6:
                position1X = x 
                position1Y = y
            
            if round == 16:
                position2X = x
                position2Y = y
                round = 0

                speed = 10*(math.sqrt((position1X - position2X)**2 + (position1Y - position2Y)**2))


            cv2.rectangle(
                frame,
                (x, y),
                (x + face_w, y + face_h),
                (red, 0, 0),
                2
            )

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 255, 0),
                -1
            )

            cv2.line(
                frame,
                (width // 2, height // 2 ),
                (center_x, center_y),
                (0, 255, 0),
                1
            )


    #Area ratio

    area = height * width

    areaF = face_h * face_w

    areaR = areaF / area
    
    #print("ratio: " + str(areaR))

    #-------------------------------------------------------------------

    dy = -(center_y - (height // 2))

    dx = -(center_x - (width // 2))


    

    angle = math.degrees(math.atan2(dy, dx))
    bearing = (90 - angle) % 360
    #print(str(bearing)) 

    if esp.in_waiting:
        sensor = int(esp.readline().decode().strip())

    if tracking:
        arduino.write(f"{dx},{dy},{int(tracking)},0,{sensor}\n".encode())
    else:
        arduino.write(f"0,0,{int(tracking)},{int(bearing)},{sensor}\n".encode())

    print(bearing)



    cv2.imshow("camera", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

camera.release()

cv2.destroyAllWindows() 