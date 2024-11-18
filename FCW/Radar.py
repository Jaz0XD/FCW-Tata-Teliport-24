'''
Note: This script demonstrates how to fuse camera and radar data for enhanced object detection.
'''

import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("./yolov8n.pt")  # Replace with your model file if different

# Simulated Radar Data (Example)
# Each entry is [distance (m), velocity (m/s), angle (degrees)]
radar_data = [
    {"distance": 20, "velocity": -5, "angle": 0},  # Object 1
    {"distance": 30, "velocity": -10, "angle": -5},  # Object 2
]

def fuse_camera_radar(camera_frame, radar_data, yolo_results):
    """
    Fuse camera (YOLO) and radar data for enhanced object detection.
    :param camera_frame: The current camera frame (image)
    :param radar_data: List of radar detections
    :param yolo_results: YOLOv8 detections
    :return: Frame with fused data visualized
    """
    # Loop through YOLO detections
    for result in yolo_results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result  # Bounding box coordinates, confidence, class ID
        class_name = model.names[int(cls)]

        # Only consider relevant objects (e.g., vehicles)
        if class_name in ["car", "truck", "bus"]:
            bbox_center_x = (x1 + x2) / 2
            bbox_center_y = (y1 + y2) / 2

            # Match radar data to YOLO bounding boxes
            closest_radar_object = None
            min_distance = float('inf')
            for radar_obj in radar_data:
                radar_angle_px = radar_obj["angle"]  # Assume angle mapping to horizontal position
                radar_distance = radar_obj["distance"]

                # Simple matching logic: nearest radar object to bounding box center
                if abs(bbox_center_x - radar_angle_px) < 50:  # Threshold for matching
                    if radar_distance < min_distance:
                        min_distance = radar_distance
                        closest_radar_object = radar_obj

            # Display matched radar information on frame
            if closest_radar_object:
                cv2.rectangle(camera_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(
                    camera_frame,
                    f"{class_name} {min_distance:.2f}m {closest_radar_object['velocity']:.2f}m/s",
                    (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    2,
                )

    return camera_frame

def main():
    # Initialize camera feed
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the camera.")
            break

        # Run YOLOv8 detection
        results = model(frame)

        # Fuse radar data with YOLO results
        fused_frame = fuse_camera_radar(frame, radar_data, results)

        # Display the fused frame
        cv2.imshow("Camera-Radar Fusion", fused_frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
