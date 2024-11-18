
<h1 align="center">PROJECT DETAILS</h1>
<h2 align="center">TATA ELXSI TELIPORT SEASON 2</h2>
<h2 align="center">FORWARD COLLISION WARNING (CASE STUDY 2)</h2>
<h1 align="center">TEAM DETAILS</h1>
<h3 align='center'>Team Leader: 	MOHAMED B SIRAJUDDEEN 	(Computer Science Engineering)</h3>
<h3 align='center'>Member 1: 	SANDEEP G 			(Computer Science Engineering)</h3>
<h3 align='center'>Member 2: 	RAGURAM R 			(Biomedical Engineering)</h3>

<p>CAMERA BASED DETECTION <br/><br/>
Use of Pre-Trained models like YOLOv8 (Fine-Tuned)<br/>8 Stereo camera (120 FOV : 250m)<br/>1 Dashcam (180 FOV : 150m )
</p>
<br/>
<br/>
<p>
RADAR DETECTION<br/><br/>
Use of YOLOv8 and Camera Integration<br/>1 Front RADAR sensor (60 FOV : 250m)<br/>1 Rear RADAR sensor (90 FOV : 50m)
</p>

<p>
Camera-Based Visuals for Object Detection<br/>
Working Principle:<br/>
Cameras provide continuous visual data. Using a trained YOLO (v5/v8) model for object detection, the system processes the images to identify obstacles, calculate distances, and trigger warnings.<br/>
<br/><br/>
Effectiveness:<br/>
<br/>
Highly accurate in identifying objects with trained datasets.<br/>
Real-time alerts prevent collisions.<br/>
  <br/><br/>
Reliability:<br/>
<br/>
Can fail under poor visibility (e.g., fog, rain).<br/>
Dependent on camera resolution and processing speed.<br/>
  <br/><br/>
Scalability:<br/>
<br/>
Easy to adapt for other ADAS features like lane departure warnings or pedestrian detection.<br/>
<br/><br/>
  Usability:<br/>
<br/>
Seamless integration into ADAS systems.<br/>
Requires minimal user interaction.<br/>
  <br/><br/>
Innovation:<br/>
<br/>
Combines GenAI for code generation with robust ML algorithms (YOLO).<br/><br/><br/>
Advantages:<br/>
<br/>
High detection accuracy.<br/>
Ability to recognize diverse object types.<br/>
Visual data can be stored for post-event analysis.<br/>
<br/><br/>
Disadvantages:<br/>
<br/>
Performance heavily dependent on lighting and environmental conditions.<br/>
High computational cost for real-time processing.<br/>
<br/><br/>Software Requirements:<br/>
<br/>
OpenCV, YOLO (v5/v8), Python, CARLA for simulation.<br/>
<br/><br/>
  Hardware Requirements:<br/>
<br/>
High-resolution cameras, GPU for inference, onboard processor.<br/>
<br/><br/>
  Skills Required:<br/>
<br/>
Python, ML model training, GenAI integration, automotive software compliance (e.g., MISRA, ASPICE).
</p>

<p>
  ### **Case 3: Radar Sensors for Object Detection**

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

#### **Key Comparison with Camera-Based Systems**:
While cameras excel at **object classification** and detail-rich imaging, radar sensors provide **unmatched reliability in poor visibility and weather conditions**, making them a crucial complement to camera-based systems. Combining the two ensures a **robust, fail-safe ADAS system**.
</p>

![Car side view finalv1](https://github.com/user-attachments/assets/c9a53fb7-18fd-44fa-86cf-bdc61ab2a639)

