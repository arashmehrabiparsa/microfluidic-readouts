import serial
import serial.tools.list_ports
import time
import logging
from typing import Optional, Union
from contextlib import contextmanager

class TeensySerialHandler:
    def __init__(self, baud_rate: int = 921600, vendor_id: int = 0x16C0, product_id: int = 0x0483):
        """
        Initialize Teensy serial connection handler
        
        Args:
            baud_rate: Serial baud rate (default 921600 for Teensy 4.1)
            vendor_id: Teensy USB vendor ID (default 0x16C0)
            product_id: Teensy USB product ID (default 0x0483)
        """
        self.baud_rate = baud_rate
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.port = None
        self.serial = None
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging"""
        logger = logging.getLogger("TeensySerial")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger

    def find_teensy_port(self) -> Optional[str]:
        """Find the Teensy device port"""
        for port in serial.tools.list_ports.comports():
            if (hasattr(port, 'vid') and hasattr(port, 'pid') and 
                port.vid == self.vendor_id and port.pid == self.product_id):
                return port.device
        return None

    def connect(self, max_attempts: int = 5) -> bool:
        """
        Connect to Teensy with retry mechanism
        
        Args:
            max_attempts: Maximum number of connection attempts
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        attempt = 0
        while attempt < max_attempts:
            try:
                self.port = self.find_teensy_port()
                if not self.port:
                    raise serial.SerialException("Teensy device not found")
                
                # Close port if it's already open
                if self.serial and self.serial.is_open:
                    self.serial.close()
                
                self.serial = serial.Serial(
                    port=self.port,
                    baudrate=self.baud_rate,
                    timeout=1,
                    write_timeout=1
                )
                
                # Clear any stale data
                self.serial.reset_input_buffer()
                self.serial.reset_output_buffer()
                
                self.logger.info(f"Successfully connected to Teensy on {self.port}")
                return True
                
            except serial.SerialException as e:
                self.logger.warning(f"Connection attempt {attempt + 1} failed: {str(e)}")
                attempt += 1
                time.sleep(2)  # Wait before retry
                
            except Exception as e:
                self.logger.error(f"Unexpected error during connection: {str(e)}")
                attempt += 1
                time.sleep(2)
                
        self.logger.error("Failed to connect after maximum attempts")
        return False

    def disconnect(self):
        """Safely disconnect from Teensy"""
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()
                self.logger.info("Disconnected from Teensy")
        except Exception as e:
            self.logger.error(f"Error during disconnect: {str(e)}")

    def read_line(self) -> Optional[str]:
        """
        Read a line from Teensy with error handling
        
        Returns:
            str: Decoded line or None if error
        """
        try:
            if not self.serial or not self.serial.is_open:
                raise serial.SerialException("Serial port not open")
                
            if self.serial.in_waiting:
                return self.serial.readline().decode('utf-8').strip()
            return None
            
        except serial.SerialException as e:
            self.logger.error(f"Serial read error: {str(e)}")
            self.connect()  # Attempt to reconnect
            return None
            
        except Exception as e:
            self.logger.error(f"Unexpected error during read: {str(e)}")
            return None

    @contextmanager
    def auto_connect(self):
        """Context manager for automatic connection handling"""
        try:
            if self.connect():
                yield self
            else:
                raise serial.SerialException("Failed to connect to Teensy")
        finally:
            self.disconnect()

    def is_connected(self) -> bool:
        """Check if connection is active"""
        return self.serial is not None and self.serial.is_open

    def clear_buffers(self):
        """Clear input and output buffers"""
        if self.is_connected():
            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()

# Example usage:
if __name__ == "__main__":
    handler = TeensySerialHandler()
    
    # Using context manager
    with handler.auto_connect() as teensy:
        if teensy.is_connected():
            for _ in range(10):
                data = teensy.read_line()
                if data:
                    print(f"Received: {data}")
                time.sleep(0.1)