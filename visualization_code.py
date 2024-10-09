import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import tkinter as tk
from scipy import signal

class FFTPlotter:
    def __init__(self, master):
        self.master = master
        master.title("Real-time FFT Plotter")
        
        # Configure serial connection
        self.ser = serial.Serial('COM4', 115200, timeout=1)
        
        # Initialize data storage
        self.frequencies = []
        self.magnitudes = []
        
        # Create GUI elements
        self.create_widgets()
        
        # Set up the plot
        self.setup_plot()
        
        # Start animation
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=100, blit=False)

    def create_widgets(self):
        control_frame = tk.Frame(self.master)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.start_stop_button = tk.Button(control_frame, text="Stop", command=self.toggle_acquisition)
        self.start_stop_button.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.line, = self.ax.plot([], [])
        
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('Magnitude')
        self.ax.set_title('Real-time FFT from Teensy')
        
        canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_plot(self, frame):
        if self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                data_points = line.split(';')
                
                self.frequencies = []
                self.magnitudes = []
                
                for point in data_points:
                    if point:
                        freq, mag = map(float, point.split(','))
                        self.frequencies.append(freq)
                        self.magnitudes.append(mag)
                
                # Apply additional processing if needed (e.g., windowing)
                self.magnitudes = signal.windows.hann(len(self.magnitudes)) * self.magnitudes
                
                self.line.set_data(self.frequencies, self.magnitudes)
                self.ax.relim()
                self.ax.autoscale_view()
                
            except ValueError:
                pass
        
        return [self.line]

    def toggle_acquisition(self):
        if self.start_stop_button['text'] == "Stop":
            self.ani.event_source.stop()
            self.start_stop_button['text'] = "Start"
        else:
            self.ani.event_source.start()
            self.start_stop_button['text'] = "Stop"

    def on_closing(self):
        self.ser.close()
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FFTPlotter(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
    

"""
actually the teensyADCGUI can integrate simRC FFT functionality with the correct COM ports and baud rate with data compression, please see associated library references and modify the script above to accomplish the desired task here are some full scope adjustments-- 
https://github.com/nazeern/nanotech/blob/main/app.py
https://github.com/nazeern/nanotech/blob/main/cnt_param_to_cap.py
https://github.com/nazeern/nanotech/blob/main/SimRC.ipynb
https://github.com/nazeern/nanotech/blob/main/nitro_app.py

import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import pandas as pd
import time

class TeensyADCGUI:
    def __init__(self, master):
        self.master = master
        master.title("Teensy ADC Reader")
        
        # Configure serial connection
        self.ser = serial.Serial('COM4', 115200, timeout=1)  # Adjust COM port as needed
        
        # Initialize data storage
        self.num_channels = 4
        self.data = [[] for _ in range(self.num_channels)]
        self.max_data_points = 1000
        
        # Create GUI elements
        self.create_widgets()
        
        # Set up the plot
        self.setup_plot()
        
        # Start animation
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=50, blit=False)

    def create_widgets(self):
        # Create a frame for controls
        control_frame = ttk.Frame(self.master)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Add a start/stop button
        self.start_stop_button = ttk.Button(control_frame, text="Stop", command=self.toggle_acquisition)
        self.start_stop_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add a save button
        self.save_button = ttk.Button(control_frame, text="Save Data", command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.lines = [self.ax.plot([], [], label=f'Channel {i+1}')[0] for i in range(self.num_channels)]
        
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('ADC Value')
        self.ax.set_title('Real-time ADC Readings from Teensy')
        self.ax.legend()
        
        canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def update_plot(self, frame):
        if self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                values = list(map(int, line.split(',')))
                
                for i, value in enumerate(values):
                    self.data[i].append(value)
                    if len(self.data[i]) > self.max_data_points:
                        self.data[i].pop(0)
                
                for i, line in enumerate(self.lines):
                    line.set_data(range(len(self.data[i])), self.data[i])
                
                self.ax.relim()
                self.ax.autoscale_view()
            except ValueError:
                pass  # Ignore any parsing errors
        
        return self.lines   

    def update_plot(self, frame):
        if self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                # Parse data assuming comma-separated peak frequencies and magnitudes
                peaks = list(map(float, line.split(',')))
                frequencies = peaks[::2]  # Extract every other element for frequencies
                magnitudes = peaks[1::2]  # Extract every other element for magnitudes

                # Clear existing plot data
                self.lines[0].set_data([], [])

                # Update plot with peak frequencies and magnitudes (adjust according to your needs)
                self.lines[0] = self.ax.bar(frequencies, magnitudes, color='blue', label='FFT Peaks')
                self.ax.set_xlabel('Frequency (Hz)')
                self.ax.set_ylabel('Magnitude')
                self.ax.legend()
                self.ax.set_title('FFT of ADC Readings from Teensy')

                self.fig.canvas.draw()
        except ValueError:
    pass`

    def toggle_acquisition(self):
        if self.start_stop_button['text'] == "Stop":
            self.ani.event_source.stop()
            self.start_stop_button['text'] = "Start"
        else:
            self.ani.event_source.start()
            self.start_stop_button['text'] = "Stop"

    def save_data(self):
        df = pd.DataFrame(dict(zip([f'Channel_{i+1}' for i in range(self.num_channels)], self.data)))
        filename = f'adc_data_{int(time.time())}.csv'
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def on_closing(self):
        self.ser.close()
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TeensyADCGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import serial
import time

# Configure serial connection (adjust for your Teensy's COM port)
ser = serial.Serial('COM4', 9600, timeout=1)

def read_impedance_data(duration):
    data = []
    start_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            impedance = ser.readline().decode('utf-8').strip()
            if impedance:
                print(impedance)
                data.append(float(impedance.split()[-1]))  # Extract impedance value from string
        except Exception as e:
            print(e)
            continue
    
    return data

# Read impedance data for 60 seconds
impedance_data = read_impedance_data(60)

# Plotting the impedance data
plt.plot(np.arange(len(impedance_data)), impedance_data, color='blue', label='Impedance (Ohms)')
plt.title('Real-time Impedance Measurements')
plt.xlabel('Time (s)')
plt.ylabel('Impedance (Ohms)')
plt.legend()
plt.grid(True)
plt.show()

# Save data to CSV
df = pd.DataFrame({'Impedance': impedance_data})
df.to_csv('impedance_data.csv', index=False)




import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Teensy serial port configuration
ser = serial.Serial('/dev/ttyACM0', 9600)  # Update this port to the correct Teensy port

# Initialize lists for real-time data plotting
data = []

# Setup the plot
fig, ax = plt.subplots()
line, = ax.plot(data)

def update(frame):
    if ser.in_waiting > 0:
        value = ser.readline().decode().strip()
        try:
            data.append(int(value))  # Convert string to integer
            if len(data) > 100:
                data.pop(0)
            line.set_ydata(data)
            line.set_xdata(range(len(data)))
            ax.relim()
            ax.autoscale_view()
        except ValueError:
            pass

ani = FuncAnimation(fig, update, interval=100)

plt.show()





import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Teensy serial port configuration
ser = serial.Serial('/dev/ttyACM0', 9600)  # Update this port to the correct Teensy port

# Initialize lists for real-time data plotting
data = []

# Setup the plot
fig, ax = plt.subplots()
line, = ax.plot(data)

def update(frame):
    if ser.in_waiting > 0:
        value = ser.readline().decode().strip()
        try:
            data.append(int(value))  # Convert string to integer
            if len(data) > 100:
                data.pop(0)
            line.set_ydata(data)
            line.set_xdata(range(len(data)))
            ax.relim()
            ax.autoscale_view()
        except ValueError:
            pass

ani = FuncAnimation(fig, update, interval=100)

plt.show()
"""