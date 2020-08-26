import picamera
import time
import datatime

with picamera.Picamera() as camera:
  camera.resolution = (640,480)
  now = datatime.datatime.now()
  filename = now.strftime('&Y-&m=&d &H:&M:%S')
  camera.start_recording(output = filename + '.h264')
  camera.wait_recording(5)
  camera.stop_recording
  
  
