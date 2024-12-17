import carla
import pygame
import numpy as np
import cv2
from ultralytics import YOLO
import threading
from queue import Queue

# Initialize pygame for speed display
pygame.init()
WIDTH, HEIGHT = 1920, 1080  # Default width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Load YOLOv8 model
model = YOLO("E:/CARLA/WindowsNoEditor/PythonAPI/examples/yolov8n.pt")  # Adjust path if necessary

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

# Function to check if any vehicle is within a certain distance in front of the player
def check_proximity(player_vehicle):
    detection_radius = 15.0  # Detection radius in meters
    warning_message = ""
    vehicles = world.get_actors().filter("vehicle.*")
    player_transform = player_vehicle.get_transform()
    player_location = player_transform.location
    player_forward = player_transform.get_forward_vector()

    for vehicle in vehicles:
        if vehicle.id != player_vehicle.id:
            other_location = vehicle.get_transform().location
            distance = player_location.distance(other_location)
            if distance < detection_radius:
                direction = other_location - player_location
                forward_dot = player_forward.x * direction.x + player_forward.y * direction.y + player_forward.z * direction.z
                if forward_dot > 0:  # Check if the vehicle is in front
                    warning_message = "WARNING: Vehicle Ahead!"
                    break

    return warning_message

#! Clear Weather
def set_weather(client, weather_params):
    """
    Sets the weather parameters in the CARLA simulator.

    :param client: The CARLA client connected to the simulator.
    :param weather_params: The WeatherParameters object with desired settings.
    """
    world = client.get_world()
    world.set_weather(weather_params)


# Main function
def main():
    global WIDTH, HEIGHT, screen  # Declare screen as global
    player_vehicle = spawn_vehicle()
    spawn_other_vehicles()  # Spawn other vehicles
    
    # Create WeatherParameters object for clear night weather
    clear_night_weather = carla.WeatherParameters(
        cloudiness=0.0,               # Clear sky
        precipitation=0.0,            # No rain
        precipitation_deposits=0.0,   # No water on the ground
        sun_altitude_angle=-20.0,     # Sun is below the horizon (nighttime)
        fog_density=0.0,              # No fog
        fog_distance=100.0,           # High visibility
        wetness=0.0,                  # Dry roads
        wind_intensity=0.0            # Calm conditions
    )
    
    # Apply the clear night weather
    set_weather(client, clear_night_weather)
    print("Weather set to clear night!")
    

    # Set up the front camera
    camera_bp = world.get_blueprint_library().find("sensor.camera.rgb")
    camera_bp.set_attribute("image_size_x", f"{WIDTH}")
    camera_bp.set_attribute("image_size_y", f"{HEIGHT}")
    camera_bp.set_attribute("fov", "110")
    front_camera = world.spawn_actor(camera_bp, carla.Transform(carla.Location(x=2.5, z=0.7)), attach_to=player_vehicle)

    # Set up the third-person camera
    third_person_camera_bp = world.get_blueprint_library().find("sensor.camera.rgb")
    third_person_camera_bp.set_attribute("image_size_x", f"{WIDTH}")
    third_person_camera_bp.set_attribute("image_size_y", f"{HEIGHT}")
    third_person_camera_bp.set_attribute("fov", "110")
    third_person_camera = world.spawn_actor(
        third_person_camera_bp,
        carla.Transform(carla.Location(x=-6.0, z=2.5), carla.Rotation(pitch=-10)),
        attach_to=player_vehicle
    )

    # Queues to hold camera frames for processing
    front_frame_queue = Queue(maxsize=10)
    third_person_frame_queue = Queue(maxsize=10)

    # Function to handle front camera images
    def front_camera_callback(image):
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = np.reshape(array, (image.height, image.width, 4))
        frame = cv2.cvtColor(array[:, :, :3], cv2.COLOR_BGRA2BGR)
        if not front_frame_queue.full():
            front_frame_queue.put(frame)

    # Function to handle third-person camera images
    def third_person_camera_callback(image):
        array = np.frombuffer(image.raw_data, dtype=np.uint8)
        array = np.reshape(array, (image.height, image.width, 4))
        frame = cv2.cvtColor(array[:, :, :3], cv2.COLOR_BGRA2BGR)
        if not third_person_frame_queue.full():
            third_person_frame_queue.put(frame)

    # Function to process frames for front and third-person views
    def process_frames():
        while True:
            # Process front camera
            if not front_frame_queue.empty():
                front_frame = front_frame_queue.get()

                # Object detection using YOLO
                results = model.predict(front_frame, conf=0.5)
                detected_objects = results[0].boxes

                # Draw bounding boxes on the front camera frame
                for obj in detected_objects:
                    x1, y1, x2, y2 = map(int, obj.xyxy[0])
                    label = obj.cls
                    confidence = obj.conf[0]
                    cv2.rectangle(front_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(front_frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                cv2.imshow("Front Camera", front_frame)

            # Process third-person camera
            if not third_person_frame_queue.empty():
                third_person_frame = third_person_frame_queue.get()
                cv2.imshow("Third-Person Camera", third_person_frame)

            cv2.waitKey(1)

    # Start the frame processing thread
    frame_processing_thread = threading.Thread(target=process_frames, daemon=True)
    frame_processing_thread.start()

    # Set camera callbacks
    front_camera.listen(lambda image: front_camera_callback(image))
    third_person_camera.listen(lambda image: third_person_camera_callback(image))

    try:
        while True:
            # Handle quitting the game and resizing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.w, event.h
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    


            # Display vehicle speed in Pygame
            screen.fill((0, 0, 0))  # Clear screen
            velocity = player_vehicle.get_velocity()
            speed = (3.6 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5)  # Convert to km/h
            font = pygame.font.Font(None, 36)
            speed_text = font.render(f"Speed: {speed:.2f} km/h", True, (255, 255, 255))
            screen.blit(speed_text, (10, 10))  # Display speed on top-left of the window

            # Check for proximity and display warning if necessary
            warning_message = check_proximity(player_vehicle)
            if warning_message:
                warning_text = font.render(warning_message, True, (255, 0, 0))
                screen.blit(warning_text, (10, 50))  # Display warning below the speed text

            pygame.display.flip()
            clock.tick(144)

    finally:
        # Clean up: destroy sensors and Pygame
        front_camera.destroy()
        third_person_camera.destroy()
        player_vehicle.destroy()
        pygame.quit()
        cv2.destroyAllWindows()

# Run the simulation
if __name__ == "__main__":
    main()