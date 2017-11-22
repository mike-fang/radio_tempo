import pygame
import os, time
from pygame.mixer import music

CWD = os.getcwd()
MUSIC_DIR = os.path.join(CWD, 'music')
YEAR_DIRS = [os.path.join(MUSIC_DIR, f) for f in os.listdir(MUSIC_DIR) if not f.startswith(',')]
YEAR_DIRS.sort()

def get_songs_from_year(y):
	return [os.path.join(y, f) for f in os.listdir(y) if not f.startswith('.')]

class MusicPlayer(object):
	def __init__(self, playlist, start_paused = False):
		self.new_playlist(playlist)

		pygame.init()
		pygame.mixer.init()
		pygame.display.init()

		music.load(playlist[self.play_pos])
		music.set_endevent(pygame.USEREVENT)
		music.play()
		
		self.paused = start_paused

		if self.paused:
			music.pause()

	def new_playlist(self, pl):
		self.play_pos = 0
		self.num_songs = len(pl)
		self.playlist = pl


	def toggle_pause(self):
		if self.paused:
			music.unpause()
		else:
			music.pause()
		self.paused = not self.paused

	def change_song(self, dir):
		#1 next song, 0 previous song
		self.play_pos += 2 * dir - 1
		self.play_pos %= self.num_songs
		music.load(self.playlist[self.play_pos])
		music.play()
		paused = False
	
		
		


if __name__ == '__main__':
	current_year = YEAR_DIRS[0]

	playlist = get_songs_from_year(current_year)
	playlist.sort()

	CLOCKPIN = 5
	DATAPIN = 6
	SWITCHPIN = 13

	player = MusicPlayer(playlist)

	playing = True
	while playing:
		for e in pygame.event.get():
			if e.type == pygame.USEREVENT:
				player.change_song(1)

