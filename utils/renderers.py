# This file contains functions to render images in various states.
# There is also a dictionary associating transitions with names.

import pygame

def static(progress, display, new, old, cx, cy):
    # This renderer is used when there is no transition going on.
    # It just draws the image with no other calculations.
	display.blit(new.surface, (cx - new.halfWidth, cy - new.halfHeight))

# This is the aforementioned dictionary.
transitions = {
}
