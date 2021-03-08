import serial
import socket

def readSerial(port, baudrate, timeout):
    """
    Reads from the port and baudrate and has a timeout

    Parameters:
        port (int)= Serial port
        baudrate (int)= Port baudrate
        timeout (int)= How long to wait
    
    Returns:
       string: Data from port
    """
    with serial.Serial(port, baudrate, timeout) as ser:
        data = ""
        data += ser.readline()
        return data

def sendSerial(port, data):
    """
    Sends data to a serial port

    Parameters:
        port (int)= Serial port

    Returns:
        nothing
    """
    with serial.Serial(port) as ser:
        ser.write(data)

def sendUDP(IP, PORT, data):
    """
    Sends data to an IP/PORT using UDP

    Parameters:
        IP (int)= IP desitination
        PORT (int)= Port desitination
        data (any)= Data to be sent

    Returns:
        nothing
    """
    sock = socket.socket(socket.AFINET, socket.SOCK_DGRAM)
    sock.sendto(data, (IP, PORT))

#  port= "/dev/..."||"COM#" baudrate= 115200 timeout= 1 
def JevoisToRio(jevoisPort, jevoisBaudrate, jevoisTimeout, rioIP, rioPort):
    """
    Sends data from Jevois to Rio, Good example of what this can do

    Parameters:
        jevoisPort (int)= Jevois serial port
        jevoisBaudrate (int)= Jevois baudrate
        jevoisTimeout (int)= Jevois timeout
        rioIP (int)= RoboRio IP
        rioPort (int)= RoboRio Port

    Returns:
        nothing
    """
    jevoisData = readSerial(jevoisPort, jevoisBaudrate, jevoisTimeout)
    sendUDP(rioIP, rioPort, jevoisData)
