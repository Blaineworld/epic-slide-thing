# This file contains functions to render images in various states.
# There is also a dictionary associating transitions with names.

import pygame

def static(progress, display, new, old):
    # This renderer is used when there is no transition going on.
    # It just draws the image with no other calculations.
    display.surface.blit(new.surface, (new.left, new.top))

def fade(progress, display, new, old):
    old.surface.set_alpha(int(255 * (1 - progress)))
    display.surface.blit(old.surface, (new.left, new.top))
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

# This is the aforementioned dictionary.
transitions = {
    "fade": fade,
    "fade through black": fade_through_black
}
