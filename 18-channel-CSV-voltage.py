"""# WRITE TO CSV BUT DISPLAY ALL 18 CHANNELS REAL TIME
import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np
import csv
import os

# Serial connection setup
serial_port = 'COM5'  # Update as needed
baud_rate = 921600
ser = serial.Serial(serial_port, baud_rate)

# CSV logging setup
csv_filename = 'adc_data_log.csv'
file_exists = os.path.isfile(csv_filename)
csv_file = open(csv_filename, mode='a', newline='')
csv_writer = csv.writer(csv_file)
if not file_exists:
    csv_writer.writerow(['Timestamp'] + [f'ADC Pin A{10 + i}' for i in range(18)])

# PyQtGraph setup
app = QtWidgets.QApplication([])

# Main window setup
main_window = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout()
main_window.setLayout(layout)

# Plot widget for ADC voltages
plot_widget = pg.GraphicsLayoutWidget(show=True, title="Real-Time ADC Voltage Data")
plot_widget.setBackground('w')
plot = plot_widget.addPlot(title="ADC Voltages")
plot.setYRange(0, 3.3)

# Add plot widget to the main layout
layout.addWidget(plot_widget)

# Set up channels
num_channels = 18  # Number of ADC pins used
curves = []
for i in range(num_channels):
    curve = plot.plot(pen=(i, num_channels))
    curves.append(curve)

# Data buffers for smooth plotting
buffer_size = 500
data_buffers = [np.zeros(buffer_size) for _ in range(num_channels)]
x = np.linspace(-buffer_size, 0, buffer_size)

# Checkboxes for showing/hiding channels
checkbox_layout = QtWidgets.QVBoxLayout()
checkboxes = []

def create_checkbox(label, channel_index):
    cb = QtWidgets.QCheckBox(label)
    cb.setChecked(True)
    cb.stateChanged.connect(lambda: toggle_curve(channel_index, cb.isChecked()))
    checkbox_layout.addWidget(cb)
    checkboxes.append(cb)

def toggle_curve(channel_index, is_checked):
    curves[channel_index].setVisible(is_checked)

for i in range(num_channels):
    create_checkbox(f"ADC Pin A{10 + i}", i)

# Add checkboxes to the main layout in a separate widget
checkbox_widget = QtWidgets.QWidget()
checkbox_widget.setLayout(checkbox_layout)
layout.addWidget(checkbox_widget)

# Data processing function
def process_data():
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if "ADC Pin" in line:
            parts = line.split(", ")
            channel = int(parts[0].split(" ")[2][1:]) - 10
            adc_value = int(parts[1].split(":")[1].strip())
            voltage = (adc_value / 1023.0) * 3.3
            if 0 <= channel < num_channels:
                data_buffers[channel][:-1] = data_buffers[channel][1:]
                data_buffers[channel][-1] = voltage
                if checkboxes[channel].isChecked():
                    curves[channel].setData(x, data_buffers[channel])

                timestamp = QtCore.QTime.currentTime().toString()
                csv_writer.writerow([timestamp] + [data_buffers[i][-1] for i in range(num_channels)])
                csv_file.flush()

# Timer for regular updates
timer = QtCore.QTimer()
timer.timeout.connect(process_data)
timer.start(50)

# Start the main window
main_window.show()

# Start the GUI
if __name__ == '__main__':
    QtWidgets.QApplication.instance().exec_()








"""













