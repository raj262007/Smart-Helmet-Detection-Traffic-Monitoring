# main.py

import cv2
import os
from detector import detect_frame
from logger import setup_csv, log_violation
from database import create_table

# ── Settings ──────────────────────────────────────────
VIDEO_SOURCE = 0          # 0 = webcam, or write "video.mp4" for video file
SNAPSHOT_DIR = "snapshots"
LOG_EVERY_N_FRAMES = 30   # log data every 30 frames
SAVE_SNAPSHOT = True      # save screenshot of violation or not

# ── Setup ─────────────────────────────────────────────
create_table()
setup_csv()
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# ── Counters ──────────────────────────────────────────
total_vehicles = 0
total_safe = 0
total_violations = 0
frame_count = 0

# ── Open Video Source ─────────────────────────────────
cap = cv2.VideoCapture(VIDEO_SOURCE)

if not cap.isOpened():
    print("Error: Could not open video source!")
    exit()

print("System is running... Press 'q' to quit")

# ── Main Loop ─────────────────────────────────────────
while True:
    ret, frame = cap.read()

    if not ret:
        print("Video ended or camera disconnected!")
        break

    frame_count += 1

    # Run detection on current frame
    annotated_frame, safe, violation = detect_frame(frame)

    # Update counters
    total_vehicles += (safe + violation)
    total_safe += safe
    total_violations += violation

    # Show stats on frame
    cv2.putText(annotated_frame, f"Total Vehicles : {total_vehicles}",
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(annotated_frame, f"Safe           : {total_safe}",
                (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(annotated_frame, f"Violations     : {total_violations}",
                (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Log every 30 frames if violation found
    if frame_count % LOG_EVERY_N_FRAMES == 0 and violation > 0:

        # Save snapshot
        image_path = ""
        if SAVE_SNAPSHOT:
            image_path = f"{SNAPSHOT_DIR}/violation_{frame_count}.jpg"
            cv2.imwrite(image_path, annotated_frame)

        # Log to CSV and database
        log_violation(total_vehicles, total_safe, total_violations, image_path)

    # Show the frame
    cv2.imshow("Smart Helmet Detection System", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("System stopped.")