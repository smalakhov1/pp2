import pygame
import datetime
import os

# window center
CENTER_X = 400
CENTER_Y = 400

# angle fix for original hand image
BASE_HAND_ANGLE = 15

# image variables
clock_img = None
hand_img = None

# current folder
BASE_DIR = os.path.dirname(__file__)

# images folder
IMG_DIR = os.path.join(BASE_DIR, "images")


def load_images():
    global clock_img, hand_img

    # load clock background
    clock_img = pygame.image.load(
        os.path.join(IMG_DIR, "mickeyclock.jpeg")
    )

    clock_img = pygame.transform.scale(clock_img, (800, 800))

    # load hand image
    hand_img = pygame.image.load(
        os.path.join(IMG_DIR, "hand.png")).convert_alpha()

    hand_img = pygame.transform.scale(hand_img, (180, 240))


def rotate_hand(image, angle):
    # rotate image
    return pygame.transform.rotate(image, angle)


def draw_one_hand(screen, image, angle):
    # rotate hand
    rotated = rotate_hand(image, angle)

    # center hand
    rect = rotated.get_rect(center=(CENTER_X, CENTER_Y))

    # draw hand
    screen.blit(rotated, rect)


def draw_clock(screen):
    # draw background
    screen.blit(clock_img, (0, 0))

    # get current time
    now = datetime.datetime.now()

    minutes = now.minute
    seconds = now.second

    # calculate angles with fix
    minute_angle = -minutes * 6 + BASE_HAND_ANGLE
    second_angle = -seconds * 6 + BASE_HAND_ANGLE

    # draw minute hand
    draw_one_hand(screen, hand_img, minute_angle)

    # draw second hand
    left_hand = pygame.transform.flip(hand_img, True, False)
    draw_one_hand(screen, left_hand, second_angle)