"""









import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np
import csv
import os

# Serial connection setup
serial_port = 'COM5'  # Update as needed
baud_rate = 921600
ser = serial.Serial(serial_port, baud_rate)

# CSV logging setup
csv_filename = 'adc_data_log.csv'
csv_file = open(csv_filename, mode='w', newline='')  # 'w' mode overwrites the file each time
csv_writer = csv.writer(csv_file)
# Write header
csv_writer.writerow(['Timestamp'] + [f'ADC Pin A{10 + i}' for i in range(18)])

# PyQtGraph setup
app = QtWidgets.QApplication([])

# Main window setup
main_window = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout()
main_window.setLayout(layout)

# Plot widget for ADC voltages
plot_widget = pg.GraphicsLayoutWidget(show=True, title="Real-Time ADC Voltage Data")
plot_widget.setBackground('w')
plot = plot_widget.addPlot(title="ADC Voltages")
plot.setYRange(0, 3.3)

# Add plot widget to the main layout
layout.addWidget(plot_widget)

# Set up channels
num_channels = 18  # Number of ADC pins used
curves = []
for i in range(num_channels):
    curve = plot.plot(pen=(i, num_channels))
    curves.append(curve)

# Data buffers for smooth plotting
buffer_size = 500
data_buffers = [np.zeros(buffer_size) for _ in range(num_channels)]
x = np.linspace(-buffer_size, 0, buffer_size)

# Checkboxes for showing/hiding channels
checkbox_layout = QtWidgets.QVBoxLayout()
checkboxes = []

def create_checkbox(label, channel_index):
    cb = QtWidgets.QCheckBox(label)
    cb.setChecked(True)
    cb.stateChanged.connect(lambda: toggle_curve(channel_index, cb.isChecked()))
    checkbox_layout.addWidget(cb)
    checkboxes.append(cb)

def toggle_curve(channel_index, is_checked):
    curves[channel_index].setVisible(is_checked)

for i in range(num_channels):
    create_checkbox(f"ADC Pin A{10 + i}", i)

# Add checkboxes to the main layout in a separate widget
checkbox_widget = QtWidgets.QWidget()
checkbox_widget.setLayout(checkbox_layout)
layout.addWidget(checkbox_widget)

# Data processing function
def process_data():
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if "ADC Pin" in line:
            parts = line.split(", ")
            channel = int(parts[0].split(" ")[2][1:]) - 10
            adc_value = int(parts[1].split(":")[1].strip())
            voltage = (adc_value / 1023.0) * 3.3
            if 0 <= channel < num_channels:
                data_buffers[channel][:-1] = data_buffers[channel][1:]
                data_buffers[channel][-1] = voltage
                if checkboxes[channel].isChecked():
                    curves[channel].setData(x, data_buffers[channel])

                timestamp = QtCore.QTime.currentTime().toString()
                csv_writer.writerow([timestamp] + [data_buffers[i][-1] for i in range(num_channels)])
                csv_file.flush()  # Ensure immediate writing to disk

# Timer for regular updates
timer = QtCore.QTimer()
timer.timeout.connect(process_data)
timer.start(50)

# Start the main window
main_window.show()

# Start the GUI
if __name__ == '__main__':
    QtWidgets.QApplication.instance().exec_()
"""






"""

#WRITE TO CSV NON-PREFFERED COL ROW FORMAT HEADINGS
import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np
import csv
import os

# Serial connection setup
serial_port = 'COM5'  # Update as needed
baud_rate = 921600
ser = serial.Serial(serial_port, baud_rate)

# CSV logging setup
csv_filename = 'adc_data_log.csv'
csv_file = open(csv_filename, mode='w', newline='')  # 'w' mode overwrites the file each time
csv_writer = csv.writer(csv_file)

# PyQtGraph setup
app = QtWidgets.QApplication([])

# Main window setup
main_window = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout()
main_window.setLayout(layout)

# Plot widget for ADC voltages
plot_widget = pg.GraphicsLayoutWidget(show=True, title="Real-Time ADC Voltage Data")
plot_widget.setBackground('w')
plot = plot_widget.addPlot(title="ADC Voltages")
plot.setYRange(0, 3.3)

# Add plot widget to the main layout
layout.addWidget(plot_widget)

# Set up channels
num_channels = 18  # Number of ADC pins used
curves = []
for i in range(num_channels):
    curve = plot.plot(pen=(i, num_channels))
    curves.append(curve)

# Data buffers for smooth plotting
buffer_size = 500
data_buffers = [np.zeros(buffer_size) for _ in range(num_channels)]
x = np.linspace(-buffer_size, 0, buffer_size)

# Checkboxes for showing/hiding channels
checkbox_layout = QtWidgets.QVBoxLayout()
checkboxes = []

def create_checkbox(label, channel_index):
    cb = QtWidgets.QCheckBox(label)
    cb.setChecked(True)
    cb.stateChanged.connect(lambda: toggle_curve(channel_index, cb.isChecked()))
    checkbox_layout.addWidget(cb)
    checkboxes.append(cb)

def toggle_curve(channel_index, is_checked):
    curves[channel_index].setVisible(is_checked)

for i in range(num_channels):
    create_checkbox(f"ADC Pin A{10 + i}", i)

# Add checkboxes to the main layout in a separate widget
checkbox_widget = QtWidgets.QWidget()
checkbox_widget.setLayout(checkbox_layout)
layout.addWidget(checkbox_widget)

# Data processing function
def process_data():
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if "ADC Pin" in line:
            parts = line.split(", ")
            channel = int(parts[0].split(" ")[2][1:]) - 10
            adc_value = int(parts[1].split(":")[1].strip())
            voltage = (adc_value / 1023.0) * 3.3
            if 0 <= channel < num_channels:
                data_buffers[channel][:-1] = data_buffers[channel][1:]
                data_buffers[channel][-1] = voltage
                if checkboxes[channel].isChecked():
                    curves[channel].setData(x, data_buffers[channel])

                timestamp = QtCore.QTime.currentTime().toString()
                
                # Write received data to CSV in formatted style
                formatted_received = f"Received: ADC Pin: A{10 + channel}, ADC Value: {adc_value}, Voltage: {voltage:.4f} V"
                csv_writer.writerow([formatted_received])

                # Writing an example of invalid data
                formatted_invalid = f"Invalid data: ADC Pin: A{10 + channel}, ADC Value: {adc_value}, Voltage: {voltage:.4f} V"
                csv_writer.writerow([formatted_invalid])
                
                csv_file.flush()  # Ensure immediate writing to disk

# Timer for regular updates
timer = QtCore.QTimer()
timer.timeout.connect(process_data)
timer.start(50)

# Start the main window
main_window.show()

# Start the GUI
if __name__ == '__main__':
    QtWidgets.QApplication.instance().exec_()
"""




