
<h1 align="center">PROJECT DETAILS</h1>
<h2 align="center">TATA ELXSI TELIPORT SEASON 2</h2>
<h2 align="center">FORWARD COLLISION WARNING (CASE STUDY 2)</h2>
<h1 align="center">TEAM DETAILS</h1>
<h3 align='center'>Team Leader: 	MOHAMED B SIRAJUDDEEN 	(Computer Science Engineering)</h3>
<h3 align='center'>Member 1: 	SANDEEP G 			(Computer Science Engineering)</h3>
<h3 align='center'>Member 2: 	RAGURAM R 			(Biomedical Engineering)</h3>

<p>
<h2>Camera-Based Visuals for Object Detection</h2><br/><br/>
- **Working Principle**:  
   Cameras provide continuous visual data. Using a trained YOLO (v5/v8) model for object detection, the system processes the images to identify obstacles, calculate distances, and trigger warnings.

   ---
   
- **Effectiveness**:  
   - Highly accurate in identifying objects with trained datasets.  
   - Real-time alerts prevent collisions.  

---

- **Reliability**:  
   - Can fail under poor visibility (e.g., fog, rain).  
   - Dependent on camera resolution and processing speed.  

---

- **Scalability**:  
   - Easy to adapt for other ADAS features like lane departure warnings or pedestrian detection.  

---

- **Usability**:  
   - Seamless integration into ADAS systems.  
   - Requires minimal user interaction.  

---

- **Innovation**:  
   - Combines GenAI for code generation with robust ML algorithms (YOLO).  

---

- **Advantages**:  
   - High detection accuracy.  
   - Ability to recognize diverse object types.  
   - Visual data can be stored for post-event analysis.  

---

- **Disadvantages**:  
   - Performance heavily dependent on lighting and environmental conditions.  
   - High computational cost for real-time processing.  

---

- **Software Requirements**:  
   - OpenCV, YOLO (v5/v8), Python, CARLA for simulation.

---
  
- **Hardware Requirements**:  
   - High-resolution cameras, GPU for inference, onboard processor.
 
---

- **Skills Required**:  
   - Python, ML model training, GenAI integration, automotive software compliance (e.g., MISRA, ASPICE).
</p>
<br/><br/><br/>
<p>
<h2>RADAR based Sensor for Detection</h2><br/><br/>
#### **Working Principle**:
Radar sensors emit **radio waves** that reflect off objects in their path. By analyzing the **reflected signals**, the system calculates the distance, speed, and direction of objects. Doppler shift is used to determine the relative velocity of moving objects, enabling accurate detection even in challenging environmental conditions.

---

#### **Effectiveness**:
- **Highly reliable** in detecting objects at long and medium ranges, even in adverse weather conditions (e.g., fog, rain, snow).  
- Capable of tracking **moving objects** like vehicles and pedestrians.  

---

#### **Reliability**:
- Performs well in **all weather conditions** and low visibility.  
- Resistant to interference from environmental factors, though extreme electromagnetic noise can affect accuracy.  

---

#### **Scalability**:
- Easily integrates into various **ADAS features**, including adaptive cruise control, blind-spot detection, and collision avoidance.  
- Supports **360-degree coverage** when used in combination with multiple radar sensors.

---

#### **Usability**:
- Straightforward integration into **ADAS architectures**.  
- Minimal calibration required for long-term operation.  

---

#### **Innovation**:
- Combines **Doppler radar** principles with advanced signal processing algorithms.  
- Potential for integration with **sensor fusion systems** (e.g., combining radar and cameras) to enhance overall detection capabilities.

---

#### **Advantages**:
- Effective in all lighting and weather conditions.  
- Can detect both **stationary and moving objects**.  
- Accurate measurement of object distance and relative speed.  
- Lower computational requirements compared to vision-based systems.  

---

#### **Disadvantages**:
- Cannot classify objects (e.g., pedestrian vs. vehicle) without additional sensor data.  
- Lower resolution compared to cameras or LIDAR.  
- Limited detection of fine details and shapes.  

---

