"""import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Set up the serial port (ensure this matches the correct COM port for your Teensy)
serial_port = 'COM5'  # Adjust this to your system's port
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

# Initialize figure and subplots
fig, ax_adc = plt.subplots(figsize=(10, 6))

# ADC Plot (Time Domain)
time_axis = np.linspace(0, 1, 1024)  # Time axis for ADC
adc_line, = ax_adc.plot(time_axis, np.zeros(1024))
ax_adc.set_title('ADC Signal')
ax_adc.set_xlabel('Time (s)')
ax_adc.set_ylabel('Voltage')

# Set axis limits
ax_adc.set_ylim(0, 4095)  # ADC values (12-bit, 0 to 4095)

# ADC data buffer
adc_values = np.zeros(1024)

# Update function to refresh the plots
def update(frame):
    if ser.in_waiting:  # Check if data is available in the serial buffer
        data = ser.readline().decode('utf-8').strip()  # Read and decode the incoming data
        print("Received:", data)  # Optional: for debugging

        # Parse ADC data
        if data.startswith("ADC"):
            try:
                adc_value = float(data.split(',')[1])  # Get the ADC value
                adc_values[:-1] = adc_values[1:]  # Shift values to the left
                adc_values[-1] = adc_value  # Add new value to the end
                adc_line.set_ydata(adc_values)  # Update ADC plot data
            except ValueError:
                print("Invalid ADC data:", data)

    return adc_line,

# Animate the plot
ani = FuncAnimation(fig, update, interval=100)  # Refresh every 100ms

# Show the plot
plt.tight_layout()
plt.show()
"""
import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import csv
import time

# Set up the serial port (ensure this matches the correct COM port for your Teensy)
serial_port = 'COM5'  # Adjust this to your system's port
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

# Initialize figure and subplots
fig, ax_adc = plt.subplots(figsize=(10, 6))

# ADC Plot (Time Domain) - Extend for multiple channels
num_channels = 4  # Number of ADC channels (A10 to A13)
time_axis = np.linspace(0, 1, 1024)  # Time axis for ADC
adc_lines = [ax_adc.plot(time_axis, np.zeros(1024), label=f"ADC {i+10}")[0] for i in range(num_channels)]
ax_adc.set_title('ADC Signals')
ax_adc.set_xlabel('Time (s)')
ax_adc.set_ylabel('ADC Value')

# Set axis limits
ax_adc.set_ylim(0, 1023)  # 10-bit ADC values (0 to 1023)

# ADC data buffers for multiple channels
adc_values = [np.zeros(1024) for _ in range(num_channels)]

# CSV file setup
csv_file = open("adc_data.csv", mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp"] + [f"ADC{i+10}" for i in range(num_channels)])

# Update function to refresh the plots
def update(frame):
    if ser.in_waiting:  # Check if data is available in the serial buffer
        data = ser.readline().decode('utf-8').strip()  # Read and decode the incoming data
        print("Received:", data)  # Optional: for debugging
        
        # Check for "ADC Pin" to parse ADC data from Teensy
        if "ADC Pin" in data:
            try:
                # Parse multiple ADC values
                parts = data.split(', ')
                adc_channel = int(parts[0].split(':')[1].strip()[1:]) - 10  # Extract ADC Pin (A10 to A13)
                adc_value = float(parts[1].split(':')[1].strip())  # Extract ADC Value
                
                # Update buffer for corresponding channel
                adc_values[adc_channel][:-1] = adc_values[adc_channel][1:]  # Shift values to the left
                adc_values[adc_channel][-1] = adc_value  # Add new value to the end
                
                # Update plot for each ADC channel
                for i, line in enumerate(adc_lines):
                    line.set_ydata(adc_values[i])

                # Write to CSV
                timestamp = time.time()
                csv_writer.writerow([timestamp] + [adc_values[i][-1] for i in range(num_channels)])

            except (ValueError, IndexError):
                print("Invalid data:", data)

    return adc_lines

# Animate the plot
ani = FuncAnimation(fig, update, interval=100)  # Refresh every 100ms

# Show the plot
plt.legend()
plt.tight_layout()
plt.show()

# Close the CSV file when done
csv_file.close()
