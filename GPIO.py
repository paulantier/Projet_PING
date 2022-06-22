import RPi.GPIO as GPIO
# pour les tests
#import time


def controlevitesse(n):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    sortie1 = 4
    sortie2 = 5
    if (n == 0):
        GPIO.setup(sortie1,GPIO.OUT)
        GPIO.output(sortie1,0)
        GPIO.setup(sortie2,GPIO.OUT)
        GPIO.output(sortie2,0)
    if(n==1):
        GPIO.setup(sortie1,GPIO.OUT)
        GPIO.output(sortie1,1)
        GPIO.setup(sortie2,GPIO.OUT)
        GPIO.output(sortie2,0)
    if(n==2):
        GPIO.setup(sortie1,GPIO.OUT)
        GPIO.output(sortie1,1)
        GPIO.setup(sortie2,GPIO.OUT)
        GPIO.output(sortie2,1)
        
#tests
#time.sleep(1)
#controlevitesse(1)
#time.sleep(5)
#controlevitesse(0)
#time.sleep(5)
#controlevitesse(2)
#time.sleep(5)
#controlevitesse(0)
