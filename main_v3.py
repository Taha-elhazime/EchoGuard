import cv2 
import numpy as np
import mediapipe as mp
import math 
import time

#Absolute variables
x = 1
y = 1
face_w = 1
face_h = 1
center_x = 1
center_y = 1
bearing = 1
speed = 1
last_x = 1
last_y = 1
dx = 1
dy = 1

#Relative variables

roi_x = 1
roi_y = 1
roi_face_w = 1
roi_face_h = 1
roi_center_x = 1
roi_center_y = 1

#ROI variables

roi_left = 1
roi_top = 1
roi_bottom = 1
roi_right = 1

tracking = False 
round = 0
bearing_done = False
margin = 60

camera = cv2.VideoCapture(0)
cv2.VideoCapture("video.mp4")

mp_face_detection = mp.solutions.face_detection

detector = mp_face_detection.FaceDetection(
    model_selection = 0,
    min_detection_confidence=0.5
)

print(str(camera.isOpened()))

if camera.read():
    print("Success")
else:
    print("no")

last_seen = time.time()

while True:

    success, frame = camera.read()
    height, width, channels = frame.shape

    if not success:
        break
    
    if tracking:
        rgb_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        results = detector.process(rgb_roi)

        if results.detections:
            last_seen = time.time()
            bearing_done = False 

            detection = results.detections[0]
            bbox = detection.location_data.relative_bounding_box

            roi_height, roi_width, channels = roi.shape

            roi_x = int(bbox.xmin * roi_width)
            roi_y = int(bbox.ymin * roi_height)

            roi_face_w = int(bbox.width * roi_width)
            roi_face_h = int(bbox.height * roi_height)

            x = roi_left + roi_x
            y = roi_top + roi_y

            face_w = roi_face_w
            face_h = roi_face_h

            last_x = center_x
            last_y = center_y

            center_x = x + face_w // 2
            center_y = y + face_h // 2

            dy = center_y - last_y
    else:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = detector.process(rgb_frame)

        if time.time() - last_seen >= 0.2 and not bearing_done:

            dx = center_x - (width // 2)
            dy = center_y - (height // 2)

            angle = math.degrees(math.atan2(dy, dx))
            bearing = (90 + angle) % 360

            print(bearing)

            bearing_done = True

        if results.detections:
            last_seen = time.time()
            bearing_done = False 

            detection = results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            tracking = True
            x = int(bbox.xmin * width)
            y = int(bbox.ymin * height)

            face_w = int(bbox.width * width)
            face_h = int(bbox.height * height)

            last_x = center_x
            last_y = center_y

            center_x = x + (face_w // 2)
            center_y = y + (face_h // 2)

            dx = center_x - last_x
            dy = center_y - last_y 

    if results.detections:
        tracking = True
    else:
        tracking = False

    #print(tracking)

    cv2. rectangle(
        frame,
        (x, y),
        (x + face_w, y + face_h),
        (0, 255, 255),
        2
    )

    cv2. circle(
        frame,
        (center_x, center_y),
        5,
        (0, 0, 255),
        -1  
    )

    k = 1.5

    round += 1

    if round == 1:
        x1 = center_x
        y1 = center_y

    if round == 4:
        x2 = center_x 
        y2 = center_y
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        speed = distance
        round = 0
        

    margintg = 60 + int(speed * k) 

    if margintg > margin:
        margin = margintg
    else:
        margin -= 1
    #print(str(margin))
    #print(str(speed))
    print(x, y)


    roi_left = x- margin
    roi_top = y - margin

    roi_right = x + face_w + margin
    roi_bottom = y + face_h + margin
    

    roi_left = max(0, roi_left)
    roi_top = max(0, roi_top)

    roi_right = min(width, roi_right)
    roi_bottom = min(height, roi_bottom)

    roi = frame[roi_top:roi_bottom, roi_left:roi_right]

    cv2.imshow("ROI", roi)
    cv2. imshow("Camera", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows() 