#### **Software Requirements**:
- Radar signal processing libraries (e.g., **MATLAB, Python with SciPy**).  
- Integration frameworks for ADAS systems.  
- Tools for simulation and testing (e.g., **ROS, CARLA, MATLAB Simulink**).  

---

#### **Hardware Requirements**:
- **Short-range radar sensors** (for parking assistance and low-speed detection).  
- **Long-range radar sensors** (for high-speed collision avoidance and adaptive cruise control).  
- **Onboard processors** capable of handling radar signal data.  

---

#### **Skills Required**:
- Knowledge of **electromagnetic wave theory** and radar principles.  
- Expertise in **signal processing and Doppler shift analysis**.  
- Experience with **ADAS integration** and **automotive software standards** (e.g., ASPICE, ISO 26262).  

---
</p>
<p>
 Categories Tested<br/>Standard Scenarios: Stationary and moving obstacles on straight roads.<br/>Environmental Conditions: Day, night, rain, fog, snow.<br/>Traffic Complexities: Cut-in, cut-out, multi-lane scenarios.<br/>Road Types: Curves, inclines, uneven surfaces.<br/>Edge Cases: False positives, unusual obstacles, sensor malfunctions.<br/>Key Results<br/>Total Test Cases: 20<br/>Passed: 100%<br/>Metrics Achieved:<br/>Warning Time: ≤ 2.0s → Achieved: 1.8s<br/>False Positive Rate: ≤ 5% → Achieved: 3%<br/>Testing Tools<br/>Simulation: CARLA<br/>Metrics Evaluated: Warning accuracy, false positive/negative rates, driver response time.
![image](https://github.com/user-attachments/assets/4c14ee02-b801-4505-b275-9c5240870d3b)
   
 </p>

![Car side view finalv1](https://github.com/user-attachments/assets/c9a53fb7-18fd-44fa-86cf-bdc61ab2a639)
![JXI_TATA_FINAL 1](https://github.com/user-attachments/assets/6245d4e9-db38-43c7-aa36-7f1b4a15d003)
![Flowchartv4](https://github.com/user-attachments/assets/b07a98fb-a108-4e80-9b2c-9d57fa477c06)

<h2>REFERENCES</h2>
<p>https://www.researchgate.net/publication/258359207_Safety_Benefits_of_Forward_Collision_Warning_Brake_Assist_and_Autonomous_Braking_Systems_in_Rear-End_Collisions</p><br/>
<p>https://pmc.ncbi.nlm.nih.gov/articles/PMC8924939/</p><br/>
<p>https://www.researchgate.net/publication/338384037_A_Forward_Collision_Warning_System_Using_Driving_Intention_Recognition_of_the_Front_Vehicle_and_V2V_Communication</p><br/>
<p>https://www.researchgate.net/publication/4092563_Forward_collision_warning_with_a_single_camera</p><br/>
<p>https://www.researchgate.net/publication/295920228_INTRODUCTION_Forward_Collision_Warning_Clues_to_Optimal_Timing_of_Advisory_Warnings_Downloaded_from_SAE_International</p><br/>
<p>https://www.researchgate.net/profile/Toshihiro-Hiraoka/publication/234054272_Situation-adaptive_warning_timing_of_a_forward_obstacle_collision_warning_system/links/0912f50ea1e70a0ced000000/Situation-adaptive-warning-timing-of-a-forward-obstacle-collision-warning-system.pdf</p><br/>
<p>https://www.researchgate.net/publication/325255668_A_Perceptual_Forward_Collision_Warning_Model_using_Naturalistic_Driving_Data</p><br/>
<p>https://www.researchgate.net/publication/264397726_Effectiveness_of_forward_obstacles_collision_warning_system_based_on_deceleration_for_collision_avoidance</p><br/>
<p>https://www.researchgate.net/publication/377494939_Evaluating_forward_collision_warning_and_autonomous_emergency_braking_systems_in_India_using_dashboard_cameras</p><br/>
<p>https://www.researchgate.net/publication/354607233_Forward_collision_warning_system_for_motorcyclist_using_smart_phone_sensors_based_on_time-to-collision_and_trajectory_prediction</p><br/>

