import pygame
from time import sleep
from KY040 import KY040
import RPi.GPIO as GPIO

pygame.mixer.init()
playlist = []
for i in range(5):
	playlist.append('/home/pi/radio_tempo/music/1980/{}.wav'.format(i+1))
print(playlist[0])
#sound = pygame.mixer.Sound(playlist[0])
pygame.mixer.music.load(playlist[0])

CLOCKPIN = 5
DATAPIN = 6
SWITCHPIN = 13

def rotaryChange(direction):
	print "turned - " + str(direction)

paused = True
def toggle_play():
	global paused
	if paused:
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()
		paused = True

curr_song = 0
def change_song(dir):
	global curr_song
	global paused
	curr_song += 2 * dir - 1
	curr_song %= len(playlist)
	pygame.mixer.music.load(playlist[curr_song])
	pygame.mixer.music.play()
	paused = False

GPIO.setmode(GPIO.BCM)

ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN,
	  change_song, toggle_play)

ky040.start()

pygame.mixer.music.play()
pygame.mixer.music.pause()

try:
	while True:
	    sleep(0.1)
finally:
	ky040.stop()
	GPIO.cleanup()
