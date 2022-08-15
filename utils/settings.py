import os
import utils.config as config

# Load the instance settings.
instance = config.load_settings("./Instance Settings.txt", {
    "backup video drivers": (config.parse_list, "fbcon, directfb, svgalib, xvfb, Xvfb, x11"),
    "path to remote folder": (str, "./files"),
    "show debug info": (config.parse_polar, "NO"),
    "status bar size": (config.parse_percentage, "10%")
})

# Load the slideshow settings.
slideshow = config.load_settings(instance["path to remote folder"] + "/Slideshow Settings.txt", {
    "time for each slide": (config.parse_duration, "0:45"),
    "time for each transition": (config.parse_duration, "0:05"),
    "show slide numbers": (config.parse_polar, "YES"),
    "background color": (config.parse_color, "#000000"),
    "show status bar": (config.parse_polar, "YES"),
    "status bar text color": (config.parse_color, "#FFFCF0")
})
