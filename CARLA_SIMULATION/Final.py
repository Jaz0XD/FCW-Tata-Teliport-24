'''
Important Note: Inorder to run this script, you need to have the CARLA simulator installed on your system.
You can download the CARLA simulator from the following link: https://carla.org/

Also, you need to have the yolov8n.pt file in the same directory as this script.
File is provided in the repository.

Note: This script is the final demonstration of Object Detection and Warning System.

Features: 
1. Spawns a player vehicle in CARLA simulation.
2. Uses YOLOv8 object detection to detect objects in the camera feed.
3. Displays the camera feed with bounding boxes around detected objects.
4. Displays the speed of the player vehicle in the Pygame window.
5. Spawns other vehicles in random locations for realism.
6. Uses multithreading to handle camera feed and object detection.
7. Enabled Autopilot for the player vehicle to follow the road and traffic rules.
'''

import carla
import pygame
import numpy as np
import cv2
from ultralytics import YOLO
import threading
from queue import Queue

# Initialize pygame for speed display
pygame.init()
WIDTH, HEIGHT = 640, 480  # Default width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Load YOLOv8 model
model = YOLO("./yolov8n.pt")  # Adjust path if necessary

# Connect to CARLA server
client = carla.Client("localhost", 2000)
client.set_timeout(15.0)
world = client.get_world()

# Function to spawn player vehicle
def spawn_vehicle():
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter("model3")[0]  # Choose a vehicle model
    spawn_point = world.get_map().get_spawn_points()[0]
    player_vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    player_vehicle.set_autopilot(True)  # Enable autopilot to follow the road
    return player_vehicle

# Function to spawn other vehicles in random locations
def spawn_other_vehicles():
    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter("vehicle.*")[0]  # Random vehicle model
    spawn_points = world.get_map().get_spawn_points()
    for spawn_point in spawn_points[1:20]:  # Limit to 5 vehicles for this example
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        vehicle.set_autopilot(True)  # Set autopilot for random movement

# Main function
def main():
    global WIDTH, HEIGHT, screen  # Declare screen as global
    player_vehicle = spawn_vehicle()
    spawn_other_vehicles()  # Spawn other vehicles
    
    # Set up the camera
    camera_bp = world.get_blueprint_library().find("sensor.camera.rgb")
    camera_bp.set_attribute("image_size_x", f"{WIDTH}")
    camera_bp.set_attribute("image_size_y", f"{HEIGHT}")
    camera_bp.set_attribute("fov", "110")
    camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=2.5, z=0.7)), attach_to=player_vehicle)

    # Queue to hold camera frames for processing
    frame_queue = Queue(maxsize=10)  # Buffer size 10 for the frames

    # Function to handle camera images, detect objects, and display in OpenCV window
    def camera_callback(image):
        # Convert image to numpy array
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = np.reshape(array, (image.height, image.width, 4))  # Convert to BGRA format
        frame = cv2.cvtColor(array[:, :, :3], cv2.COLOR_BGRA2BGR)  # Properly convert BGRA to BGR

        # Put frame into the queue
        if not frame_queue.full():
            frame_queue.put(frame)

    # Function to process frames from the queue in a separate thread
    def process_frames():
        while True:
            if not frame_queue.empty():
                frame = frame_queue.get()

                # Object detection using YOLO
                results = model.predict(frame, conf=0.5)
                detected_objects = results[0].boxes

                # Draw bounding boxes on the frame
                for obj in detected_objects:
                    x1, y1, x2, y2 = map(int, obj.xyxy[0])  # Bounding box coordinates
                    label = obj.cls  # Detected object class
                    confidence = obj.conf[0]  # Confidence score
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                # Display the camera feed in an OpenCV window
                cv2.imshow("Front Camera", frame)
                cv2.waitKey(1)

    # Start the frame processing thread
    frame_processing_thread = threading.Thread(target=process_frames, daemon=True)
    frame_processing_thread.start()

    # Set camera callback to listen to the camera feed
    camera.listen(lambda image: camera_callback(image))

    try:
        while True:
            # Handle quitting the game and resizing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.VIDEORESIZE:  # Handle window resizing
                    WIDTH, HEIGHT = event.w, event.h
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            # Display vehicle speed in Pygame
            screen.fill((0, 0, 0))  # Clear screen
            velocity = player_vehicle.get_velocity()
            speed = (3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5)  # Convert to km/h
            font = pygame.font.Font(None, 36)
            speed_text = font.render(f"Speed: {speed:.2f} km/h", True, (255, 255, 255))
            screen.blit(speed_text, (10, 10))  # Display speed on top-left of the window
            pygame.display.flip()
            clock.tick(144)

    finally:
        # Clean up: destroy sensors and Pygame
        camera.destroy()
        player_vehicle.destroy()
        pygame.quit()
        cv2.destroyAllWindows()

# Run the simulation
if __name__ == "__main__":
    main()