"""
import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np
import csv
import os

# Serial connection setup
serial_port = 'COM5'  # Update as needed
baud_rate = 921600
ser = serial.Serial(serial_port, baud_rate)

# CSV logging setup
csv_filename = 'adc_data_log.csv'
csv_file = open(csv_filename, mode='w', newline='')  # 'w' mode overwrites the file each time
csv_writer = csv.writer(csv_file)

# Define fixed-width formatting for CSV columns
header_format = "{:<15}" + "{:<12}" * 18
row_format = "{:<15}" + "{:<12.4f}" * 18

# Write header
csv_writer.writerow(['Timestamp'] + [f'ADC Pin A{10 + i}' for i in range(18)])

# PyQtGraph setup
app = QtWidgets.QApplication([])

# Main window setup
main_window = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout()
main_window.setLayout(layout)

# Plot widget for ADC voltages
plot_widget = pg.GraphicsLayoutWidget(show=True, title="Real-Time ADC Voltage Data")
plot_widget.setBackground('w')
plot = plot_widget.addPlot(title="ADC Voltages")
plot.setYRange(0, 3.3)

# Add plot widget to the main layout
layout.addWidget(plot_widget)

# Set up channels
num_channels = 18  # Number of ADC pins used
curves = []
for i in range(num_channels):
    curve = plot.plot(pen=(i, num_channels))
    curves.append(curve)

# Data buffers for smooth plotting
buffer_size = 500
data_buffers = [np.zeros(buffer_size) for _ in range(num_channels)]
x = np.linspace(-buffer_size, 0, buffer_size)

# Checkboxes for showing/hiding channels
checkbox_layout = QtWidgets.QVBoxLayout()
checkboxes = []

def create_checkbox(label, channel_index):
    cb = QtWidgets.QCheckBox(label)
    cb.setChecked(True)
    cb.stateChanged.connect(lambda: toggle_curve(channel_index, cb.isChecked()))
    checkbox_layout.addWidget(cb)
    checkboxes.append(cb)

def toggle_curve(channel_index, is_checked):
    curves[channel_index].setVisible(is_checked)

for i in range(num_channels):
    create_checkbox(f"ADC Pin A{10 + i}", i)

# Add checkboxes to the main layout in a separate widget
checkbox_widget = QtWidgets.QWidget()
checkbox_widget.setLayout(checkbox_layout)
layout.addWidget(checkbox_widget)

# Data processing function
def process_data():
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if "ADC Pin" in line:
            parts = line.split(", ")
            channel = int(parts[0].split(" ")[2][1:]) - 10
            adc_value = int(parts[1].split(":")[1].strip())
            voltage = (adc_value / 1023.0) * 3.3
            if 0 <= channel < num_channels:
                data_buffers[channel][:-1] = data_buffers[channel][1:]
                data_buffers[channel][-1] = voltage
                if checkboxes[channel].isChecked():
                    curves[channel].setData(x, data_buffers[channel])

                # Format timestamp and channel voltages for CSV
                timestamp = QtCore.QTime.currentTime().toString()
                row_data = [timestamp] + [data_buffers[i][-1] for i in range(num_channels)]
                csv_file.write(row_format.format(*row_data) + "\n")
                csv_file.flush()  # Ensure immediate writing to disk

# Timer for regular updates
timer = QtCore.QTimer()
timer.timeout.connect(process_data)
timer.start(50)

# Start the main window
main_window.show()

# Start the GUI
if __name__ == '__main__':
    QtWidgets.QApplication.instance().exec_()
"""





