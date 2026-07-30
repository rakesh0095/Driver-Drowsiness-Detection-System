from collections import deque

# -------------------- CONSTANTS --------------------
EAR_THRESHOLD = 0.25
SLEEP_SECONDS = 5
SMOOTHING_WINDOW = 5

# Global runtime variables
sleep_start_time = None
alarm_playing = False
alert_logged = False
ear_buffer = deque(maxlen=SMOOTHING_WINDOW)

# Eye Landmark Indices
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
