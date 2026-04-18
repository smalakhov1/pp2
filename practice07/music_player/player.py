import pygame
import os

BASE_DIR = os.path.dirname(__file__)
MUSIC_DIR = os.path.join(BASE_DIR, "music")


def load_tracks():
    tracks = []

    for file in os.listdir(MUSIC_DIR):
        if file.endswith(".mp3") or file.endswith(".wav"):
            tracks.append(os.path.join(MUSIC_DIR, file))

    return tracks


def play_track(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()


def stop_track():
    pygame.mixer.music.stop()


def next_track(index, tracks):
    return (index + 1) % len(tracks)


def prev_track(index, tracks):
    return (index - 1) % len(tracks)


def draw_ui(screen, font, tracks, current_index, is_playing):
    screen.fill((255, 255, 255))

    # title
    title = font.render("music player", True, (0, 0, 0))
    title_rect = title.get_rect(center=(350, 70))
    screen.blit(title, title_rect)

    # current track name
    if len(tracks) > 0:
        name = os.path.basename(tracks[current_index])
    else:
        name = "no tracks"

    track_text = font.render(name, True, (0, 0, 0))
    track_rect = track_text.get_rect(center=(350, 180))
    screen.blit(track_text, track_rect)

    # status
    status = "playing" if is_playing else "stopped"
    state_text = font.render(status, True, (120, 120, 120))
    state_rect = state_text.get_rect(center=(350, 240))
    screen.blit(state_text, state_rect)

    # small controls text
    small_font = pygame.font.SysFont(None, 24)

    controls = small_font.render(
        "P - play   S - stop   N - next   B - back   Q - quit",
        True,
        (80, 80, 80)
    )

    controls_rect = controls.get_rect(center=(350, 360))
    screen.blit(controls, controls_rect)