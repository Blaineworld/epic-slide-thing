import os
import utils.config as config

# Load the instance settings.
instance = config.load_settings("./Instance Settings.txt", {
    "backup video drivers": (config.parse_list, "fbcon, directfb, svgalib, xvfb, Xvfb, x11"),
    "path to remote folder": (str, "./files"),
    "status size": (config.parse_percentage, "10%"),
    "max fps": (int, "60")
})

# Load the slideshow settings.
slideshow = config.load_settings(instance["path to remote folder"] + "/Slideshow Settings.txt", {
    "time for each slide": (config.parse_duration, "0:45"),
    "randomize order": (config.parse_polar, "YES"),
    "time for each transition": (config.parse_duration, "0:00.75"),
    "possible transitions": (config.parse_list, "fade, fade through black"),
    "show slide numbers": (config.parse_polar, "YES"),
    "background color": (config.parse_color, "#000000"),
    "show status": (config.parse_polar, "YES"),
    "status color": (config.parse_color, "#FFF0E8")
})
