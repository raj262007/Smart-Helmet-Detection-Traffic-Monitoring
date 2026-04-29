# 🪖 Smart Helmet Detection & Traffic Monitoring System

Real-time AI system that detects two-wheeler riders and
identifies helmet violations using YOLOv8 and OpenCV.

---

## 🚀 Features

- Real-time helmet detection using YOLOv8
- Violation logging with timestamp (CSV + SQLite)
- Live Streamlit dashboard
- Downloadable Excel reports
- Violation snapshots saved automatically

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Main programming language |
| YOLOv8 | Object detection model |
| OpenCV | Video processing |
| Streamlit | Live dashboard |
| Pandas | Data handling |
| SQLite | Database storage |

---

## ▶️ How to Run

### 1. Create virtual environment

py -3.11 -m venv venv
venv\Scripts\activate

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run detection
python main.py

### 4. Run dashboard (new terminal)
streamlit run dashboard.py

---

## 📁 Project Structure
smart-helmet-detection/
├── main.py          # Main detection script
├── detector.py      # YOLO detection logic
├── logger.py        # CSV + DB logging
├── database.py      # Database setup
├── dashboard.py     # Streamlit dashboard
├── requirements.txt # Dependencies
├── data/            # CSV + DB files
├── models/          # YOLO model weights
├── snapshots/       # Violation screenshots
└── reports/         # Excel reports

---

## 📊 Model Performance

| Class | mAP50 |
|-------|-------|
| With Helmet | 88.6% |
| Without Helmet | 84.9% |
| Overall | 86.8% |

---

## 🔮 Future Enhancements

- Number plate recognition (ANPR)
- Multi-camera support
- Mobile alerts for violations
- Cloud deployment
- Night vision support

---

## 📍 Real World Applications

- Traffic police monitoring
- Smart city surveillance
- Highway toll booths
- Construction site safety
- School/college zone monitoring


