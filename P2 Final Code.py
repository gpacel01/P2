# This python code is to be uploaded onto the Raspberry Pi PICO, ultimately turning it into a state machine.

# In State One, the PICO must be blinking its LED once per second, supplying instructions via morse code through GP2 for the detective to supply 5V
# to GP5, and then reading for 5V supplied at the GP5 pin.

# In State Two, the PICO must be blinking its LED twice every 0.8 seconds, supplying instructions via morse code through GP7 for the detective to
# supply 5V at the GP9 pin, and then reading for 5V supplied at the GP9 pin.

# In State Three, the PICO must be blinking its LED thrice per 0.6 seconds, supplying instructions via morse code through GP12 for the detective to
# supply 5V at the GP13 pin, and then reading for 5V supplied at the GP13 pin.

# In State Solved, the PICO must be blinking its LED rapidly and continuously, sending a message out its USB port at 115200 bps that says,
# “PUZZLE SOLVED! Secret key: 7529EA5ED01F07301C6A96C2E436F2CF550D3B9A542413D7A6C921D89D376528."


# import necessary libraries
from machine import pin
import RPi.GPIO as GPIO
import utime
import serial


# the pin connected to the on-board LED   
led = Pin(25, Pin.OUT)

# identify GPIO pins as input or output
GPIO.setup(2, GPIO.OUT)
GPIO.setup(5, GPIO.IN) # default is pull down, don't need to set 
GPIO.setup(7, GPIO.OUT)
GPIO.setup(9, GPIO.IN) # default is pull down, don't need to set 
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.IN) # default is pull down, don't need to set 


# creating an array called messageOne which says "5V at GP5" when translated from binary to morse code
messageOne = [0,0,1,1,0,1,0,1,0,1,1,1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,1]

# creating an array called messageTwo which says "5V at GP9" when translated from binary to morse code
messageTwo = [0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1,0,1,0,1,0,0,0,0,0,0,1,1,1,0,0,1]

# creating an arraay called messageThree which says "5V at GP13" when translated from binary to morse code
messageThree = [0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,1,0,0,1,1]

# initialize a rate of morse code message delivery (in milliseconds) 
messageRate = 1 # equal to 1 kHz

# initializing the state
state = STATE_ONE

# start counting the time for both the LED to function and message to be delivered
ledStartTime = utime.ticks_ms()
messageStartTime = utime.ticks_ms()

# start next state with LED on, should only stay on for 0.1 seconds
led.value(1) 

# STATE ONE LOOP
while(state = STATE_ONE):
    
    # initialize/reset the counter each time through the loop
    i = 0
    
    while (i <= len(messageOne)):
        
        # start counting the time since this loop starts
        nowTime = utime.ticks_ms()
        
        # determine how much time has passed without a message being sent
        messagePassedTime = nowTime - messageStartTime
        
        # send one byte of messageOne
        if messagePassedTime > messageRate # message should be delivered at 1 kHz
            GPIO.output(2, messageOne[i]) # send morse code through GP2 with the message "5V at GP5"; the 1s and 0s in morse will either output 5V or 0V, respectively
            messageStartTime = utime.ticks_ms() # reset messageStartTime
            i = i + 1 # add one to continue indexing through messageOne
        
        # determine how much time has passed without the LED being turned on
        ledPassedTime = nowTime - ledStartTime
        
        # flash LED according to State One LED pattern
        if ledPassedTime > 1000 
            ledStartTime = utime.ticks_ms() # reset ledStartTime
            led.value(1) # turn LED on after 1 full second has surpassed
        elif ledPassedTime > 100
            led.value(0) # turn LED off for 0.9 seconds
    
        # advance to State Two if 5V detected at GP5 pin         
        if (GPIO.input(5) == GPIO.HIGH):
            state = STATE_TWO
            

# start counting the time for both the LED to function and message to be delivered
ledStartTime = utime.ticks_ms()
messageStartTime = utime.ticks_ms()

# start next state with LED on, should only stay on for 0.1 seconds
led.value(1) 

