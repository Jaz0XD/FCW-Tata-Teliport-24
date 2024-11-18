'''
Note: This Script Integrates the camera and calculates the distance and time-to-collision (TTC) for detected objects.
'''

import cv2
import numpy as np
from ultralytics import YOLO
import time

# Load the YOLOv8 pre-trained model
model = YOLO("./yolov8n.pt")  # Replace with your model file if different

# Constants
FOCAL_LENGTH = 700  # Focal length of the camera (to be calibrated)
BRAKE_THRESHOLD_TTC = 3  # Time-to-collision threshold (seconds)

def calculate_distance(bounding_box_width, known_width=2.0, focal_length=FOCAL_LENGTH):
    """
    Estimate distance of object from the car using the bounding box width.
    :param bounding_box_width: Width of the detected object's bounding box in pixels
    :param known_width: Real-world width of the object in meters
    :param focal_length: Focal length of the camera
    :return: Distance in meters
    """
    return (known_width * focal_length) / bounding_box_width

def calculate_time_to_collision(car_speed, object_speed, distance):
    """
    Calculate Time to Collision (TTC).
    :param car_speed: Speed of the car in m/s
    :param object_speed: Speed of the detected object in m/s
    :param distance: Distance to the object in meters
    :return: Time to collision in seconds
    """
    relative_speed = car_speed - object_speed
    if relative_speed <= 0:
        return float('inf')  # No collision possible if object is moving away
    return distance / relative_speed

def main():
    # Initialize video capture (camera feed)
    cap = cv2.VideoCapture(0)  # Replace with your camera source if different

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    # Variables to track object speed
    object_positions = {}  # Store previous positions for each object
    car_speed = float(input("Enter car's current speed in m/s: "))  # Replace with real-time sensor data

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the camera.")
            break

        # Run YOLOv8 detection
        results = model(frame)

        for result in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = result  # Bounding box coordinates, confidence, class ID
            class_name = model.names[int(cls)]

            # Only consider relevant objects (e.g., vehicles, pedestrians)
            if class_name in ["car", "truck", "bus", "person"]:
                bounding_box_width = x2 - x1
                object_id = f"{int(x1)}_{int(y1)}"  # Unique ID for the object (based on bounding box location)
                current_time = time.time()

                # Calculate distance
                distance = calculate_distance(bounding_box_width)

                # Estimate object speed
                if object_id in object_positions:
                    previous_x, previous_time = object_positions[object_id]
                    object_speed = (bounding_box_width - previous_x) / (current_time - previous_time)
                else:
                    object_speed = 0  # Assume 0 speed for the first frame

                object_positions[object_id] = (bounding_box_width, current_time)

                # Calculate Time to Collision (TTC)
                ttc = calculate_time_to_collision(car_speed, object_speed, distance)

                # Display detection info
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name} {distance:.2f}m TTC: {ttc:.2f}s",
                            (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Apply brakes if TTC is below threshold
                if ttc < BRAKE_THRESHOLD_TTC:
                    print(f"Warning: Collision with {class_name} detected! Applying brakes.")
                    # Trigger car braking system (replace this with actual API call)
                    car_speed = max(0, car_speed - 5)  # Example of reducing speed

        # Display the frame
        cv2.imshow("Autonomous Car Detection", frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
