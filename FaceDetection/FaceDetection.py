import cv2
import time


def DetectFace():
    cascPath = r"haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascPath)
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    obs = []
    startTime = time.time()
    while int(time.time() - startTime) < 2:
        if not video_capture.isOpened():
            obs.append(False)
            continue

        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        if len(faces) == 0:
            obs.append(False)
        else:
            obs.append(True)
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #         # Display the resulting frame
        # cv2.imshow('Video', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #          pass
    video_capture.release()
    cv2.destroyAllWindows()
    return sum(obs) >= 3

