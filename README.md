# LivingStream Object Tracking for Unity

LivingStream Object Tracking is an application that utilizes the Intel RealSense D435i camera to detect and track objects in real-time using computer vision techniques powered by Ultralytics YOLO11. The tracked object data (x, y, z coordinates) is sent via UDP to Unity for visualization, making it ideal for interactive and immersive applications.

This application is part of the larger LivingStream project which uses a projector to display a river with local fish. The projection is interactive and reacts to people as they walk over the projection. The project was created in coordination with the University of Texas at Arlington and the U.S. Army Corps of Engineers for education and entertainment at one of their visitor's centers.

UTA Computer Science and Engineering \
LivingStream Senior Design Team

Arham Ali ([GitHub](https://github.com/ara1399/)) \
Bryan Ukeje​ \
Daniel Hofer​ ([GitHub](https://github.com/275RR-Public/)) \
William Forbes​

---

## Hardware Requirements

- **Required**:
  - Intel RealSense D435i camera ([link](https://www.intelrealsense.com/depth-camera-d435i/))
  - Windows 10 or 11 machine with internet access
  - USB 3.1 Gen 1 or better cable and port (Double-check if you notice camera delays, stutters, or blackouts)

- **Optional but Highly Recommended**:
  - NVIDIA GPU (1000 series or better, excluding the newest 5000 series) for approximately an 8x performance increase
  - AMD GPUs are NOT currently supported

**WARNING**: Running the application on a CPU instead of an NVIDIA GPU will noticeably degrade the experience.

---

## Software Requirements

- Python 3.11.9 ([download](https://www.python.org/downloads/release/python-3119/)) - "Windows installer (64-bit)"
- Intel RealSense SDK 2.56.3 beta ([download](https://github.com/IntelRealSense/librealsense/releases/tag/v2.56.3)) - "Intel.RealSense.SDK-WIN10-2.56.3.7838.beta.exe"

---

## Environment Setup

To optimize the application's performance:

- **For Better Tracking**:
  - Reduce reflective surfaces in the environment.
  - Increase ambient light.

- **For Better Projection**:
  - Decrease ambient light to improve picture quality.

Hardware placement:

- **Projector**:
  - Mount the projector in a top-down orientation.

- **Camera**:
  - Position the camera at an angle rather than top-down for better identification and tracking of objects.
  - Position the camera to the center of the width (long-side in 1080p) of the projection for the optimal horizontal field of view (FOV).
  - In order to achieve the 2 above positions optimally, the camera will likely need to be offset from the projection (not overhead of any of the projection).
  - Lastly, minimize the offset to maintain accurate depth measurements (the D435i maintains accurate measurements up to 3m) across the entire projection.
  - In reality, this will be a series of trade-offs based on your environment. Try to maintain a mostly center offset to keep a decent angle of the camera while keeping most of the projection within 4m of the camera.

**Note**: Many projectors can shift the projection from their center line in both the horizontal and vertical. This might aide in placement of both the projector and D435i. The calibration steps after installation will adjust for the placement of both the projector and D435i.

---

## Automated Installation Using `RUN.bat`

The easiest way to install and run the application is by using the provided `RUN.bat` script. This script automates the installation process and launches the application.

### Automatic Steps

1. **Ensure Prerequisites**:
   - Install Python 3.11.9 and check "Add Python to PATH" during installation ([download](https://www.python.org/downloads/release/python-3119/)).
   - Install the Intel RealSense SDK ([download](https://github.com/IntelRealSense/librealsense/releases/tag/v2.56.3)).
   - Verify that your Intel RealSense D435i camera is connected via a USB 3.1 Gen 1 or better port.

2. **Run `RUN.bat`**:
   - Navigate to the project directory in File Explorer.
   - Double-click `RUN.bat`.
   - Follow any on-screen prompts to confirm installations and specify GPU support (if applicable).

3. **Wait for Installation**:
   - The script checks for an existing installation.
   - If not found, it will:
     - Create a virtual environment (`.venv`).
     - Update pip.
     - Install required libraries (PyTorch, pyrealsense2, opencv-python, numpy, ultralytics).
   - This process may take several minutes due to large library downloads.

4. **Launch the Application**:
   - Upon successful installation, `RUN.bat` activates the virtual environment and runs the app.

**Note**: On the first run, the YOLO model will download, requiring an active internet connection.

---

## Manual Installation

For users who prefer a hands-on approach, need to troubleshoot specific steps, or need to by-pass the install script: follow this manual install process.

### Manual Steps

1. **Install Python 3.11.9**:
   - Download and install Python 3.11.9 from [here](https://www.python.org/downloads/release/python-3119/).
   - During installation, check "Add Python to PATH".

2. **Install Intel RealSense SDK**:
   - Download and install the SDK from [here](https://github.com/IntelRealSense/librealsense/releases/tag/v2.56.3).

3. **Navigate to Project Directory**:
   - Open a Command Prompt or PowerShell.
   - Use the `cd` command to navigate to the project root folder (e.g., `cd path\to\project`).

4. **Create a Virtual Environment**:
   - Run:

     ```bash
     python -m venv .venv
     ```

   - This creates a virtual environment named `.venv`.

5. **Activate the Virtual Environment**:
   - Run:

     ```bash
     .\.venv\Scripts\activate
     ```

   - Your prompt should now show `(.venv)` to indicate the environment is active.

6. **Update Pip**:
   - Run:

     ```bash
     python -m pip install --upgrade pip
     ```

7. **Install PyTorch if NVIDIA GPU** (1000 series or better):
   - Run:

     ```bash
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
     ```

   - This step may take several minutes due to library sizes.

8. **Install Remaining Libraries**:
   - Run:

     ```bash
     pip install pyrealsense2 opencv-python numpy ultralytics
     ```

   - This step may take several minutes due to library sizes.

9. **Run the Application**:
   - Run:

     ```bash
     python app.py
     ```

**Note**: On the first run, the YOLO model will download, requiring an active internet connection.

---

## App launching after installation

Launching the app after installation can be accomplished automatically with `RUN.bat` or manually.

### Using `RUN.bat`

- Double-click **`RUN.bat`**:

  - RUN.bat will check for a current install
  - RUN.bat activates the virtual environment and runs the app

### Manually

1. **Navigate to Project Directory**:
   - Open a Command Prompt or PowerShell.
   - Use the `cd` command to navigate to the project root folder (e.g., `cd path\to\project`).

2. **Activate the Virtual Environment** if not active:
   - Run:

     ```bash
     .\.venv\Scripts\activate
     ```

   - Your prompt should now show `(.venv)` to indicate the environment is active.

3. **Run the Application**:
   - Run:

     ```bash
     python app.py
     ```

---

## Aligning the D435i with Unity

**IMPORTANT: After installation but before use of the system, the camera's coordinate system needs to be aligned with Unity's coordinate system.** **This should only need to be completed once after installation unless the hardware is moved or misalignment is noticed.** This will ensure that the effects shown in the projection and the people being tracked will be aligned. You will use ArUco markers (marker_0, marker_1, marker_2) and the provided `UnityConfig.exe` to calibrate the system. The `UnityConfig.exe` application projects a green circle at the origin of Unity with a 1 meter grid pattern onto the physical space. The projection represents Unity's coordinate system (the game world). The markers that you will place represent the camera's coordinate system with actual dimensions in meters.

### Prerequisites

- **Printer**: Have access to a printer for the three ArUco markers (marker_0, marker_1, marker_2) that will be generated using the LivingStream Object Tracking application. **The markers can be generated and printed in advance if needed (see step 2).**
- **Tape Measure**: Have access to a tape measure for marker placement (Note: 1m ~ 3.28ft ~ 39.36in).

### Steps

1. **Prepare**:
   - Launch `Unity_Config.exe` to project the green circle (origin) and 1-meter grid onto the physical space.
   - Launch the Object Tracking app with `RUN.bat` or manually, select **"Test Mode"**, and verify that the camera can see the entire projection.
   - Let both apps run but switch to the Unity app if needed to display the cirles and grid projection onto the floor.

2. **Generate ArUco Markers**:
   - In the Object Tracking app, select **"Config Mode"**.
   - In "Config Mode," click **"Create Markers"** to generate ArUco markers with IDs 0, 1, and 2.
   - A success message will be displayed in your terminal window after creation.
   - Find the generated marker images (e.g., `marker_0.png`, `marker_1.png`, `marker_2.png`) in the `markers` directory.
   - Print these markers (recommended size: 10-20 cm per side) for clear detection.
   - Verify the marker's integrity with the image files and note their orientation (the top-left on the image) in case the printer rotates or crops them.

3. **Place the Markers**:
   - The green circle is the origin, the red circle is right along the positive X-axis, the blue circle is up along the positive Z-axis.
   - Place **marker0** directly on the projected green circle with the top-left corner of the marker in the center of the circle.
   - All markers will be placed with the same rotation of the top-left corner.
   - Using your Tape Measure, place the top-left of **marker1** one meter away from the top-left of marker0 along the positive X-axis, in the direction of the red circle (note that marker1 may not overlap with the red circle).
   - Using your Tape Measure, place the top-left of **marker2** one meter away from the top-left of marker0 along the positive Z-axis, in the direction of the blue circle (note that marker2 may not overlap with the blue circle).

4. **Perform Calibration**:
   - If unsure, use "Test Mode" to verify all markers are visible to the camera.
   - In "Config Mode," click **"Calibrate"**.
   - View your terminal window for instructions.
   - When prompted, press **Enter** to capture a frame.
   - The application will detect the markers, compute their 3D positions using the depth camera, calculate the transformation (scale, rotation, translation) to match the Unity coordinates, and save the parameters to `calibration_config.py`.
   - The transformation saved message or an error message will appear in the terminal window.

5. **Go Live and Test with Unity_Config.exe**:
   - Return to the home screen by clicking the "Back" button or by pressing 'q'.
   - Select **"Live Mode"** from the home screen.
   - Ensure `Unity_Config.exe` is projecting onto the floor.
   - Verify the alignment by walking in the tracked area and checking if you and box that appears to represent you are aligned (the box should follow you very closely as you move around).

6. **Repeat if Necessary**

### Notes

- **Marker Placement**: Ensure markers are flat on the surface, well-lit, and free from obstructions for reliable detection.
- **Depth Range**: All markers must be within the RealSense camera's depth range during calibration.
- **Camera Stability**: Keep the camera stationary during calibration and live operation to maintain the transformation accuracy.
- **Testing Calibration**: Use "Test Mode" before and after calibration to visually confirm tracking performance if issues arise.

---

## Normal Operation

1. Launch the Object Tracking app and select "Live Mode"
2. Launch LivingStream

---

## Troubleshooting

- **Python Not Found or Wrong Version**:
  - Verify Python 3.11.9 is installed and in the PATH (`python --version`).

- **Camera Not Detected**:
  - Ensure the camera is connected via USB 3.1 Gen 1 or better.
  - Check Windows privacy settings: Search "camera privacy" and enable camera access.

- **Installation Fails**:
  - Confirm internet connectivity.
  - Update pip and retry (`python -m pip install --upgrade pip`).
  - Manually install libraries individually to isolate issues.

- **Performance Issues**:
  - Use an NVIDIA GPU for optimal performance.
  - Adjust lighting and reduce reflective surfaces as per the environment setup tips.

For additional help, consult the Intel RealSense SDK documentation or PyTorch installation guide.

---

## For Developers

- **Source Code**:
  - Main logic is in `app.py`.
  - Installation logic is in `install.py`.
  - Batch script logic is in `RUN.bat`.

- **Dependencies**:
  - Core libraries: `torch`, `torchvision`, `torchaudio`, `pyrealsense2`, `opencv-python`, `numpy`, `ultralytics`.

- **Unity Integration**:
  - Data is sent via loopback using UDP ( 127.0.0.1 : 5005 ). Ensure your Unity project is configured to receive an ID and x, y, z coordinates for each tracked object.

---
