import face_recognition
import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        cv2.putText(frame, "Align Face & Press 's' to Capture", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Enrollment Console', frame)
        key = cv2.waitKey(30) & 0xFF

        if key == ord('s'):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)
            if len(encodings) > 0:
                np.save("temp_face.npy", encodings[0].astype(np.float64))
                break

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()