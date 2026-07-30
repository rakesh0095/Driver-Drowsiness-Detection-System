import cv2
import numpy as np
import mediapipe as mp
from scipy.spatial import distance
import time
from playsound import playsound
import threading
import csv
from datetime import datetime

# ---- import config variables ----
from config import (
    EAR_THRESHOLD, SLEEP_SECONDS, SMOOTHING_WINDOW,
    sleep_start_time, alarm_playing, alert_logged, ear_buffer,
    LEFT_EYE_INDICES, RIGHT_EYE_INDICES
)

# -------------------- FUNCTIONS --------------------
def calculate_EAR(eye_points):
    A = distance.euclidean(eye_points[1], eye_points[5])
    B = distance.euclidean(eye_points[2], eye_points[4])
    C = distance.euclidean(eye_points[0], eye_points[3])
    return (A + B) / (2.0 * C)

def smooth_ear(ear):
    ear_buffer.append(ear)
    return sum(ear_buffer) / len(ear_buffer)

def play_alarm():
    global alarm_playing
    alarm_playing = True
    while alarm_playing:
        try:
            playsound("alarm.wav")
        except:
            playsound("alarm.mp3")

def log_alert(alert_type, ear_val, duration):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("alerts.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, alert_type, f"{ear_val:.3f}", f"{duration:.2f}"])

# -------------------- MEDIAPIPE SETUP --------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -------------------- CAMERA --------------------
cap = cv2.VideoCapture(0)
print("Sleep Detection started...")

# -------------------- MAIN LOOP --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    h, w, _ = frame.shape

    frame.flags.writeable = False
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    frame.flags.writeable = True

    EAR = 0
    face_detected = False

    if results.multi_face_landmarks:
        face_detected = True
        lm = results.multi_face_landmarks[0].landmark

        left_eye = np.array([(int(lm[p].x * w), int(lm[p].y * h))
                             for p in LEFT_EYE_INDICES])
        right_eye = np.array([(int(lm[p].x * w), int(lm[p].y * h))
                              for p in RIGHT_EYE_INDICES])

        left_ear = calculate_EAR(left_eye)
        right_ear = calculate_EAR(right_eye)

        EAR = smooth_ear((left_ear + right_ear) / 2)

        cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
        cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)

        if EAR < EAR_THRESHOLD:
            if sleep_start_time is None:
                sleep_start_time = time.time()
                alert_logged = False

            elapsed = time.time() - sleep_start_time

            cv2.putText(frame, f"Eyes Closed: {elapsed:.1f}s", (20, 440),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            if elapsed >= SLEEP_SECONDS:
                cv2.putText(frame, "!!! SLEEPING ALERT !!!",
                            (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2,
                            (0, 0, 255), 5)

                if not alarm_playing:
                    threading.Thread(target=play_alarm, daemon=True).start()

                if not alert_logged:
                    log_alert("SLEEP_ALERT", EAR, elapsed)
                    alert_logged = True

        else:
            if sleep_start_time is not None:
                duration = time.time() - sleep_start_time
                if duration >= SLEEP_SECONDS:
                    log_alert("EYES_OPENED", EAR, duration)

            sleep_start_time = None
            if alarm_playing:
                alarm_playing = False

    else:
        sleep_start_time = None
        ear_buffer.clear()
        if alarm_playing:
            alarm_playing = False

    cv2.putText(frame, f"EAR: {EAR:.3f}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    status_text = "Face Detected" if face_detected else "No Face"
    cv2.putText(frame, status_text, (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 150), 2)

    cv2.imshow("Sleep Detection System", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()



