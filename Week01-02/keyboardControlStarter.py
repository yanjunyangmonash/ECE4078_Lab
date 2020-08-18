# teleoperate the robot through keyboard control
# getting-started code

from pynput.keyboard import Key, Listener, KeyCode
import cv2
import numpy as np

class Keyboard:
    # feel free to change the speed, or add keys to do so
    wheel_vel_forward = 100
    wheel_vel_rotation = 20
    pressed = False

    def __init__(self, ppi=None):
        # storage for key presses
        self.directions = [False for _ in range(4)]
        self.signal_stop = False 

        # connection to PenguinPi robot
        self.ppi = ppi
        self.wheel_vels = [0, 0]
        self.last_input = 'No Input'
        
        #with Listener(on_press=self.on_press,on_release=self.on_release) as self.listener:
            #self.listener.join()

        self.listener = Listener(on_press=self.on_press,on_release=self.on_release).start()

    def on_press(self, key):
        if not self.pressed:
            print('{0} pressed'.format(key))
            self.pressed = True
            
        # use arrow keys to drive, space key to stop
        # feel free to add more keys
        if key == Key.up:
            self.directions[0] = True
            self.last_input = '^'
        elif key == Key.down:
            self.directions[1] = True
            self.last_input = 'V'
        elif key == Key.left:
            self.directions[2] = True
            self.last_input = '<'
        elif key == Key.right:
            self.directions[3] = True
            self.last_input = '>'
        elif key == Key.space:
            self.signal_stop = True
            self.last_input = 'Stop'

        self.send_drive_signal()
        
    def on_release(self, key):
        if key == Key.up:
            print('{0} released'.format(key))
            self.signal_stop = True
            self.directions[0] = False
            self.pressed = False
            
        elif key == Key.down:
            self.signal_stop = True
            self.directions[1] = False
            
        elif key == Key.left:
            self.signal_stop = True
            self.directions[2] = False
            
        elif key == Key.space:
            self.signal_stop = True
            self.directions[3] = False
                
        self.last_input = 'Stop'    
        self.send_drive_signal()
        
    def get_drive_signal(self):           
        # translate the key presses into drive signals 
        
        # compute drive_forward and drive_rotate using wheel_vel_forward and wheel_vel_rotation
        # drive_forward = ???
        # drive_rotate = ???
        

        # translate drive_forward and drive_rotate into left_speed and right_speed
        # left_speed = ???
        # right_speed = ???
        
        #My Solution
        if self.signal_stop:
            left_speed = right_speed = 0
            self.signal_stop = False
        else:
            if self.directions[0]:
                left_speed = right_speed = self.wheel_vel_forward
                #self.directions[0] = False
            elif self.directions[1]:
                left_speed = right_speed = -self.wheel_vel_forward
                #self.directions[1] = False
            elif self.directions[2]:
                left_speed = self.wheel_vel_rotation
                right_speed = self.wheel_vel_forward
                #self.directions[2] = False
            elif self.directions[3]:
                right_speed = self.wheel_vel_rotation
                left_speed = self.wheel_vel_forward
                #self.directions[3] = False
        '''
        if (self.signal_stop):
            self.directions = [False for _ in range(4)]
            self.signal_stop = False
        
        if (self.directions[0] and self.directions[1]):
            self.directions[0] = False
            self.directions[1] = False
        
        if (self.directions[2] and self.directions[3]):
            self.directions[2] = False
            self.directions[3] = False
            
        drive_forward = (self.directions[0] - self.directions[1]) * self.wheel_vel_forward
        drive_rotate = (self.directions[2] - self.directions[3]) * self.wheel_vel_rotation

        left_speed = drive_forward - drive_rotate
        right_speed = drive_forward + drive_rotate
        '''



        return left_speed, right_speed
    
    def send_drive_signal(self):
        if not self.ppi is None:
            lv, rv = self.get_drive_signal()
            lv, rv = self.ppi.set_velocity(lv, rv)
            self.wheel_vels = [lv, rv]
            
    def latest_drive_signal(self):
        return self.wheel_vels
    

if __name__ == "__main__":
    #import penguinPiC
    #ppi = penguinPiC.PenguinPi()
    from PenguinPiC import PenguinPi
    ppi = PenguinPi()
    

    keyboard_control = Keyboard(ppi)

    cv2.namedWindow('video', cv2.WINDOW_NORMAL);
    cv2.setWindowProperty('video', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE);

    while True:
        # font display options
        font = cv2.FONT_HERSHEY_SIMPLEX
        location = (0, 0)
        font_scale = 1
        font_col = (255, 255, 255)
        line_type = 2

        # get velocity of each wheel
        wheel_vels = keyboard_control.latest_drive_signal();
        L_Wvel = wheel_vels[0]
        R_Wvel = wheel_vels[1]

        # get current camera frame
        curr = ppi.get_image()

        # scale to 144p
        # feel free to change the resolution
        resized = cv2.resize(curr, (960, 720), interpolation = cv2.INTER_AREA)

        # feel free to add more GUI texts
        cv2.putText(resized, 'PenguinPi', (15, 50), font, font_scale, font_col, line_type)
        cv2.putText(resized, 'INPUT: ' + keyboard_control.last_input, (15, 700), font, font_scale, (255, 255, 0), line_type)

        cv2.imshow('video', resized)
        cv2.waitKey(1)

        continue
