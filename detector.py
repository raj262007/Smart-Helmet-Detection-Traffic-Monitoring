
import cv2
from ultralytics import YOLO
model = YOLO('models/best.pt') # downloads automatically on first run

# Class names from data.yaml
HELMET_CLASS = "with helmet"
NO_HELMET_CLASS = "without helmet"

def detect_frame(frame):
    # Run YOLO detection on the frame
    results = model(frame, verbose=False)

    with_helmet = 0
    without_helmet = 0

    for result in results:
        boxes = result.boxes

        if boxes is None:
            continue

        for box in boxes:
            # Get confidence score and class name
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Skip low confidence detections
            if confidence < 0.5:
                continue

            # Get box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Check if helmet or no helmet
            if HELMET_CLASS in class_name.lower():
                with_helmet += 1
                color = (0, 255, 0)   # Green for safe
                label = f"Helmet {confidence:.2f}"
            else:
                without_helmet += 1
                color = (0, 0, 255)   # Red for violation
                label = f"No Helmet {confidence:.2f}"

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Draw label background
            cv2.rectangle(frame, (x1, y1 - 25), (x1 + len(label) * 10, y1), color, -1)

            # Draw label text
            cv2.putText(
                frame, label,
                (x1, y1 - 7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2
            )

    # Show warning if violation found
    if without_helmet > 0:
        cv2.putText(
            frame,
            f"!! VIOLATION DETECTED: {without_helmet} !!",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0, (0, 0, 255), 3
        )

    return frame, with_helmet, without_helmet