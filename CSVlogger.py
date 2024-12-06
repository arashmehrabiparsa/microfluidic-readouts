
import serial
import struct
import time
import csv
import sys
import os

# Constants
DEFAULT_READ_SERIAL_PORT = 'COM5'
DEFAULT_CONTROL_SERIAL_PORT = 'COM5'
read_baud_rate = 115200
control_baud_rate = 9600
num_pins = 18
buffer_size = num_pins * 2  # Each pin sends 2 bytes

# Function to decode the serial data
def decode_serial_data(data):
    try:
        readings = struct.unpack('<' + 'H' * num_pins, data)
        return readings
    except struct.error as e:
        print(f"Error decoding data: {e}")
        return []

# Main function
def main():
    # Default values
    pwm = 100
    pwm_samplerate = 300
    duration = 5  # Duration in seconds
    sampleRate = 10000  # Sample rate

    # Specify full path for output CSV
    file_path = os.path.join(os.getcwd(), 'output.csv')  # Ensure full path
    print(f"CSV output path: {file_path}")

    # Get default serial ports
    read_serial_port = DEFAULT_READ_SERIAL_PORT
    control_serial_port = DEFAULT_CONTROL_SERIAL_PORT

    # Parse command-line arguments (if provided)
    if len(sys.argv) >= 2:
        read_serial_port = sys.argv[1]
    if len(sys.argv) >= 3:
        control_serial_port = sys.argv[2]
    if len(sys.argv) >= 4:
        duration = int(sys.argv[3])
    if len(sys.argv) >= 5:
        sampleRate = int(sys.argv[4])
    if len(sys.argv) >= 6:
        pwm = int(sys.argv[5])
    if len(sys.argv) >= 7:
        pwm_samplerate = int(sys.argv[6])

    # Initialize data array with headers
    arr = [['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17']]
    count = 0
    maxCount = duration * sampleRate

    # Open the CSV file for writing initially
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(arr[0])  # Write headers

    # Set the sample rate and PWM via the control serial port
    try:
        with serial.Serial(control_serial_port, control_baud_rate) as control_ser:
            control_ser.write(f"readrate {sampleRate}\r".encode('utf-8'))
            time.sleep(0.1)
            control_ser.write(f"pwm {pwm} {pwm_samplerate}\r".encode('utf-8'))
            time.sleep(0.1)
            print(f"Control serial port {control_serial_port} configured with PWM {pwm} and sample rate {sampleRate}.")
    except serial.SerialException as e:
        print(f"Error communicating with control serial port {control_serial_port}: {e}")
        return

    # Start reading data from the read serial port
    try:
        with serial.Serial(read_serial_port, read_baud_rate) as read_ser:
            read_ser.reset_input_buffer()
            read_ser.reset_output_buffer()

            while count < maxCount:
                data = read_ser.read(buffer_size)
                
                print(f"Raw data: {data}")  # Print raw data received

                if len(data) == buffer_size:
                    readings = decode_serial_data(data)
                    if readings:
                        print(f"Decoded readings: {readings}")  # Print decoded readings
                        arr.append(list(readings))
                        count += 1
                        print(f"Reading {count}/{maxCount}")

                        # Write to CSV every 10,000 readings
                        if count % 10000 == 0 or count == maxCount:
                            print(f"Writing {len(arr) - 1} rows to CSV at count {count}...")
                            with open(file_path, 'a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerows(arr[1:])  # Write new rows
                            arr = [arr[0]]  # Reset array except header
                    else:
                        print("Failed to decode data")
                else:
                    print("Incomplete data received: Buffer size mismatch")

            # Write any remaining data
            with open(file_path, 'a', newline='') as file:
                print(f"Writing remaining {len(arr) - 1} rows to CSV...")
                writer = csv.writer(file)
                writer.writerows(arr[1:])  # Write the remaining data

    except serial.SerialException as e:
        print(f"Error reading from serial port {read_serial_port}: {e}")

if __name__ == "__main__":
    main()




"""
import serial
import struct
import time
import csv
import sys

class SerialDataLogger:
    def __init__(self, read_serial_port='COM5', control_serial_port='COM5', read_baud_rate=115200, control_baud_rate=9600, num_pins=18, buffer_size=None, pwm=100, pwm_samplerate=300, duration=5, sample_rate=10000, file_path=r'C:\Users\Guest2\Personal\Github\channel-read-CNT-nanostructures\nanotech\output.csv'):
        # Initialize variables
        self.read_serial_port = read_serial_port
        self.control_serial_port = control_serial_port
        self.read_baud_rate = read_baud_rate
        self.control_baud_rate = control_baud_rate
        self.num_pins = num_pins
        self.buffer_size = buffer_size or num_pins * 2  # Each pin sends 2 bytes
        self.pwm = pwm
        self.pwm_samplerate = pwm_samplerate
        self.duration = duration
        self.sample_rate = sample_rate
        self.file_path = file_path
        self.arr = [['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17']]
        self.count = 0
        self.max_count = duration * sample_rate

    def decode_serial_data(self, data):
        try:
            readings = struct.unpack('<' + 'H' * self.num_pins, data)
            print(f"Decoded data: {readings}")  # Added for debugging
            return readings
        except struct.error as e:
            print(f"Error decoding data: {e}")
            return []

    def set_control_parameters(self):
        # Set the sample rate and PWM via the control serial port
        try:
            print(f"Opening control serial port: {self.control_serial_port}")  # Added for debugging
            with serial.Serial(self.control_serial_port, self.control_baud_rate) as control_ser:
                control_ser.write(f"readrate {self.sample_rate}\r".encode('utf-8'))
                time.sleep(0.1)
                control_ser.write(f"pwm {self.pwm} {self.pwm_samplerate}\r".encode('utf-8'))
                time.sleep(0.1)
                print(f"Control serial port {self.control_serial_port} configured with PWM {self.pwm} and sample rate {self.sample_rate}.")
        except serial.SerialException as e:
            print(f"Error communicating with control serial port {self.control_serial_port}: {e}")

    def log_data(self):
        # Start reading data from the read serial port
        try:
            print(f"Opening read serial port: {self.read_serial_port}")  # Added for debugging
            with serial.Serial(self.read_serial_port, self.read_baud_rate) as read_ser:
                read_ser.reset_input_buffer()
                read_ser.reset_output_buffer()
                print(f"Successfully opened {self.read_serial_port} for reading")  # Added for debugging

                while self.count < self.max_count:
                    print("Reading data...")  # Added for debugging
                    data = read_ser.read(self.buffer_size)
                    print(f"Received data: {data}")  # Added for debugging

                    if len(data) == self.buffer_size:
                        readings = self.decode_serial_data(data)
                        if readings:
                            self.arr.append(list(readings))
                            self.count += 1
                            print(f"Reading {self.count}/{self.max_count}")

                            # Write to CSV every 100 readings (for more frequent writing)
                            if self.count % 100 == 0:
                                print("Writing data to CSV...")  # Added for debugging
                                self.write_to_csv()
                                self.arr = [self.arr[0]]  # Reset array except header
                                print(f"Data written at count {self.count}")
                        else:
                            print("Failed to decode data")
                    else:
                        print(f"Incomplete data received: {len(data)} bytes")

                # Write any remaining data
                self.write_to_csv()

        except serial.SerialException as e:
            print(f"Error reading from serial port {self.read_serial_port}: {e}")

    def write_to_csv(self):
        # Write data to CSV file with flush
        try:
            print(f"Opening file {self.file_path} for writing...")  # Added for debugging
            with open(self.file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.arr[1:])  # Write the remaining data
                file.flush()  # Ensure immediate write to disk
            print(f"Data written to {self.file_path}")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")

    def run(self):
        # Parse command-line arguments (if provided)
        if len(sys.argv) >= 2:
            self.read_serial_port = sys.argv[1]
        if len(sys.argv) >= 3:
            self.control_serial_port = sys.argv[2]
        if len(sys.argv) >= 4:
            self.duration = int(sys.argv[3])
            self.max_count = self.duration * self.sample_rate
        if len(sys.argv) >= 5:
            self.sample_rate = int(sys.argv[4])
            self.max_count = self.duration * self.sample_rate
        if len(sys.argv) >= 6:
            self.pwm = int(sys.argv[5])
        if len(sys.argv) >= 7:
            self.pwm_samplerate = int(sys.argv[6])

        # Open the CSV file for writing headers
        try:
            print(f"Opening file {self.file_path} for header writing...")  # Added for debugging
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.arr[0])  # Write headers
            print(f"Headers written to {self.file_path}")
        except Exception as e:
            print(f"Error opening/writing to CSV file: {e}")

        # Set control parameters and start logging data
        self.set_control_parameters()
        self.log_data()


if __name__ == "__main__":
    logger = SerialDataLogger()  # Create an instance of the class
    logger.run()  # Call the run method to start logging"""