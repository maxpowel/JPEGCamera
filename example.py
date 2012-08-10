#Example script

import time
from JPEGCamera import JPEGCamera

camera = JPEGCamera("/dev/ttyO1")
camera.simpleTakePhoto("image.jpg");
camera.close()
