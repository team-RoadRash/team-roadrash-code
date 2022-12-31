# importing the reqired libraries
from machine import Pin, PWM
import time
import utime
# pin declarations
    #pins for BL Module input
xp = Pin(10, Pin.IN, Pin.PULL_DOWN)
xn = Pin(11, Pin.IN, Pin.PULL_DOWN)
yp = Pin(12, Pin.IN, Pin.PULL_DOWN)
yn = Pin(13, Pin.IN, Pin.PULL_DOWN)
sw = Pin(14, Pin.IN, Pin.PULL_DOWN)

# define pins as input
xp.init(Pin.IN, Pin.PULL_DOWN)
xn.init(Pin.IN, Pin.PULL_DOWN)
yp.init(Pin.IN, Pin.PULL_DOWN)
yn.init(Pin.IN, Pin.PULL_DOWN)
sw.init(Pin.IN, Pin.PULL_DOWN)
    # pins for motor 1
en1 = Pin(17, value = 0, mode=Pin.OUT)
in1a = Pin(20, value=0, mode=Pin.OUT)
in1b = Pin(21, value=0, mode=Pin.OUT)

    # pins for motor 2
en2 = Pin(3, value=0, mode=Pin.OUT)
in2a = Pin(6, value=0, mode=Pin.OUT)
in2b = Pin(7, value=0, mode=Pin.OUT)


# set pwm object for the two motors at 60 Hz
    # for motor 1
pwm1 = PWM(en1)
pwm1.freq(60)

    # for motor 2
pwm2 = PWM(en2)
pwm2.freq(60)

#Ultrasonic pin definitions
Ltrigger = Pin(0, Pin.OUT)
Lecho = Pin(1, Pin.IN)
Rtrigger = Pin(26,Pin.OUT)
Recho = Pin(27,Pin.IN)

#ultrasonic function definition
def ultra(trigger_ip,echo_ip):
    trigger=trigger_ip
    echo=echo_ip
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()

    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = ((timepassed * 0.0343) / 2) /29.1
    return distance

# function for motor control
def control(xduty, yduty, label):
    # parameters assigned to local variables
    xduty=xduty
    yduty=yduty
    label=label
    if yduty>0: sense = "cw"
    elif yduty<0: sense = "ccw"
    elif yduty==0: sense = "noip"
    
    if label==1:
    #function logic when there is no input in y-direction
        if sense == "noip":
            if xduty==0:
                in1a.value(0)
                in1b.value(0)
                in2a.value(0)
                in2b.value(0)
                pwm1.duty_u16(0)
                pwm2.duty_u16(0)
            elif xduty>0:
                in2a.value(1)
                in2b.value(0)
                in1a.value(0)
                in1b.value(1)
                pwm1.duty_u16(xduty//2)
                pwm2.duty_u16(xduty//2)
            elif xduty<0:
                print (xduty,yduty)
                in2a.value(0)
                in2b.value(1)
                in1a.value(1)
                in1b.value(0)
                pwm1.duty_u16(xduty//2)
                pwm2.duty_u16(xduty//2)
        # function logic when positive y-direction movement(forward)
        if sense == "cw":
            in1a.value(1)
            in1b.value(0)
            in2a.value(1)
            in2b.value(0)
            # set the speed of rotation as per x-direction input(left or right)
            if xduty==0:  
                pwm1.duty_u16(yduty)
                pwm2.duty_u16(yduty)
            elif xduty>0:
                if xduty==yduty:
                    xduty = int(xduty/2.0)
                pwm1.duty_u16(yduty//2)
                pwm2.duty_u16(yduty)
            elif xduty<0:
                if (xduty*-1)==yduty:
                    xduty = int(xduty/2.0)
                pwm1.duty_u16(yduty)
                pwm2.duty_u16(yduty+xduty)
        # function logic when negative y-direction movement(reverse)
        elif sense == "ccw":
            in1a.value(0)
            in1b.value(1)
            in2a.value(0)
            in2b.value(1)
            yduty=yduty*-1
            # set the speed of rotation as per x-direction input(left or right)
            if xduty==0:  
                pwm1.duty_u16(yduty)
                pwm2.duty_u16(yduty)
            elif xduty>0:
                pwm1.duty_u16(yduty//2)
                pwm2.duty_u16(yduty)
            elif xduty<0:
                pwm1.duty_u16(yduty)
                pwm2.duty_u16(yduty//2)
      
    if label==0:
        in1a.value(0)
        in1b.value(0)
        in2a.value(0)
        in2b.value(0)
        pwm1.duty_u16(0)
        pwm2.duty_u16(0)
        utime.sleep(2)
# assume that only valid inputs are received on the BL module .

# main logic of the program
while True:
    Rdist=ultra(Ltrigger,Lecho)
    Ldist=ultra(Rtrigger,Recho)
#     xn = float(input("Xn-input : "))
#     xp = float(input("Xp-input : "))
#     yn = float(input("Yn-input : "))
#     yp = float(input("Yp-input : "))
#     print('xn: ', xn.value(), 'xp: ', xp.value(), 'yn: ', yn.value(), 'yp: ', yp.value())
    xduty=0
    yduty=0
    label=0
    ul=0
    ur=0
    if Ldist>0.3 and Rdist>0.3:
        ul=0
        ur=0
    if Ldist<0.3 and Rdist>0.3:
        ul=1
        ur=0
    if Ldist>0.3 and Rdist<0.3:
        ul=0
        ur=1
    if Ldist<0.3 and Rdist<0.3:
        ul=1
        ur=1
    if xn.value() or xp.value()==0:
        xduty=0
        label=1
    if xn.value()==1:
        xduty=-100
        if ur==1:
            xduty=100
    if xp.value()==1:
        xduty=100
        if ul==1:
            xduty=-100
    if yp.value() or yn.value()==0:
        yduty=0
        label=1
    if yp.value()==1:
        yduty=100
    if yn.value()==1:
        yduty=-100
    if sw.value()==1:
        xduty=0
        yduty=0
        label=1
    utime.sleep(0.01)
#     # convert % speed to 0-65025 range
    xduty = int(xduty * 65025 / 100) # roundoff to int
    yduty = int(yduty * 65025 / 100)
    # call the function motor
    print(ul,ur,xduty)
    control(xduty,yduty,label)
