import serial
import time
import numpy as np
import matplotlib.pyplot as plt


from collections import deque

# Serial port configuration for Arduino communication
ser = serial.Serial('COM4', 9600) 
time.sleep(2)  

# Configuration
max_distance = 60
spacing = 5

# Sensor positions in cm
s1_x, s2_x, s3_x = -spacing, 0, spacing  # Center sensor at 0
history_length = 50  

# Initialize position history
position_history = deque(maxlen=history_length)

def estimate_position(distances):
    """
    Input: 
        distances - numpy array of distances from the sensors to the object

    Output: 
        position - numpy array of the estimated object position [x, y]
        num_sensors - number of sensors used to estimate the position

    Info:   
        Estimate object position based on available sensor readings.
        Handles cases with 1, 2, or 3 working sensors.
        All positions are relative to center sensor at (0,0)
    """

    # Filter out invalid readings 
    valid_mask = (distances > 0) & (distances < max_distance)
    valid_distances = distances[valid_mask]
    valid_indices = np.where(valid_mask)[0]  
    
    if len(valid_distances) == 0:
        print("No valid sensor readings available")
        return [0,60], 0
    
    print(f"Using {len(valid_distances)} sensors: {valid_indices + 1}")
    
    # Case 1: Only one sensor is working
    if len(valid_distances) == 1:
        sensor_idx = valid_indices[0]
        r = valid_distances[0]

        # Left sensor
        if sensor_idx == 0:  
            #print(f"Estimated position: {-spacing}, {r}")
            return [-spacing, r], 1

        # Center sensor
        elif sensor_idx == 1:  
            #print(f"Estimated position: {0}, {r}")
            return [0, r], 1

        # Right sensor
        else:  
            #print(f"Estimated position: {spacing}, {r}")
            return [spacing, r], 1

    # Case 2: Two sensors are working
    elif len(valid_distances) == 2:

        # Center sensor
        if 1 in valid_indices:  
            r = valid_distances[valid_indices.tolist().index(1)]

            # Get the index and distance of the other sensor
            other_idx = valid_indices[valid_indices != 1][0]
            other_dist = valid_distances[valid_indices != 1][0]
            
            # Calculate the angle between the two sensors
            if other_idx == 0:  
                angle_rad = np.arctan2((other_dist - r), spacing)
            else:  
                angle_rad = np.arctan2((r - other_dist), spacing)
                
            # Conversion to Cartesian coordinates
            x = r * np.sin(angle_rad)
            y = r * np.cos(angle_rad)

            #print(f"Estimated position: {x}, {y}")

            return [x, y], 2  
            
        # Two side sensors
        else:  
            d1, d3 = valid_distances
            angle_rad = np.arctan2((d1 - d3), (2 * spacing))

            # Calculate the average distance
            r = (d1 + d3) / 2  

            # Conversion to Cartesian coordinates
            x = r * np.sin(angle_rad)
            y = r * np.cos(angle_rad)

            #print(f"Estimated position: {x}, {y}")

            return [x, y], 2  
            
    # Case 3: All three sensors are working
    else:  
        d1, d2, d3 = valid_distances

        # Center sensor
        r = d2  

        # Calculate the angle between the two side sensors
        angle_rad = np.arctan2((d1 - d3), (2 * spacing))

        # Conversion to Cartesian coordinates
        x = r * np.sin(angle_rad)
        y = r * np.cos(angle_rad)

        #  print(f"Estimated position: {x}, {y}")

        return [x, y], 3  

# Set up the plot with better styling
plt.style.use('bmh')
plt.ion()
fig, ax = plt.subplots(figsize=(10, 8))

# Plot sensor positions
sensor_positions = np.array([[s1_x, 0], [s2_x, 0], [s3_x, 0]])
ax.scatter(sensor_positions[:, 0], sensor_positions[:, 1], 
          c='blue', marker='^', s=100, label='Sensors')

# Add sensor labels
for i, pos in enumerate(sensor_positions):
    ax.annotate(f'{i+1}', (pos[0], pos[1]), 
                xytext=(0, -20), textcoords='offset points',
                ha='center', va='top')

# Plot object position and history
current_pos = ax.scatter([], [], c='red', s=100, label='Current Position')
history_pos = ax.scatter([], [], c='gray', alpha=0.3, s=50, label='Position History')

# Configure plot appearance with adjusted limits and ticks
ax.set_xlim(-40, 40)  
ax.set_ylim(0, 60)  
ax.set_aspect('equal')

# Set custom x-axis ticks with wider spacing but no labels
x_ticks = np.arange(-40, 41, 8) 
ax.set_xticks(x_ticks)

# Remove x-axis labels
ax.set_xticklabels([]) 

# Set custom y-axis ticks
y_ticks = np.arange(0, 61, 10)  
ax.set_yticks(y_ticks)
ax.set_yticklabels([f'{int(y)}' for y in y_ticks]) 

# Add grid with adjusted spacing
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_xlabel('') 
ax.set_ylabel('Distance (cm)') 
ax.set_title('Sonar Array Tracking System', pad=20)

# Add legend
ax.legend(loc='upper right')

# Add distance circles with center at (0,0)
for radius in [10, 20, 30, 40, 50]:
    circle = plt.Circle((0, 0), radius, fill=False, 
                       linestyle='--', alpha=0.3, color='gray')
    ax.add_patch(circle)
    # Center the label above the circle
    ax.annotate(f'{radius}cm', 
                xy=(0, radius),  # Point to label
                xytext=(0, 15),  # Offset upward
                textcoords='offset points',
                ha='center',     # Center horizontally
                va='bottom',     # Place above the point
                fontsize=8)      # Slightly smaller font

# Main tracking loop
while True:
    try:
        line = ser.readline().decode().strip()
        try:
            parts = line.split(',')
            distances = np.array([float(x) if x.strip() else -1 for x in parts])
            
            if len(distances) != 3:
                print(f"Warning: Expected 3 distances, got {len(distances)}")
                continue

            # Add debug printing of raw sensor values
            #print(f"Raw sensor readings - Left: {distances[0]:.1f}cm, Center: {distances[1]:.1f}cm, Right: {distances[2]:.1f}cm")
            
            position, num_sensors = estimate_position(distances)
            if position is not None:
                # Update position history
                position_history.append(position)
                
                # Update current position with color based on number of sensors
                colors = {0: 'red', 1: 'yellow', 2: 'orange', 3: 'green'}
                current_pos.set_color(colors[num_sensors])
                current_pos.set_offsets([position])
                
                # Update history positions
                if len(position_history) > 1:
                    history_pos.set_offsets(position_history)
                
                # Update plot
                fig.canvas.draw()
                fig.canvas.flush_events()
            
        except ValueError as ve:
            print("Warning: Invalid sensor reading format:", ve)
            
    except Exception as e:
        print("Error:", e)
        time.sleep(0.1)  
