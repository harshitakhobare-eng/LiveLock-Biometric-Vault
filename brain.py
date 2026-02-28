import face_recognition
import cv2
import numpy as np

def boost_low_light(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl,a,b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

def get_texture_score(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = boost_low_light(frame)
    t_score = get_texture_score(frame)
    texture_label = "REAL" if t_score > 100 else "POTENTIAL SPOOF"

    cv2.putText(processed_frame, f"Texture: {int(t_score)} ({texture_label})", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Innovative AI Brain', processed_frame)

    key = cv2.waitKey(100)

    if key & 0xFF == ord('s'):
        rgb_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_frame)

        if len(encodings) > 0 and t_score > 100:
            privacy_vector = encodings[0]
            print("Vector Length:", len(privacy_vector))
            print("First 5 values:", privacy_vector[:5])
            break

    elif key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()