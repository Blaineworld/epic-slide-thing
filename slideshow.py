import pygame, math, os, sys, time

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

# Calculate sizes and positions for the screen and stuff.
statusSize = 0
if settings.slideshow["show status bar"]:
    statusSize = displayInfo.current_h * settings.instance["status bar size"]
PIC_WIDTH = displayInfo.current_w
PIC_HEIGHT = displayInfo.current_h - statusSize
PIC_CENTER_X = PIC_WIDTH / 2
PIC_CENTER_Y = PIC_HEIGHT / 2

# This class abstracts images.
class Picture:
    def scale(self, size):
        # Scales the image (smoothly if possible).
        if self.bytesize > 2:
            return pygame.transform.smoothscale(self.surface, size)
        else:
            return pygame.transform.scale(self.surface, size)

    def __init__(self, surface, name = "<Untitled>", size = None):
        # Scale the surface if no forced size was specified.
        self.scale = 1.0
        self.surface = surface
        self.bytesize = surface.get_bytesize()
        if not size:
            size = surface.get_rect().size
            self.scale = min(PIC_WIDTH / size[0], PIC_HEIGHT / size[1])
            size = (size[0] * self.scale, size[1] * self.scale)
            if self.bytesize > 2:
                self.surface = pygame.transform.smoothscale(surface, size)
            else:
                self.surface = pygame.transform.scale(surface, size)

        # Store the width and height of the actual surface.
        self.realWidth, self.realHeight = surface.get_rect().size

        # Store the picture's various measurements.
        self.width, self.height = size
        self.halfWidth = self.width / 2
        self.halfHeight = self.height / 2
        self.top = PIC_CENTER_Y - self.halfHeight
        self.left = PIC_CENTER_X - self.halfWidth
        self.bottom = PIC_CENTER_Y + self.halfHeight
        self.right = PIC_CENTER_X + self.halfWidth
        self.diagonal = math.sqrt(self.width ** 2 + self.height ** 2)

        # Store the picture's name.
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

log.out("Going fullscreen.", log.C_INFO)

# Go fullscreen.
display = pygame.display.set_mode((PIC_WIDTH, PIC_HEIGHT), pygame.FULLSCREEN, pygame.NOFRAME)
pygame.mouse.set_visible(False)

# Create a special Picture for the display itself.
displayPicture = Picture(display, "<Display>", (PIC_WIDTH, PIC_HEIGHT))
displayPicture.top = 0
displayPicture.left = 0
displayPicture.bottom = PIC_HEIGHT
displayPicture.right = PIC_WIDTH

# Store render settings in variables for speed (and resiliance).
BACKGROUND_COLOR = settings.slideshow["background color"]
SLIDE_DURATION = settings.slideshow["time for each slide"] or sys.float_info.min
TRANSITION_DURATION = settings.slideshow["time for each transition"] or sys.float_info.min

# Stuff for rendering.
index = 0
renderer = renderers.static
renderStart = time.monotonic()
renderDuration = SLIDE_DURATION

def nextSlide():
    global index
    global renderer
    global renderStart
    global renderDuration
    global renderFinishHook

    index = (index + 1) % len(pictures)
    renderer = renderers.fade_through_black
    renderStart = time.monotonic()
    renderDuration = TRANSITION_DURATION
    renderFinishHook = finishTransition

def finishTransition():
    global renderer
    global renderStart
    global renderEnd
    global renderDuration
    global renderFinishHook

    renderer = renderers.static
    renderStart = time.monotonic()
    renderDuration = SLIDE_DURATION
    renderFinishHook = nextSlide
    
renderFinishHook = nextSlide

# "Game" loop.
running = True
while running:
    # Events, mostly keyboard shortcuts.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            log.out("Halted via a quit event.", log.C_INFO)
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                log.out("Halted via the Escape key.", log.C_INFO)
                running = False
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_b:
                index = (index - 1) % len(pictures)
            elif event.key == pygame.K_n:
                index = (index + 1) % len(pictures)
            elif event.key == pygame.K_m:
                renderFinishHook()

    # Calculate progress.
    progress = min(1.0, (time.monotonic() - renderStart) / renderDuration)

    # Render the picture.
    display.fill(BACKGROUND_COLOR)
    renderer(progress, displayPicture, pictures[index], pictures[index - 1])

    # Update the display.
    pygame.display.update()

    # Finish using this renderer if necessary.
    if progress == 1.0:
        renderFinishHook()

    # Tick.
    clock.tick(60)
