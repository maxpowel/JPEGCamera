==================================
LS - Y201 Jpeg Serial Camera
==================================

As you can see is written in python. Requires struct and serial packages.
I built this library to be used with beaglebone. If you are also using
this camera under beaglebone you will need to enable serial ports (check [BeagleBoneTools](https://github.com/maxpowel/BeagleBone-Tools) )

Methods
=========

* **JPEGSerial(serialPort, baudRate = 38400)**
  Constructor: 
  Serial port, for example /dev/ttyO1.
  You can specify the baudrate but 38400 is the default value. If you have already initilizated the camera and changed the baudrate, you can specify this baudrate
  
* **simpleTakePhoto(filename)**
  Just provide a filename and all process will be automatically done (takePicture, savePicture and stopTakingPictures)

* **setBaudRate(baudRate)**
  Baudrates allowed are: 9600, 19200, 38400, 57600, 115200.
  The library automatically close and open a new connection with the new baudRate

* **setResolution(resolution)**
  Allowed resolutions are: 640x480, 320x240 and 160x120
  Example of use: camera.setResolution("640x480")

* **resetCamera**
  Reset the camera. A new connection with the default baudRate is opened after reset

* **getSize**
  Get the size in bytes of the image stored in the camera

* **takePicture**
  Take a picture and storage it in the camera
  
* **savePicture**  
  Save the picture from the camera to a local file
  
* **stopTakingPictures**
  Once you saved the picture, set the camera ready to get take next picture

* **close**
  Close connection with the camera
  

Note
===========
The camera works at 5V or 3.3V, but I you connect VCC to 5V dont use a 3.3V serial connection

[Resolution Issue](http://www.linksprite.com/faq/shownews.php?lang=en&id=83)
[Datasheet](http://www.sparkfun.com/datasheets/Sensors/Imaging/1274419957.pdf)
[Reference page](https://www.sparkfun.com/products/10061)
