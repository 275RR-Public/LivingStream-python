import os
import subprocess
import sys
import traceback

def find_python_3119():
    """Search for Python 3.11.9 executable on the system."""
    # Get the current user's username
    try:
        username = os.environ["USERNAME"]
    except KeyError:
        try:
            username = os.getlogin()
        except Exception:
            username = None

    # Common installation paths on Windows
    search_paths = [
        r"C:\Users\All Users\AppData\Local\Programs\Python\Python311\python.exe",
        r"C:\Program Files\Python311\python.exe",
        r"C:\Program Files (x86)\Python311\python.exe",
        r"C:\Python311\python.exe"
    ]

    # Add current user's AppData path if username is available
    if username:
        user_path = f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
        search_paths.insert(0, user_path)  # Prioritize current user's path

    # Check PATH environment variable
    for path in os.environ.get("PATH", "").split(";"):
        if path and os.path.exists(path):
            potential_path = os.path.join(path, "python.exe")
            if os.path.exists(potential_path):
                try:
                    result = subprocess.run([potential_path, "--version"], capture_output=True, text=True)
                    if "Python 3.11.9" in result.stdout:
                        return potential_path
                except Exception:
                    continue

    # Check each search path
    for path in search_paths:
        if os.path.exists(path):
            try:
                result = subprocess.run([path, "--version"], capture_output=True, text=True)
                if "Python 3.11.9" in result.stdout:
                    return path
            except Exception:
                continue

    return None

def check_python_version(python_path):
    """Check the version of the specified Python executable."""
    if not python_path:
        return False
    try:
        result = subprocess.run([python_path, "--version"], capture_output=True, text=True)
        return "Python 3.11.9" in result.stdout
    except Exception:
        return False

def check_prerequisites(python_3119_path):
    """Check if required software (Python 3.11.9 and RealSense SDK) is installed and configured.
    Also ask about GPU support.
    """
    print("Installation takes some time. Please be patient.")
    print("Please ensure the following are installed before proceeding:")

    # Validate Python 3.11.9
    while True:
        python_response = input("Has Python 3.11.9 been installed? (yes/no): ").strip().lower()
        if python_response in ("yes", "y"):
            if not python_3119_path or not check_python_version(python_3119_path):
                print("Error: Python 3.11.9 was not found on your system.")
                print("Please install Python 3.11.9 from https://www.python.org/downloads/release/python-3119/")
                print("Ensure you check 'Add Python to PATH' during installation or manually add it.")
                return False, None
            break
        elif python_response in ("no", "n"):
            print("Please install Python 3.11.9 from https://www.python.org/downloads/release/python-3119/ and check 'Add Python to PATH'.")
            return False, None
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    # Validate Intel RealSense SDK
    while True:
        realsense_response = input("Has the Intel RealSense SDK been installed? (yes/no): ").strip().lower()
        if realsense_response in ("yes", "y"):
            break
        elif realsense_response in ("no", "n"):
            print("Please install the Intel RealSense SDK from https://github.com/IntelRealSense/librealsense/releases/tag/v2.56.3")
            return False, None
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    # Ask about GPU
    while True:
        gpu_response = input("Do you have at least a 1000 series or better Nvidia GPU? (yes/no): ").strip().lower()
        if gpu_response in ("yes", "y", "no", "n"):
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    print(f"Using Python 3.11.9 from: {python_3119_path}")
    return True, gpu_response


def run_command_with_output(cmd):
    """Run a command and stream its output in real-time."""
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line, end='')
    proc.wait()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd)


def main():
    # Find Python 3.11.9
    python_3119 = find_python_3119()
    success, use_gpu = check_prerequisites(python_3119)
    if not success:
        sys.exit(1)

    # Determine the directory where the script is located (should be "python" folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))         # "lib" folder
    root_dir = os.path.dirname(script_dir)                          # Root folder
    venv_dir = os.path.join(root_dir, ".venv")                      # Virtual environment path
    status_file = os.path.join(script_dir, "install_status.txt")    # Status file path

    # Create virtual environment if it doesn't exist and use Python 3.11.9
    if not os.path.exists(venv_dir):
        print("Creating virtual environment...")
        subprocess.check_call([python_3119, "-m", "venv", venv_dir])
    else:
        print("Virtual environment already exists.")

    # Set the virtual environment's Python executable path (Windows-specific)
    venv_python = os.path.join(venv_dir, "Scripts", "python.exe")

    # Update pip in the virtual environment
    print("Updating pip...")
    run_command_with_output([venv_python, "-m", "pip", "install", "--upgrade", "pip"])

    # Install PyTorch based on GPU response
    if use_gpu in ("yes", "y"):
        print("Installing PyTorch with CUDA support...")
        run_command_with_output([
            venv_python, "-m", "pip", "install", "torch", "torchvision", "torchaudio",
            "--index-url", "https://download.pytorch.org/whl/cu126"  # Adjust CUDA version as needed
        ])

    # Install the remaining required libraries
    print("Installing remaining libraries...")
    run_command_with_output([
        venv_python, "-m", "pip", "install", "pyrealsense2", "opencv-python", "numpy", "ultralytics"
    ])

    # Write install flag to install_status.txt only if all steps complete
    with open(status_file, "w") as f:
        f.write("success\n")
    print("Installation status saved to install_status.txt.")

    # Provide completion message and instructions
    print("Note: On the first run, the YOLO model will be downloaded, requiring internet access.")


if __name__ == "__main__":
    try:
        main()
        print("Exiting with code 0")
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)