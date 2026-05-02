import pygame

from config import (
    text_color,
    muted_text_color,
    overlay_color,
    window_width,
    window_height,
)


def draw_hud(surface, font, small_font, score, level):
    # draw score and level in the top left corner
    score_text = font.render(f"score: {score}", True, text_color)
    level_text = font.render(f"level: {level}", True, text_color)
    info_text = small_font.render("arrows to move, r to restart", True, muted_text_color)

    surface.blit(score_text, (16, 12))
    surface.blit(level_text, (16, 42))
    surface.blit(info_text, (16, 74))


def draw_center_message(surface, title_font, body_font, title, body):
    # draw a centered overlay for game over or victory
    overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    overlay.fill(overlay_color)
    surface.blit(overlay, (0, 0))

    title_surface = title_font.render(title, True, text_color)
    body_surface = body_font.render(body, True, muted_text_color)

    title_rect = title_surface.get_rect(center=(window_width // 2, window_height // 2 - 18))
    body_rect = body_surface.get_rect(center=(window_width // 2, window_height // 2 + 24))

    surface.blit(title_surface, title_rect)
    surface.blit(body_surface, body_rect)