# STATE TWO LOOP
while(state = STATE_TWO):
    
    # initialize/reset the counter each time through the loop
    j = 0
    
    while (j <= len(messageTwo)):
        
        # start counting the time since this loop starts
        nowTime = utime.ticks_ms()
        
        # determine how much time has passed without a message being sent
        messagePassedTime = nowTime - messageStartTime
        
        # send one byte of messageOne
        if messagePassedTime > messageRate # message should be delivered at 1 kHz
            GPIO.output(7, messageTwo[j]) # send morse code through GP2 with the message "5V at GP5"; the 1s and 0s in morse will either output 5V or 0V, respectively
            messageStartTime = utime.ticks_ms() # reset messageStartTime
            j = j + 1 # add one to continue indexing through messageOne
        
        # determine how much time has passed without the LED being turned on
        ledPassedTime = nowTime - ledStartTime
        
        # flash LED according to State Two LED pattern
        if ledPassedTime > 1000 
            ledStartTime = utime.ticks_ms() # reset ledStartTime
            led.value(1) # turn LED on
        elif ledPassedTime > 300
            led.value(0) # turn LED off
        elif ledPassedTime > 200
            led.value(1) # turn LED on
        elif ledPassedTime > 100
            led.value(0) # turn LED off
             
        # advance to State Three if 5V detected at GP9 pin         
        if (GPIO.input(9) == GPIO.HIGH):
            state = STATE_THREE

# start counting the time for both the LED to function and message to be delivered
ledStartTime = utime.ticks_ms()
messageStartTime = utime.ticks_ms()

# start next state with LED on, should only stay on for 0.1 seconds
led.value(1) 

# STATE THREE LOOP
while(state = STATE_THREE):
    
    # initialize/reset the counter each time through the loop
    k = 0
    
    while (k <= len(messageThree)):
        
        # start counting the time since this loop starts
        nowTime = utime.ticks_ms()
        
        # determine how much time has passed without a message being sent
        messagePassedTime = nowTime - messageStartTime
        
        # send one byte of messageOne
        if messagePassedTime > messageRate # message should be delivered at 1 kHz
            GPIO.output(12, messageThree[k]) # send morse code through GP2 with the message "5V at GP5"; the 1s and 0s in morse will either output 5V or 0V, respectively
            messageStartTime = utime.ticks_ms() # reset messageStartTime
            k = k + 1 # add one to continue indexing through messageOne
        
        # determine how much time has passed without the LED being turned on
        ledPassedTime = nowTime - ledStartTime
        
        # flash LED according to State Three LED pattern
        if ledPassedTime > 1000 
            ledStartTime = utime.ticks_ms() # reset ledStartTime
            led.value(1) # turn LED on
        elif ledPassedTime > 500
            led.value(0) # turn LED off
        elif ledPassedTime > 400
            led.value(1) # turn LED on
        elif ledPassedTimee > 300
            led.value(0) # turn LED off
        elif ledPassedTime > 200
            led.value(1) # turn LED on
        elif ledPassedTime > 100
            led.value(0) # turn LED off
             
        # advance to State Solved if 5V detected at GP13 pin         
        if (GPIO.input(13) == GPIO.HIGH):
            state = STATE_SOLVED


# send a message out USB port at 115200 bps. This is done before the STATE SOLVED LOOP so that it only happens once
ser = serial.Serial('/dev/ttyUSB0',115200) # open serial port
ser.write = ('PUZZLE SOLVED! Secret key: 7529EA5ED01F07301C6A96C2E436F2CF550D3B9A542413D7A6C921D89D376528') # (hash says "Sko'bos")
ser.close() # close port

# start counting the time for LED to function
ledStartTime = utime.ticks_ms()

# start next state with LED on, should only stay on for 0.1 seconds
led.value(1) 

# STATE SOLVED LOOP
while(state = STATE_SOLVED)
    
    # start counting the time since this loop starts
    nowTime = utime.ticks_ms()
    
    # determine how much time has passed without the LED being turned on
    ledPassedTime = nowTime - ledStartTime
        
    # tell the on-board LED to assume the State Solved blinking pattern
    if ledPassedTime > 200
        led.value(1) # turn LED on
        ledStartTime = utime.ticks_ms()
    elif ledPassedTime > 100
        led.value(0) # turn LED off
