from picamera import PiCamera
from time import sleep
from gpiozero import Button
import signal
import sys
import RPi.GPIO as GPIO

# initial setting
BUTTON_GPIO = 21
SAVE_LOCATION = "Desktop/"
MAX_VIDEO = 10;
VIDEO_TIME = 5 #unit : second

# Checking variables
global Button_check
Button_check = False;
video_count = 1;
video_check_array = [0 for i in range(MAX_VIDEO + 5)]

#exiting program by pressing ctrl+C 
def signal_handler(sig,frame) :
    camera.stop_preview()
    print("video to save : ")
    for i in range(1, MAX_VIDEO) :
        if(video_check_array[i] == 1) :
            print(i)
    
    GPIO.cleanup()
    sys.exit()
    
def button_pressed_callback(channel) :
    print("button has pressed")
    global Button_check
    Button_check = True;
    
def Prev_video_count_num(cnt) : #regardless it is occupied
    cnt -= 1
    if(cnt <= 0) :
        cnt += MAX_VIDEO
    return cnt

def Next_video_count_num(cnt) : #regardless it is occupied
    cnt +=1
    if(cnt>MAX_VIDEO):
        cnt %= MAX_VIDEO
    return cnt

def Next_video_count_occupy(cnt) : #regard it is occupied
    cnt = Next_video_count_num(cnt)
    while(video_check_array[cnt] == True) :
        cnt = Next_video_count_num(cnt)
    return cnt
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING,
                      callback = button_pressed_callback, bouncetime=100)

with PiCamera() as camera :
    camera.rotation = 180;
    camera.resolution = (640, 480)
    
    try:
        while True :
            Button_check = False;
            camera.start_preview()
            camera.start_recording(str(video_count) + '.h264')
            camera.wait_recording(5)
            camera.stop_recording()
            print(Button_check)
            print(type(video_count))
            video_count = Next_video_count_occupy(video_count)
        
            if(Button_check == True) :
                video_check_array[video_count] = 1;
                video_check_array[Next_video_count_occupy(video_count)] = 1;
            
    except KeyboardInterrupt:
        camera.stop_preview()
        print("video to save : ")
        for i in range(1, MAX_VIDEO) :
            if(video_check_array[i] == 1) :
                print(i)
                
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()



"""

#the maximum number that we can save videos
maximum_video = 10; 

button = Button(21)

def button_pressed_if() :
    print("button has pressed")

button_when_pressed = button_pressed_if 

button.wait_for_press()
button_pressed_if()
pause()


    
    camera.start_preview()
    
    #
    pause()
    camera.capture('test.jpg')
    camera.stop_preview()


"""