import pygame
import sys
from player import load_tracks, draw_ui, play_track, stop_track, next_track, prev_track

# initialize pygame
pygame.init()
pygame.mixer.init()

# window settings
WIDTH = 700
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("music player")

# font
font = pygame.font.SysFont(None, 36)

# load music
tracks = load_tracks()

# current track index
current_index = 0

# playing state
is_playing = False

# fps
clock = pygame.time.Clock()

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                play_track(tracks[current_index])
                is_playing = True

            elif event.key == pygame.K_s:
                stop_track()
                is_playing = False

            elif event.key == pygame.K_n:
                current_index = next_track(current_index, tracks)
                play_track(tracks[current_index])
                is_playing = True

            elif event.key == pygame.K_b:
                current_index = prev_track(current_index, tracks)
                play_track(tracks[current_index])
                is_playing = True

            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    draw_ui(screen, font, tracks, current_index, is_playing)

    pygame.display.flip()
    clock.tick(60)