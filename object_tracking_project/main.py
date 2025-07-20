import cv2
from ultralytics import YOLO
import numpy as np
import time

# Ask user for input source
source = input("Enter '0' for webcam or path to video file: ")
if source == '0':
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(source)

# Load YOLO model
model = YOLO("yolov8n.pt")  # Automatically downloads pretrained weights

def get_dominant_color(image):
    # Resize to speed up
    img = cv2.resize(image, (50, 50))
    data = img.reshape((-1, 3))
    data = data.astype('float32')
    # Find most frequent color
    colors, counts = np.unique(data, axis=0, return_counts=True)
    dominant = colors[counts.argmax()]
    return tuple(map(int, dominant))

def rgb_to_name(rgb):
    # Simple mapping for common colors
    colors = {
        (255, 0, 0): "Red",
        (0, 255, 0): "Green",
        (0, 0, 255): "Blue",
        (255, 255, 0): "Yellow",
        (0, 255, 255): "Cyan",
        (255, 0, 255): "Magenta",
        (0, 0, 0): "Black",
        (255, 255, 255): "White",
        (128, 128, 128): "Gray",
        (128, 0, 0): "Maroon",
        (128, 128, 0): "Olive",
        (0, 128, 0): "Dark Green",
        (128, 0, 128): "Purple",
        (0, 128, 128): "Teal",
        (0, 0, 128): "Navy"
    }
    # Find closest color
    min_dist = float('inf')
    closest_name = "Unknown"
    for c, name in colors.items():
        dist = sum((a - b) ** 2 for a, b in zip(rgb, c))
        if dist < min_dist:
            min_dist = dist
            closest_name = name
    return closest_name

prev_centers = {}
prev_times = {}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    results = model(frame)[0]

    for result in results.boxes:
        x1, y1, x2, y2 = map(int, result.xyxy[0])
        cls_id = int(result.cls[0])
        class_name = model.names[cls_id]
        conf = float(result.conf[0])

        # Center of bounding box
        center = ((x1 + x2) // 2, (y1 + y2) // 2)

        # Speed calculation (pixels/sec)
        speed = 0
        if class_name in prev_centers:
            prev_center = prev_centers[class_name]
            prev_time = prev_times[class_name]
            dist = ((center[0] - prev_center[0]) ** 2 + (center[1] - prev_center[1]) ** 2) ** 0.5
            time_diff = current_time - prev_time
            if time_diff > 0:
                speed = dist / time_diff
        prev_centers[class_name] = center
        prev_times[class_name] = current_time

        # Get ROI and dominant color
        roi = frame[y1:y2, x1:x2]
        if roi.size > 0:
            color = get_dominant_color(roi)
            color_name = rgb_to_name(color)
            color_text = f'Color: {color_name}'
            area = (x2 - x1) * (y2 - y1)
        else:
            color = (0, 255, 0)
            color_text = 'Color: N/A'
            area = 0

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Prepare label with class, confidence, color, speed, area, and coordinates
        label = f'{class_name} ({conf:.2f})'
        speed_text = f'Speed: {speed:.2f} px/s'
        area_text = f'Area: {area} px'
        coords_text = f'Box: ({x1},{y1})-({x2},{y2})'

        cv2.putText(frame, label, (x1, y1 - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, color_text, (x1, y1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.putText(frame, speed_text, (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.putText(frame, area_text, (x1, y2 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.putText(frame, coords_text, (x1, y2 + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Object Detection (Name, Confidence, Color, Speed)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
