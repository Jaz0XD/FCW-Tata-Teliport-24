'''
Note: This script is an optimized Camera code that integrates Adaptive Cruise Control (ACC) logic.
'''

import cv2
import numpy as np
from ultralytics import YOLO
import time

# Load the YOLOv8 pre-trained model
model = YOLO("./yolov8n.pt")  # Replace with your model file if different

# Constants
FOCAL_LENGTH = 700  # Focal length of the camera (to be calibrated)
SAFE_TIME_GAP = 2  # Safe following time gap in seconds
MAX_SPEED = 30  # Maximum speed of the car in m/s (example: 108 km/h)
MIN_SPEED = 0  # Minimum speed (stationary)
ACCELERATION = 1.5  # Rate of speed increase in m/s²
DECELERATION = -3.0  # Rate of speed decrease in m/s²

def calculate_distance(bounding_box_width, known_width=2.0, focal_length=FOCAL_LENGTH):
    """
    Estimate distance of object from the car using the bounding box width.
    :param bounding_box_width: Width of the detected object's bounding box in pixels
    :param known_width: Real-world width of the object in meters
    :param focal_length: Focal length of the camera
    :return: Distance in meters
    """
    return (known_width * focal_length) / bounding_box_width

def calculate_safe_speed(distance, car_speed):
    """
    Calculate the safe speed based on the distance to the object and the safe time gap.
    :param distance: Distance to the object in meters
    :param car_speed: Current speed of the car in m/s
    :return: Recommended safe speed in m/s
    """
    safe_speed = distance / SAFE_TIME_GAP
    return min(safe_speed, MAX_SPEED)

def adjust_speed(current_speed, target_speed):
    """
    Adjust the car's speed smoothly toward the target speed.
    :param current_speed: Current speed of the car in m/s
    :param target_speed: Target speed in m/s
    :return: New adjusted speed in m/s
    """
    if current_speed < target_speed:
        # Accelerate smoothly
        return min(current_speed + ACCELERATION, target_speed, MAX_SPEED)
    elif current_speed > target_speed:
        # Decelerate smoothly
        return max(current_speed + DECELERATION, target_speed, MIN_SPEED)
    return current_speed

def main():
    # Initialize video capture (camera feed)
    cap = cv2.VideoCapture(0)  # Replace with your camera source if different

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    # Initialize the car's speed
    car_speed = float(input("Enter the car's initial speed in m/s: "))  # Replace with real-time sensor data

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the camera.")
            break

        # Run YOLOv8 detection
        results = model(frame)

        # Initialize the closest object's distance
        closest_distance = float('inf')

        for result in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = result  # Bounding box coordinates, confidence, class ID
            class_name = model.names[int(cls)]

            # Only consider relevant objects (e.g., vehicles)
            if class_name in ["car", "truck", "bus"]:
                bounding_box_width = x2 - x1
                distance = calculate_distance(bounding_box_width)
                closest_distance = min(closest_distance, distance)

                # Display detection info
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name} {distance:.2f}m",
                            (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Adaptive Cruise Control logic
        if closest_distance != float('inf'):  # If an object is detected
            target_speed = calculate_safe_speed(closest_distance, car_speed)
        else:
            target_speed = MAX_SPEED  # No object detected, cruise at max speed

        car_speed = adjust_speed(car_speed, target_speed)

        # Display current speed and target speed
        cv2.putText(frame, f"Car Speed: {car_speed:.2f} m/s", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Target Speed: {target_speed:.2f} m/s", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Display the frame
        cv2.imshow("Adaptive Cruise Control", frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
