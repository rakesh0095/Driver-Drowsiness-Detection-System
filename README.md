# 🚗 Driver Drowsiness Detection System

A real-time Driver Drowsiness Detection System developed using **Python, OpenCV, and MediaPipe**. The system monitors the driver's eyes through a webcam and detects drowsiness using the Eye Aspect Ratio (EAR). When the driver's eyes remain closed for a specific duration, an alarm is triggered to help prevent accidents.

---

## 🚀 Features

- Real-time face and eye detection
- Eye Aspect Ratio (EAR) calculation
- Driver drowsiness detection
- Audio alarm notification
- Alert logging in CSV file
- Live webcam monitoring

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- SciPy
- Playsound

---

## 📂 Project Structure

```
Driver-Drowsiness-Detection-System/
│── detection.py
│── config.py
│── alarm.wav
│── alerts.csv
│── requirements.txt
│── README.md
```

---

## ⚙️ Prerequisites

- Python 3.9 or above
- Webcam
- pip

Install required packages:

```bash
pip install opencv-python mediapipe numpy scipy playsound
```

---

## ▶️ How to Run

1. Clone the repository

```bash
git clone https://github.com/rakesh0095/Driver-Drowsiness-Detection-System.git
```

2. Navigate to the project folder

```bash
cd Driver-Drowsiness-Detection-System
```

3. Install the required dependencies.

4. Run the application

```bash
python detection.py
```

---

## 📌 How It Works

- Detects the driver's face using MediaPipe Face Mesh.
- Calculates the Eye Aspect Ratio (EAR).
- Continuously monitors eye movements.
- If the eyes remain closed for a predefined time, an alarm is played.
- Saves alert details in a CSV file for future analysis.

---

## 📸 Output

- Real-time webcam feed
- Eye landmarks detection
- Drowsiness warning
- Alarm notification
- Alert logs

---

## 🔮 Future Enhancements

- Mobile notification support
- Email alert system
- Head pose detection
- Yawning detection
- Dashboard for alert history

---

## 👨‍💻 Author

**Rakesh Kumar**

GitHub: https://github.com/rakesh0095

LinkedIn: https://www.linkedin.com/in/rakesh-kumar-3307b2224/

---

⭐ If you found this project useful, please consider giving it a star.
