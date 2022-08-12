import os
import utils.config as config

# Load the instance settings.
instance = config.load_settings("./Instance Settings.txt", {
    "backup video drivers": (config.parse_list, "fbcon, directfb, svgalib, xvfb, Xvfb, x11"),
    "path to remote folder": (str, "./files"),
    "show debug info": (config.parse_polar, "NO"),
})

# Load the slideshow settings.
slideshow = config.load_settings(instance["path to remote folder"] + "/Slideshow Settings.txt", {
    "show slide numbers": (config.parse_polar, "YES"),
    "time to show each image": (config.parse_duration, "0:45")
})
