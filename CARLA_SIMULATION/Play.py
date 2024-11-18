'''
Important Note: Inorder to run this script, you need to have the CARLA simulator installed on your system.
You can download the CARLA simulator from the following link: https://carla.org/

Also, you need to have the yolov8n.pt file in the same directory as this script.
File is provided in the repository.

Note: This script is a simple example to demonstrate how to use YOLOv8 object detection with CARLA simulation.

Features: 
1. Spawns a player vehicle in CARLA simulation.
2. Uses YOLOv8 object detection to detect objects in the camera feed.
'''


import carla
import pygame
import numpy as np
from ultralytics import YOLO

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    player_vehicle.set_autopilot(False)
    return player_vehicle

# Draw bounding boxes on Pygame screen
def draw_bounding_boxes(detections):
    for detection in detections:
        x1, y1, x2, y2 = map(int, detection.xyxy[0])  # Bounding box coordinates
        label = detection.cls  # Detected object class
        confidence = detection.conf[0]  # Confidence score
        color = (255, 0, 0)  # Red color for bounding box

        pygame.draw.rect(screen, color, (x1, y1, x2 - x1, y2 - y1), 2)
        font = pygame.font.Font(None, 24)
        text = font.render(f"{label} {confidence:.2f}", True, color)
        screen.blit(text, (x1, y1 - 10))

# Main function
def main():
    player_vehicle = spawn_vehicle()
    
    # Set up the camera
    camera_bp = world.get_blueprint_library().find("sensor.camera.rgb")
    camera_bp.set_attribute("image_size_x", f"{WIDTH}")
    camera_bp.set_attribute("image_size_y", f"{HEIGHT}")
    camera_bp.set_attribute("fov", "110")
    camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=2.5, z=0.7)), attach_to=player_vehicle)

    # Function to handle camera images, detect objects, and display in Pygame
    def camera_callback(image):
        # Convert image to numpy array
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = np.reshape(array, (image.height, image.width, 4))  # Convert to BGRA format
        array = array[:, :, :3][:, :, ::-1]  # Convert BGRA to RGB

        # Object detection using YOLO
        results = model.predict(array, conf=0.5)
        detected_objects = results[0].boxes  # Get detected objects

        # Display camera feed
        screen_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))  # Transpose for Pygame display
        screen.blit(screen_surface, (0, 0))

        # Draw bounding boxes
        draw_bounding_boxes(detected_objects)

        # Get vehicle speed and display on screen
        velocity = player_vehicle.get_velocity()
        speed = (3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5)  # Convert to km/h
        font = pygame.font.Font(None, 36)
        speed_text = font.render(f"Speed: {speed:.2f} km/h", True, (255, 255, 255))
        screen.blit(speed_text, (10, 10))

        # Apply automatic braking if an object is detected within 15 meters
        for obj in detected_objects:
            # Assume the bounding box represents an object within 15 meters
            distance = 15  # Adjust based on your use case
            if distance < 15 and speed > 20:  # Slow down if speed > 20 km/h
                control = carla.VehicleControl()
                control.throttle = 0.0
                control.brake = 1.0
                player_vehicle.apply_control(control)

        pygame.display.flip()  # Update the display

    # Set camera callback to listen to the camera feed
    camera.listen(lambda image: camera_callback(image))

    try:
        while True:
            # Handle quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # WASD controls for manual driving
            keys = pygame.key.get_pressed()
            control = carla.VehicleControl()

            if keys[pygame.K_w]:  # Move forward
                control.throttle = 0.5
            if keys[pygame.K_s]:  # Move backward
                control.reverse = True
                control.throttle = 0.5
            if keys[pygame.K_a]:  # Turn left
                control.steer = -0.5
            if keys[pygame.K_d]:  # Turn right
                control.steer = 0.5

            player_vehicle.apply_control(control)
            clock.tick(60)

    finally:
        # Clean up: destroy sensors and Pygame
        camera.destroy()
        player_vehicle.destroy()
        pygame.quit()

# Run the simulation
if __name__ == "__main__":
    main()
