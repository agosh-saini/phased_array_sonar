# Sonar Array Tracking System

This project implements a real-time object tracking system using three ultrasonic sensors arranged in a linear array. 


## Hardware Requirements

- Arduino board (Used R4 for testing)
- 3 ultrasonic sensors (used HC-SR04)
- USB-C power and data cable
- Computer with Python 3.x installed

## Software Requirements

- Python 3.x
- Required Python packages:
  - numpy
  - matplotlib
  - pyserial

Install required packages using:
```bash
pip install numpy matplotlib pyserial
```

## Hardware Setup

1. Connect three ultrasonic sensors to the Arduino

2. Physical sensor arrangement:
   - Sensors should be mounted in a straight line
   - Spacing between sensors: ~5cm 
   - Sensors should be oriented to face the same direction

## Arduino Code

The Arduino is to be programmed to:
1. Read distances from all three sensors
2. Format the data as comma-separated values
3. Send the data over serial at 9600 baud rate

Example Arduino output format:
```
10.5,15.2,12.3
```
Where each number represents the distance in centimeters from each sensor.

## Usage

1. Update the COM port in `main.py` to match your Arduino's port:
```python
ser = serial.Serial('COM3', 9600)  # Change COM3 to your port
```

2. Run the Python script:
```bash
python main.py
```

3. The system will:
   - Connect to the Arduino
   - Open a real-time plot window
   - Display object position as a red dot
   - Print sensor status messages to the console

## Position Estimation

The system uses different estimation strategies based on available sensors:

1. Three sensors (optimal):
   - Uses center sensor for distance
   - Uses side sensors for angle calculation
   - Most accurate position estimation

2. Two sensors:
   - If center sensor available: Uses center + one side sensor
   - If only side sensors: Uses both side sensors
   - Good accuracy with some limitations

3. One sensor:
   - Estimates position directly in front of the working sensor
   - Limited to distance-only estimation
   - Assumes object is directly in front of the sensor

## Configuration

Key parameters can be adjusted in `main.py`:
- `spacing`: Distance between sensors (default: 10cm)
- Plot limits: `ax.set_xlim(-100, 100)` and `ax.set_ylim(0, 150)`
- Maximum valid distance: `distances < 1000` (1000cm)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
