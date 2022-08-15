# This file contains functions to render images in various states.
# There is also a dictionary associating transitions with names.

import pygame

def static(progress, display, new, old):
    # This renderer is used when there is no transition going on.
    # It just draws the image with no other calculations.
    display.surface.blit(new.surface, (new.left, new.top))

def fade(progress, display, new, old):
    old.surface.set_alpha(int(255 * (1 - progress)))
    display.surface.blit(old.surface, (old.left, old.top))
    old.surface.set_alpha(255)

    new.surface.set_alpha(int(255 * progress))
    display.surface.blit(new.surface, (new.left, new.top))
    new.surface.set_alpha(255)

def fade_through_black(progress, display, new, old):
    if progress < 0.5:
        old.surface.set_alpha(int(255 * (1 - progress / 0.5)))
        display.surface.blit(old.surface, (old.left, old.top))
        old.surface.set_alpha(255)

    if progress > 0.5:
        new.surface.set_alpha(int(255 * ((progress - 0.5) / 0.5)))
        display.surface.blit(new.surface, (new.left, new.top))
        new.surface.set_alpha(255)

def fade_through_black(progress, display, new, old):
    if progress < 0.5:
        old.surface.set_alpha(int(255 * (1 - progress / 0.5)))
        display.surface.blit(old.surface, (old.left, old.top))
        old.surface.set_alpha(255)

    if progress > 0.5:
        new.surface.set_alpha(int(255 * ((progress - 0.5) / 0.5)))
        display.surface.blit(new.surface, (new.left, new.top))
        new.surface.set_alpha(255)

def move_down(progress, display, new, old):
    display.surface.blit(new.surface, (new.left, new.top + display.realHeight * (progress - 1)))
    display.surface.blit(old.surface, (old.left, old.top + display.realHeight * progress))

def move_up(progress, display, new, old):
    display.surface.blit(new.surface, (new.left, new.top - display.realHeight * (progress - 1)))
    display.surface.blit(old.surface, (old.left, old.top - display.realHeight * progress))

def move_left(progress, display, new, old):
    display.surface.blit(new.surface, (new.left - display.realWidth * (progress - 1), new.top))
    display.surface.blit(old.surface, (old.left - display.realWidth * progress, old.top))

def move_right(progress, display, new, old):
    display.surface.blit(new.surface, (new.left + display.realWidth * (progress - 1), new.top))
    display.surface.blit(old.surface, (old.left + display.realWidth * progress, old.top))

def shrink_and_grow(progress, display, new, old):
    if progress < 0.5:
        scale = 1 - progress / 0.5
        surface = old.resize((old.width * scale, old.height * scale))
        display.surface.blit(surface, (display.halfWidth - old.halfWidth * scale, display.halfHeight - old.halfHeight * scale))
    if progress > 0.5:
        scale = (progress - 0.5) / 0.5
        surface = new.resize((new.width * scale, new.height * scale))
        display.surface.blit(surface, (display.halfWidth - new.halfWidth * scale, display.halfHeight - new.halfHeight * scale))

# This is the aforementioned dictionary.
transitions = {
    "fade": fade,
    "fade through black": fade_through_black,
    "move down": move_down,
    "move up": move_up,
    "move left": move_left,
    "move right": move_right,
    "shrink and grow": shrink_and_grow
}
