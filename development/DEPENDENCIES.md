# Python Package Dependencies

This document lists all the Python packages needed for the RubiksCubeRobot project.

## Required Packages

Run the following commands to install all dependencies:

```bash
uv add opencv-python
uv add numpy
uv add pigpio
```

## Package Details

| Package | Import Name | Purpose |
|---------|-------------|---------|
| `opencv-python` | `cv2` | Computer vision library for image processing and camera operations |
| `numpy` | `numpy` | Numerical computing library for array operations and mathematical functions |
| `pigpio` | `pigpio` | Python interface to the pigpio daemon for GPIO control on Raspberry Pi |

## Usage in Project

- **opencv-python (cv2)**: Used in `cameraSensor.py` and `imageProcessor.py` for video capture, image processing, and color detection
- **numpy**: Used throughout the project for numerical operations, array manipulation, and mathematical calculations (camera sensor, image processor, cube logic)
- **pigpio**: Used in `cameraSensor.py` for controlling LED brightness through PWM on the robot's Raspberry Pi

## Additional Notes

- These packages are installed on a Raspberry Pi device running the RubiksCubeRobot
- Standard library modules (sys, time, math, copy, random) are also used but do not require `uv add` commands
- The project also includes local modules in the `maestro/` directory for servo motor control

