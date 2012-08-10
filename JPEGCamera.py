import serial
import struct
import time

#Commands for the LinkSprite Serial JPEG Camera
GET_SIZE = struct.pack("BBBBB",0x56, 0x00, 0x34, 0x01, 0x00)
QUICK_SERIAL = struct.pack("BBBBBBB", 0x56 ,0x00 ,0x24 ,0x03 ,0x01 ,0x0D ,0xA6)
RESET_CAMERA = struct.pack("BBBB",0x56, 0x00, 0x26, 0x00)
TAKE_PICTURE = struct.pack("BBBBB",0x56, 0x00, 0x36, 0x01, 0x00)
STOP_TAKING_PICS = struct.pack("BBBBB",0x56, 0x00, 0x36, 0x01, 0x03)

baudRates = {
    9600: struct.pack("BBBBBBB", 0x56 ,0x00 ,0x24 ,0x03 ,0x01 ,0xAE ,0xC8),
    19200: struct.pack("BBBBBBB", 0x56 ,0x00 ,0x24 ,0x03 ,0x01 ,0x56 ,0xE4),
    38400: struct.pack("BBBBBBB", 0x56 ,0x00 ,0x24 ,0x03 ,0x01 ,0x2A ,0xF2),
    57600: struct.pack("BBBBBBB", 0x56 ,0x00 ,0x24 ,0x03 ,0x01 ,0x1C ,0x4C),
    115200: struct.pack("BBBBBBB", 0x56 ,0x00 ,0x24 ,0x03 ,0x01 ,0x0D ,0xA6)
}

resolutions = {
    "640x480": struct.pack("BBBBB",0X56 ,0X00 ,0X54 ,0X01 ,0X00), 
    "320x240": struct.pack("BBBBB",0X56 ,0X00 ,0X54 ,0X01 ,0X11),
    "160x120": struct.pack("BBBBB",0X56 ,0X00 ,0X54 ,0X01 ,0X22)
}

class JPEGCamera:
	
	def __init__(self, port, baudRate = 38400):
	  self.port = port
	  self.baudRate = baudRate
	  self.ser = serial.Serial(self.port, self.baudRate)
	
	def setBaudRate(self, baudRate):
	  if baudRate in baudRates:
	    self.baudRate = baudRate
	    self.ser.write(baudRates[baudRate])
	    self.ser.read(5)
	    self.ser.close()
	    self.ser = serial.Serial(self.port, self.baudRate)
	  else:
	    raise Exception('Value ' + baudRate + ' is not a valid baudrate')
	
	
	def setResolution(self, resolution):
	  if resolution in resolutions:
	    self.ser.write(resolutions[resolution])
	  else:
	    raise Exception('Value ' + resolution + ' is not a valid resolution')
	  
	def resetCamera(self):
	  self.ser.write(RESET_CAMERA)
	  self.ser.read(4)
	  self.ser.close()
	  #Wait until the camera is ready
	  time.sleep(2)
	  #Reconnect using the default baudrate
	  self.ser = serial.Serial(self.port, 38400)
	  
	def getSize(self):
	  data = self._getSize()
	  size = data[7] * 256 + data[8]
	  return size
	
	def _getSize(self):
	  self.ser.write(GET_SIZE)
	  data = struct.unpack("BBBBBBBBB",self.ser.read(9))
	  return data

	def takePicture(self):
	  self.ser.write(TAKE_PICTURE)
	  self.ser.read(5)
	  
	  
	def savePicture(self, filename):
	  dataSize = self._getSize()
	  self.ser.write(struct.pack("BBBBBBBBBBBBBBBB",0x56 ,0x00 ,0x32 ,0x0C ,0x00 ,0x0A ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,dataSize[7] ,dataSize[8] ,0x00 ,0x0A))
	  self.ser.read(5)
	  f = open(filename, 'wb')
	  image = self.ser.read(dataSize[7] * 256 + dataSize[8])
	  f.write(image)
	  f.close()
	
	def stopTakingPictures(self):
	  self.ser.write(STOP_TAKING_PICS)
	  self.ser.read(5)
	
	def close(self):
	  self.ser.close
	  
	def simpleTakePhoto(self, filename):
	  self.takePicture()
	  self.savePicture(filename)
	  self.stopTakingPictures()
	  