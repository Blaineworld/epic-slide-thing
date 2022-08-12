import pygame, os, sys, time

# Welcome message.
print("\n(Press [Escape] to stop the slideshow.)\n")

import utils.log as log
import utils.settings as settings
import utils.renderers as renderers

try:
    # Try to initialize the display without setting a video driver.
    pygame.display.init()
    log.out("Used the default video driver.", log.C_INFO)
except pygame.error:
    # Try to use one of the backup video drivers.

    found = False

    for driver in settings.instance["backup video drivers"]:
        os.putenv("SDL_VIDEODRIVER", driver)
        try:
            pygame.display.init()
            found = True
            log.out("Used the video driver `" + driver + "`.", log.C_INFO)
        except pygame.error:
            continue
        break

    if not found:
        log.out("No suitable video driver was found!\nTry adding more names to `backup video drivers`\nin the `Instance Settings.txt` file.", log.C_CRITICAL)
        sys.exit()

    del found

# Initialize some stuff.
pygame.init()
displayInfo = pygame.display.Info()
clock = pygame.time.Clock()
display = pygame.display.set_mode((displayInfo.current_w, displayInfo.current_h), pygame.FULLSCREEN, pygame.NOFRAME)
pygame.mouse.set_visible(False)

# Calculate sizes and positions for the screen and stuff.
statusSize = displayInfo.current_h * settings.instance["status bar size"]
picWidth = displayInfo.current_w
picHeight = displayInfo.current_h - statusSize
picCenterX = picWidth / 2
picCenterY = picHeight / 2

# This class abstracts images.
class Picture:
    def __init__(self, surface, name = "<Untitled>"):
        # Scale the surface and remember its size.
        width, height = surface.get_rect().size
        scale = min(picWidth / width, picHeight / height)
        self.height = int(height * scale)
        self.width = int(width * scale)

        # Store the actual surface.
        self.surface = pygame.transform.smoothscale(surface, (self.width, self.height))

        # These are for calculating the edge positions.
        self.halfHeight = self.height / 2
        self.halfWidth = self.width / 2

        # Store even more miscellaneous data.
        self.name = name

# Load the images.
folder = settings.instance["path to remote folder"] + "/Images"
names = os.listdir(folder)
pictures = []
for name in names:
    try:
        pictures.append(Picture(pygame.image.load(folder + "/" + name), name))
    except (pygame.error, ValueError):
        log.out("The image `" + name + "`\nfailed to load.", log.C_ISSUE)
del names
del folder

if len(pictures) == 0:
    log.out("No images could be loaded!", log.C_ISSUE | log.C_CRITICAL)
    pygame.quit()
    sys.exit()

log.out("Loaded " + str(len(pictures)) + " images.", log.C_INFO)

# Stuff for rendering.
index = 0
renderer = renderers.static

# "Game" loop.
running = True
while running:
    # Events, mostly keyboard shortcuts.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            log.out("Quit via a quit event.", log.C_INFO)
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            log.out("Quit via the Escape key.", log.C_INFO)
            running = False
            pygame.quit()
            sys.exit()

    # Render the picture.
    display.fill(settings.slideshow["background color"])
    renderer(0.5, display, pictures[index], pictures[index - 1], picCenterX, picCenterY)

    # Update the display.
    pygame.display.update()

    # Tick.
    clock.tick(60)
