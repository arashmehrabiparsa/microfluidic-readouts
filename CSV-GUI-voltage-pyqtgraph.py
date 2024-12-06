"""

#voltage values serially plotted new library 

import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np

# Set up serial connection
serial_port = 'COM5'
baud_rate = 921600
ser = serial.Serial(serial_port, baud_rate)

# Set up the PyQtGraph window
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(show=True, title="Real-Time ADC Voltage Data from Teensy")
win.resize(1000, 600)
plot = win.addPlot(title="ADC Voltages")
plot.setYRange(0, 3.3)  # Set Y-axis to voltage range (0V to 3.3V)

# Set up curves for each ADC channel
curves = []
num_channels = 4
for i in range(num_channels):
    curve = plot.plot(pen=(i, num_channels))
    curves.append(curve)

# Data buffer for plotting
buffer_size = 500  # Increased buffer size
data_buffers = [np.zeros(buffer_size) for _ in range(num_channels)]
x = np.linspace(-buffer_size, 0, buffer_size)

# Update function for real-time plotting
def update():
    global data_buffers
    if ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            if "ADC Pin" in line:
                parts = line.split(', ')
                channel = int(parts[0].split(':')[1].strip()[1:]) - 10
                adc_value = int(parts[1].split(':')[1].strip())
                voltage = (adc_value / 1023.0) * 3.3  # Convert ADC value to voltage
                
                if 0 <= channel < num_channels:
                    # Shift buffer and insert new voltage value
                    data_buffers[channel][:-1] = data_buffers[channel][1:]
                    data_buffers[channel][-1] = voltage  # Store voltage instead of ADC value
                    
                    # Update the plot data
                    curves[channel].setData(x, data_buffers[channel])
        except (ValueError, IndexError):
            pass

# Set up timer for continuous updates
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)  # Update every 50ms

# Start the PyQt event loop
if __name__ == '__main__':
    QtWidgets.QApplication.instance().exec_()



#serial plotting voltages with new library """


"""seeking to add checkbox funcitonality to chgoose which channels to display or not"""

import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np

# Set up serial connection
serial_port = 'COM5'  # Adjust this to your system's port
baud_rate = 921600
ser = serial.Serial(serial_port, baud_rate)

# Set up the PyQtGraph window
app = QtWidgets.QApplication([])
main_layout = QtWidgets.QVBoxLayout()

# Create a widget for the main layout
main_widget = QtWidgets.QWidget()
main_widget.setLayout(main_layout)

# Set up the PyQtGraph plot
win = pg.GraphicsLayoutWidget(show=True, title="Real-Time ADC Voltage Data from Teensy")
main_layout.addWidget(win)

# Set background color
win.setBackground('w')  # Change to white background

# Add a plot
plot = win.addPlot(title="ADC Voltages")
plot.setYRange(0, 3.3)  # Set Y-axis to voltage range (0V to 3.3V)

# Set up curves for each ADC channel
curves = []
num_channels = 4
for i in range(num_channels):
    curve = plot.plot(pen=(i, num_channels))
    curves.append(curve)

# Data buffer for plotting
buffer_size = 500  # Increased buffer size
data_buffers = [np.zeros(buffer_size) for _ in range(num_channels)]
x = np.linspace(-buffer_size, 0, buffer_size)

# Create a vertical layout for checkboxes
checkbox_layout = QtWidgets.QVBoxLayout()

# Create checkboxes for each channel
checkboxes = []
def create_checkbox(label, channel_index):
    cb = QtWidgets.QCheckBox(label)
    cb.setChecked(True)  # Start with all channels checked
    cb.stateChanged.connect(lambda: toggle_curve(channel_index, cb.isChecked()))
    checkbox_layout.addWidget(cb)
    checkboxes.append(cb)

def toggle_curve(channel_index, is_checked):
    if is_checked:
        curves[channel_index].show()  # Show curve
    else:
        curves[channel_index].hide()  # Hide curve

# Add checkboxes to the layout
for i in range(num_channels):
    create_checkbox(f"ADC Channel {i + 10}", i)

# Create a widget for the checkboxes and set its layout
checkbox_widget = QtWidgets.QWidget()
checkbox_widget.setLayout(checkbox_layout)

# Add the checkbox widget to the main layout
main_layout.addWidget(checkbox_widget)

# Update function for real-time plotting
def update():
    global data_buffers
    if ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8').strip()
            if "ADC Pin" in line:
                parts = line.split(', ')
                channel = int(parts[0].split(':')[1].strip()[1:]) - 10
                adc_value = int(parts[1].split(':')[1].strip())
                voltage = (adc_value / 1023.0) * 3.3  # Convert ADC value to voltage
                
                if 0 <= channel < num_channels:
                    # Shift buffer and insert new voltage value
                    data_buffers[channel][:-1] = data_buffers[channel][1:]
                    data_buffers[channel][-1] = voltage  # Store voltage instead of ADC value
                    
                    # Update the plot data only if the channel is checked
                    if checkboxes[channel].isChecked():
                        curves[channel].setData(x, data_buffers[channel])
        except (ValueError, IndexError):
            pass

# Set up timer for continuous updates
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)  # Update every 50ms

# Start the PyQt event loop
if __name__ == '__main__':
    main_widget.show()
    QtWidgets.QApplication.instance().exec_()
