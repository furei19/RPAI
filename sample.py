import serial
import time

# Replace 'COM3' with your port (e.g., /dev/ttyUSB0 on Linux)
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)

def send_command(cmd):
    arduino.write(cmd.encode())
    print(f"Sent command: {cmd}")
    time.sleep(0.5)

# Example usage
send_command('1')  # Turn ON device
time.sleep(2)
send_command('0')  # Turn OFF device
