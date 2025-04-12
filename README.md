# LivingStream Object Tracking for Unity

LivingStream Object Tracking is an application that utilizes the Intel RealSense D435i camera to detect and track objects in real-time using computer vision techniques powered by Ultralytics YOLO11 AI. The tracked object data ID and (x, y, z coordinates) is sent via UDP to Unity for visualization, making it ideal for interactive and immersive applications.

This application is part of the larger **LivingStream project** which uses a projector to display a river with local fish. Combining the two applications, creates a projection which is interactive and reacts to people as they walk on it. The project was created in coordination with the University of Texas at Arlington and the U.S. Army Corps of Engineers for education and entertainment at one of their visitor's centers.

Source Code: \
**LivingStream-python** ([link](https://github.com/275RR-Public/LivingStream-python)) <-- you're here\
**LivingStream-unity** ([link](https://github.com/275RR-Public/LivingStream-unity))

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
  - Windows 10 or 11 machine (likely 64-bit)
  - USB 3.1 Gen 1 or better cable and port (Double-check if you notice camera delays, stutters, or blackouts)
  - Short-throw, low-latency, 1080p Projector (example: [BENQ TH671ST](https://www.benq.com/en-us/projector/cinema/th671st.html))
  - Internet access

- **Optional but Highly Recommended**:
  - NVIDIA GPU (1000 series or better, excluding the newest 5000 series) for approximately an 8x performance increase
  - AMD GPUs are NOT currently supported

**WARNING**: Running the application on a CPU instead of a NVIDIA GPU will noticeably degrade the experience. When selecting "Live Mode" in the LivingStream Object Tracking app, the app will display "cpu" or "cuda" (Nvidia GPU) to notify you of the resource being used.

---

## Software Requirements

- **Required**:
  - Python 3.11.9 ([download](https://www.python.org/downloads/release/python-3119/)) - go to bottom of page "Windows installer (64-bit)"
  - Intel RealSense SDK 2.56.3 beta ([download](https://github.com/IntelRealSense/librealsense/releases/tag/v2.56.3)) - go to Assets at bottom of page "Intel.RealSense.SDK-WIN10-2.56.3.7838.beta.exe"
  - Latest Nvidia drivers for your GPU ([download](https://www.nvidia.com/en-us/drivers/))
  - LivingStream-unity source code ([download](https://github.com/275RR-Public/LivingStream-unity))
  - LivingStream-python source code ([download](https://github.com/275RR-Public/LivingStream-python))

- **Optional**:
  - Ghostwriter (simple app for markdown files like this README.md) ([download](https://github.com/KDE/ghostwriter/releases/tag/2.1.6)) - "ghostwriter_2.1.6_win64_portable.zip"

**NOTE**: See below for specific Installation instructions to follow

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

**Note**: To keep resource usage reasonable, the number of objects that can be tracked simultaneously has been limited to 3 people.

---

## Automated Installation of LivingStream Object Tracking Using `RUN.bat`

The easiest way to install and run the application is by using the provided `RUN.bat` script. This script automates the installation process and launches the application.

### Automatic Steps

1. **Ensure Prerequisites**:
   - Install the latest Nvidia drivers for your GPU ([download](https://www.nvidia.com/en-us/drivers/))
   - Install Python 3.11.9 and check "Add Python to PATH" during installation ([download](https://www.python.org/downloads/release/python-3119/)).
   - Install the Intel RealSense SDK ([download](https://github.com/IntelRealSense/librealsense/releases/tag/v2.56.3)).
   - Verify that your Intel RealSense D435i camera is connected via a USB 3.1 Gen 1 or better port.
   - Note: You can verify the camera is working by using the RealSense Viewer that is provided in the RealSense SDK. After launching, click "Stereo Module" and "RGB Camera" to ON. You must close this app before proceeding any further.

2. **Launch `RUN.bat`**:
   - Navigate to the LivingStream-python directory in File Explorer.
   - Note: Windows might display "Defender prevented an unrecognized app", click "More Info", click "Run Anyway"
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

## Manual Installation of LivingStream Object Tracking

For users who need to troubleshoot specific steps or need to by-pass the install script: follow this manual install process.

### Manual Steps

1. **Install Python 3.11.9**:
   - Download and install Python 3.11.9 from [here](https://www.python.org/downloads/release/python-3119/).
   - During installation, check "Add Python to PATH".

2. **Install Intel RealSense SDK**:
   - Download and install the SDK from [here](https://github.com/IntelRealSense/librealsense/releases/tag/v2.56.3).

3. **Navigate to LivingSteam-python Directory**:
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

- **Double-click `RUN.bat`**:

  - RUN.bat will check for a current install
  - RUN.bat activates the virtual environment and runs the app

### Manually

1. **Navigate to LivingStream-python Directory**:
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

**Note**: "Click and Drag" a file while holding "Alt" to create shortcuts on Windows. Before releasing, Windows should indicate that a shortcut is being created. Creating shortcuts for `RUN.bat` and `LivingStream.exe` on your Desktop could simplify future use.

---

## Aligning the D435i with Unity

**IMPORTANT: After installation but before use of the system, the camera's coordinate system needs to be aligned with Unity's coordinate system.** **This should only need to be completed once after installation unless the hardware is moved, the projection is adjusted or scaled, or misalignment is noticed.** This will ensure that the effects shown in the projection and the people being tracked will be aligned. You will use ArUco markers (marker_0, marker_1, marker_2) and the provided `LivingStream.exe` to calibrate the system. The `LivingStream.exe` application in the "Calibrate" screen projects a green circle at the origin of Unity onto the physical space. The projection represents Unity's coordinate system (the game world).

### Prerequisites

- **Printer**: Have access to a printer for the three ArUco markers (marker_0, marker_1, marker_2) that will be generated using the LivingStream Object Tracking application. **The markers can be generated and printed in advance if needed (see step 2).**
- **LivingStream.exe** is located in **LivingStream-unity\Build\\\<type>\\** where type is your system **32bit or 64bit** (most likely 64bit for newer computer systems)

### Steps

1. **Prepare**:
   - **Note**: The first time you launch LivingStream, allow the network connection in the Windows Firewall notification.
   - **Note**: Windows might display "Defender prevented an unrecognized app", click "More Info", click "Run Anyway"
   - **Note**: You will have your computer's display and the projector as a display. There are multiple ways to configure these displays for your use. However, LivingStream will launch on your Primary display. It might be easiest for the following steps if you set both displays to be active with the projector as your primary display in the Nvidia control panel under "Set up multiple displays". Also note, in this configuration, when interacting with apps on your computer's display, LivingStream will lose focus and pause. You can make LivingStream active again by clicking anywhere on it.
   - Launch `LivingStream.exe`.
   - Click **"Calibrate"** in `LivingStream.exe` to disable the demo (main menu) and prepare Unity for calibration.
   - Launch the Object Tracking app with `RUN.bat` or manually (if not already open), select **"Test Mode"**, and verify that the camera can see the entire projection.

2. **Generate ArUco Markers**:
   - In the Object Tracking app, select **"Config Mode"**.
   - In "Config Mode," click **"Create Markers"** to generate ArUco markers with IDs 0, 1, and 2.
   - A success message will be displayed in your terminal window after creation.
   - Find the generated marker images (e.g., `marker_0.png`, `marker_1.png`, `marker_2.png`) in the `LivingStream-python\markers` directory.
   - Print these markers (recommended size: 10-15 cm per side) for clear detection.
   - Verify the printed marker's integrity with the image files and note their orientation (the top-left on the image) in case the printer rotates or crops them.

3. **Perform Calibration STEP 1 - Place the Markers**:
   - **Note**: The green circle is the origin, the red circle is right along the positive X-axis, the blue circle is up along the positive Z-axis.
   - **Note**: We are placing markers from the perspective of the Unity camera (the projector). In other words, face the projection so you are looking at the green circle with the red circle to your right, the "Back" button close to you, and the blue circle farthest from you.
   - **Note**: All markers will be placed with the same rotation (rotation doesn't matter as long as they are the same).
   - Place **marker0** directly on the projected **green** circle with the **top-left corner of the marker in the center of the circle**. Make sure the black of the marker itself (not just the printer paper) is in the center of the circle.
   - Place the top-left corner of **marker1** in the center of the **red** circle.
   - Place the top-left corner of **marker2** in the center of the **blue** circle.

4. **Perform Calibration STEP 2 - Calibrate**:
   - In the Object Tracking app under "Config Mode," click **"Calibrate"**.
   - View your terminal window for instructions, you should see "Place all the ArUco markers then press Enter when ready...".
   - Now that all markers have been placed, press Enter to capture the frame.
   - The application will detect the markers, compute their 3D positions using the RGB and depth cameras, calculate the transformation (scale, rotation, translation) to match the Unity coordinates, and save it to `calibration_config.py`.
   - The **transformation saved message** (or an error message if failed) will appear in the terminal window.
   - If you repeatly fail to save the transformaton, see the troubleshooting section below.

5. **Go Live and Test with LivingStream.exe**:
   - In the Object Tracking app, Return to the home screen by clicking the "Back" button or by pressing 'q'.
   - Select **"Live Mode"** from the home screen.
   - In `LivingStream.exe`, go "Back" to Demo mode (main menu).
   - Optional: You can also walk around in the Demo mode of LivingStream, but the tracking will not follow you exactly.
   - Verify the alignment by walking around in the **Play** mode of LivingStream for a complete test of the system.

6. **Repeat if Necessary**

### Notes

- **Marker Placement**: Ensure markers are flat on the surface, well-lit, and free from obstructions for reliable detection.
- **Depth Range**: All markers must be within the RealSense camera's depth range during calibration.
- **Camera Stability**: Keep the camera stationary during calibration and live operation to maintain the transformation accuracy.
- **Testing Calibration**: Use "Test Mode" before and after calibration to visually confirm tracking performance if issues arise.

---

## Normal Operation (after all installation and calibration)

1. Launch the LivingStream Object Tracking app using **`RUN.bat` and select "Live Mode"**
2. Launch **`LivingStream.exe` and select "Play"**

Note: Both apps need to be running for the intended experience.

---

## Troubleshooting

- **Python Not Found or Wrong Version**:
  - Verify Python 3.11.9 is installed and in the PATH (`python --version` in Windows Terminal).

- **Camera Not Detected**:
  - Close all applications.
    - Launch the RealSense Viewer which is included in the RealSense SDK to verify if working.
  - Check Windows privacy settings: Search "camera privacy" and enable camera access, both generally and for apps.
    - Launch the RealSense Viewer which is included in the RealSense SDK to verify if working.
  - Ensure the camera is connected via USB 3.1 Gen 1 or better (cable and port).
  - Unplug the USB, wait a few seconds, and replug the USB.
    - Launch the RealSense Viewer which is included in the RealSense SDK to verify if working.
  - Try a different USB port.
    - Launch the RealSense Viewer which is included in the RealSense SDK to verify if working.
  - Restart Windows.
    - Launch the RealSense Viewer which is included in the RealSense SDK to verify if working.
  - Uninstall then reinstall the RealSense SDK.
    - Launch the RealSense Viewer which is included in the RealSense SDK to verify if working.
  - If there was a recent Window's update, consider "Rolling back" the update.
    - Launch the RealSense Viewer which is included in the RealSense SDK to verify if working.

- **RUN.bat hangs when launching**:
  - This usually occurs when the RealSense camera is not responding
    - See Camera Not Detected

- **Installation Fails**:
  - Confirm internet connectivity.
  - Update pip and retry (`python -m pip install --upgrade pip`).
  - Manually install libraries individually to isolate issues.

- **Performance Issues**:
  - Use a NVIDIA GPU for optimal performance.
  - Adjust lighting and reduce reflective surfaces as per the environment setup tips.

- **Selected GPU during install but "Live Mode" showing CPU usage**:
  - Install the latest Nvidia drivers
  - Delete the .venv folder and install_status.txt file and perform installation again
  - See PyTorch installation documentation

- **Marker Calibration Issues**:
  - Verify the Markers are large enough (10-15cm per side) and are not distorted or altered.
  - Reduce reflective surfaces (possibly use floor mats), very strong/weak light sources, and obstructions.
  - After positioning the markers, try turning the projector off and then running the calibration.
  - View Environment Setup again, the camera can not take depth measurements beyond 4 meters and light sources can not be too weak but also not too strong.

For additional help, consult the Intel RealSense SDK documentation or Projector manuals.

---

## For Developers

- **Source Code for LivingStream-python**:
  - Main logic is in `app.py`.
  - Installation logic is in `install.py`.
  - Batch script logic is in `RUN.bat`.
  - Object detection and tracking logic is in `tracker.py`.

- **Dependencies**:
  - Core libraries: `torch`, `torchvision`, `torchaudio`, `pyrealsense2`, `opencv-python`, `numpy`, `ultralytics`.
  - `requirements.txt` is included as a point of reference for the versioning used during development.

- **Unity Integration**:
  - Data is sent via loopback using UDP ( 127.0.0.1 : 5005 ). Ensure your Unity project is listening on this port to receive an ID and x, y, z coordinates for each tracked object.

- **Class Variables**:
  - A number of important variables are used as class variables for easy alteration such as `max_tracks` for the maximum of number of people to track at one time or `roi_max_depth` for the maximum distance allowed for depth measurements.

- **Expansion of Features in the Future**:
  - The object tracking in `lib/tracker.py` is already using pose estimation with skeleton tracking keypoints to track each person's feet. This makes adding additional features in the future using a person's hands or other joints almost trivial.
  - Using OpenCV as the GUI is simple but limiting. In the future, refactor to PySide for a complete GUI implementation.

- **Other Use Cases**:
  - The calibration process is designed to map a person into Unity. For our use, the calibration process ensures Unity objects follow real world movements. However, by physically spacing the markers 1m apart during calibration while keeping marker0 at the origin, the transformation will map a 1m movement in the real world to a 1m movement in Unity.

---
