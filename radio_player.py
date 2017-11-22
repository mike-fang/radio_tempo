import pygame
import os, time, sys
import random
from pygame.mixer import music

from KY040 import KY040
import RPi.GPIO as GPIO


CWD = os.getcwd()
MUSIC_DIR = os.path.join(CWD, 'music')
YEAR_DIRS = [os.path.join(MUSIC_DIR, f) for f in os.listdir(MUSIC_DIR) if not f.startswith(',')]
YEAR_DIRS.sort()

def shutdown():
	command = '/usr/bin/sudo /sbin/shutdown now'
	import subprocess
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]
	print output
	

class MusicPlayer(object):
	def __init__(self, channel_dir, start_playing = True):
		self.playing = False

		self.chan_dir = channel_dir
		self.num_chans = len(channel_dir)
		self.chan_num = 0
		self.load_playlist(0)

		pygame.init()
		pygame.mixer.init()
		pygame.display.init()

		music.set_endevent(pygame.USEREVENT)
		if start_playing:
			self.start_pl() 

	def start_pl(self):
		self.paused = False
		music.load(self.playlist[self.play_pos])
		music.play()
		self.playing = True


	def get_pl(self, dir):
		return [os.path.join(dir, f) for f in os.listdir(dir) if not f.startswith('.')]

	def load_playlist(self, chan_num, shuffle=True):

		pl = self.get_pl(self.chan_dir[chan_num])
		pl.sort()
		if shuffle:
			random.shuffle(pl)

		self.play_pos = 0
		self.num_songs = len(pl)
		self.playlist = pl


	def toggle_pause(self):
		if not self.playing:
			self.start_pl()
		else:
			if self.paused:
				music.unpause()
			else:
				music.pause()
			self.paused = not self.paused

	def change_song(self, dir):
		#1 next song, 0 previous song
		self.play_pos += 2 * dir - 1
		self.play_pos %= self.num_songs
		self.start_pl()
		paused = False
	
	def change_chan(self, dir):
		#1 next, 0 previous chan
		self.chan_num += 2 * dir - 1
		self.chan_num %= self.num_chans

		self.load_playlist(self.chan_num)
		self.start_pl()
		paused = False
		


if __name__ == '__main__':
	current_year = YEAR_DIRS[0]

	#playlist = get_songs_from_year(current_year)
	#playlist.sort()

	CLOCKPIN = 5
	DATAPIN = 6
	SWITCHPIN = 13



	player = MusicPlayer(YEAR_DIRS)

	prev_press = 0
	def button_press():
		global prev_press
		if time.time() - prev_press > 1.0:
			player.toggle_pause()
		else:
			shutdown()
		prev_press = time.time()

	GPIO.setmode(GPIO.BCM)
	ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN,
		  player.change_chan, button_press)
	ky040.start()



	try:
		while True:
			for e in pygame.event.get():
				if e.type == pygame.USEREVENT:
					player.change_song(1)
	finally:
		ky040.stop()
		GPIO.cleanup()
