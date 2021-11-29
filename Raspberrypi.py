import timeimport RPi.GPIO as GPIO
import time

PIR = 3
NTC = 5
LDR = 7

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)		#choose pin no. system
GPIO.setup(PIR, GPIO.IN)	
GPIO.setup(NTC, GPIO.IN)
GPIO.setup(LDR, GPIO.IN)

#FLAGS

lights = False
hot = False

m = 3
while True:
#when motion detected turn on LED
    #if(GPIO.input(PIR)):
    #    print("MOVEMENT")
        #print("Motion detected" + str(i))
        
    ### LIGHT DETECTION ##
    if(GPIO.input(7) and not lights):
        print("LIGHTS ON")
        lights = True
    if(not GPIO.input(LDR) and lights):
        print("LIGHTS OFF")
        lights = False
    
    
    if(GPIO.input(NTC) and not hot):
        print("TOO HOT")
        hot = True
    if(not GPIO.input(NTC) and hot):
        print("NORMAL TEMPERATURE")
        hot = False
        
        
    if(GPIO.input(PIR)):
        print("MOVEMENT")
        time.sleep(1)   #Pause time in seconds
        
        
