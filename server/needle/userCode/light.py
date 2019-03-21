import RPi.GPIO as GPIO
import time
import atexit
from random import randint
import pygame


class Light:
    color = ""
    pin = 0
    snd = None

    def __init__(self, color, pin):
        self.color = color
        self.pin = pin
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.init()
        self.snd = pygame.mixer.Sound('beep.wav')

    def on(self):
        GPIO.output(self.pin, False)
        print "AA: %s turning on" % (self.color)

    def off(self):
        GPIO.output(self.pin, True)
        print "AA: % turning off" % (self.color)

    def beep(self):
        self.snd.play()
        self.on()
        time.sleep(0.6)
        self.off()



def wait(sec):
    time.sleep(sec)
    print "AA: waiting %d seconds" % (sec)

def random(start, finish):
    return randint(start, finish)


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7, True)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, True)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, True)


def cleanup():
    #print "Exiting program..."
    GPIO.cleanup()

GPIO.setwarnings(False)

atexit.register(cleanup)

setup()

red = Light("red", 7)
yellow = Light("yellow", 11)
green = Light("green", 13)
