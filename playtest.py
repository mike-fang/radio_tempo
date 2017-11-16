import pygame
import time

pygame.mixer.init()
sound = pygame.mixer.Sound('./music/1980/1.wav')
while True:
    sound.play()
