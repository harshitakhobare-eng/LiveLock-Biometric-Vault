import face_recognition
import cv2
import numpy as np
import vault
import time
from scipy.spatial import distance as dist
from cryptography.fernet import Fernet
import sys

THRESHOLD = 0.7

def get_ear(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def get_turn_direction(landmarks):
    nose = landmarks['nose_bridge'][0]
    left_edge = landmarks['left_eyebrow'][0]
    right_edge = landmarks['right_eyebrow'][-1]
    d_l = dist.euclidean(nose, left_edge)
    d_r = dist.euclidean(nose, right_edge)
    if d_l / d_r > 1.6:
        return "RIGHT"
    if d_r / d_l > 1.6:
        return "LEFT"
    return "CENTER"

def verify_identity(rgb_small):
    all_users = vault.get_all_users()
    encodings = face_recognition.face_encodings(rgb_small)

    if len(encodings) == 0:
        return None

    new_vector = encodings[0].astype(np.float64)

    with open("secret.key", "rb") as f:
        cipher = Fernet(f.read())

    for name, encrypted_blob in all_users:
        decrypted = cipher.decrypt(encrypted_blob)
        raw_vector_data = decrypted[:1024]
        stored_vector = np.frombuffer(raw_vector_data, dtype=np.float64)

        distance_value = dist.euclidean(new_vector, stored_vector)
        print("Distance:", distance_value)

        if distance_value < THRESHOLD:
            return name

    return None

def authenticate():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    challenge_queue = ["LOOK LEFT", "LOOK RIGHT", "BLINK 3 TIMES"]
    current_idx = 0
    authenticated_user = None
    blink_count = 0
    eye_closed = False
    start_time = None
    time_limit = 6

    while current_idx < len(challenge_queue):
        ret, raw_frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(raw_frame, 1)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small)

        target = challenge_queue[current_idx]

        cv2.putText(frame, f"Challenge: {target}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if len(face_locations) > 0:
            if start_time is None:
                start_time = time.time()

            elapsed = time.time() - start_time
            landmarks = face_recognition.face_landmarks(rgb_small, face_locations)

            if landmarks:
                marks = landmarks[0]
                passed = False

                if target == "BLINK 3 TIMES":
                    ear = (get_ear(marks['left_eye']) + get_ear(marks['right_eye'])) / 2.0
                    if ear < 0.20:
                        eye_closed = True
                    elif eye_closed:
                        blink_count += 1
                        eye_closed = False
                        if blink_count >= 3:
                            passed = True

                elif target == f"LOOK {get_turn_direction(marks)}":
                    passed = True

                if passed:
                    authenticated_user = verify_identity(rgb_small)
                    if authenticated_user:
                        break
                    else:
                        current_idx += 1
                        start_time = None
                        blink_count = 0

            if elapsed >= time_limit:
                current_idx += 1
                start_time = None
                blink_count = 0

        cv2.imshow("PrivacyFirst Auth Console", frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if authenticated_user:
        print(f"✅ Verified: {authenticated_user}")
        sys.exit(0)
    else:
        print("🛑 SYSTEM LOCKED")
        sys.exit(1)

if __name__ == "__main__":
    authenticate()