import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np
import csv
import os

# Serial connection setup
serial_port = 'COM5'  # Update as needed
baud_rate = 921600
ser = serial.Serial(serial_port, baud_rate)

# CSV logging setup
csv_filename = 'adc_data_log.csv'
csv_file = open(csv_filename, mode='w', newline='')  # 'w' mode overwrites the file each time
csv_writer = csv.writer(csv_file, delimiter=' ')

# Define fixed-width formatting for CSV columns
header_format = "{:<15}" + "{:<12}" * 18
row_format = "{:<15}" + "{:<12.4f}" * 18

# Write header
header = header_format.format('Timestamp', *[f'ADC Pin A{10 + i}' for i in range(18)])
csv_file.write(header + "\n")

# PyQtGraph setup
app = QtWidgets.QApplication([])

# Main window setup
main_window = QtWidgets.QWidget()
layout = QtWidgets.QHBoxLayout()
main_window.setLayout(layout)

# Plot widget for ADC voltages
plot_widget = pg.GraphicsLayoutWidget(show=True, title="Real-Time ADC Voltage Data")
plot_widget.setBackground('w')
plot = plot_widget.addPlot(title="ADC Voltages")
plot.setYRange(0, 3.3)

# Add plot widget to the main layout
layout.addWidget(plot_widget)

# Set up channels
num_channels = 18  # Number of ADC pins used
curves = []
for i in range(num_channels):
    curve = plot.plot(pen=(i, num_channels))
    curves.append(curve)

# Data buffers for smooth plotting
buffer_size = 500
data_buffers = [np.zeros(buffer_size) for _ in range(num_channels)]
x = np.linspace(-buffer_size, 0, buffer_size)

# Checkboxes for showing/hiding channels
checkbox_layout = QtWidgets.QVBoxLayout()
checkboxes = []

def create_checkbox(label, channel_index):
    cb = QtWidgets.QCheckBox(label)
    cb.setChecked(True)
    cb.stateChanged.connect(lambda: toggle_curve(channel_index, cb.isChecked()))
    checkbox_layout.addWidget(cb)
    checkboxes.append(cb)

def toggle_curve(channel_index, is_checked):
    curves[channel_index].setVisible(is_checked)

for i in range(num_channels):
    create_checkbox(f"ADC Pin A{10 + i}", i)

# Add checkboxes to the main layout in a separate widget
checkbox_widget = QtWidgets.QWidget()
checkbox_widget.setLayout(checkbox_layout)
layout.addWidget(checkbox_widget)

# Data processing function
def process_data():
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        if "ADC Pin" in line:
            parts = line.split(", ")
            channel = int(parts[0].split(" ")[2][1:]) - 10
            adc_value = int(parts[1].split(":")[1].strip())
            voltage = (adc_value / 1023.0) * 3.3
            if 0 <= channel < num_channels:
                data_buffers[channel][:-1] = data_buffers[channel][1:]
                data_buffers[channel][-1] = voltage
                if checkboxes[channel].isChecked():
                    curves[channel].setData(x, data_buffers[channel])

                # Format timestamp and channel voltages for CSV
                timestamp = QtCore.QTime.currentTime().toString()
                row_data = [timestamp] + [data_buffers[i][-1] for i in range(num_channels)]
                formatted_row = row_format.format(*row_data)
                csv_file.write(formatted_row + "\n")
                csv_file.flush()  # Ensure immediate writing to disk

# Timer for regular updates
timer = QtCore.QTimer()
timer.timeout.connect(process_data)
timer.start(50)

# Start the main window
main_window.show()

# Start the GUI
if __name__ == '__main__':
    QtWidgets.QApplication.instance().exec_()
