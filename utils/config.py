# This file contains a pretty good function for loading settings
# and a few functions that parse specific kinds of values.

# TODO: Make the automatic addition of settings neater.

import os

import utils.log as log

def load_settings(path, settings):
    # Loads the specified settings from the specified file.
    #
    # Takes a dictionary where keys are setting names and values are tuples
    # containing a parser function and default value in that order.
    # The default values are in the format they'd be in in the file.
    # The keys should be in all lowercase.
    #
    # The file contains a case-insensitive key per line, a colon, then a value.
    # Whitespace around both key and value is always stripped.
    # Lines beginning with a space and lines with no colon are ignored.
    #
    # Returns a dictionary with the values of the specified settings.

    values = {}

    # Create the file if it does not exist.
    if not os.path.exists(path):
        file = open(path, "w")
        file.close()

    # Parse the settings already in the file.
    file = open(path, "r")
    lines = file.readlines()
    for line in lines:
        try:
            colon = line.index(":")
        except:
            colon = -1
        if colon > -1 and line[0] != " ":
            key = line[0:colon].strip().lower()
            if key in settings:
                try:
                    values[key] = settings[key][0](line[colon + 1:].strip())
                except:
                    values[key] = settings[key][0](settings[key][1])
                    log.out(f"Malformed value for setting `{key}` in `{os.path.basename(path)}`!\nDelete the setting and re-run the slideshow\nto reset it to `{settings[key][1]}`.", log.C_WARNING)

    file.close()

    # Add the other settings to the file.
    file = open(path, "a")
    addedAnything = False
    for key in settings:
        if not (key in values):
            file.write(f"\n{key}: {settings[key][1]}")
            values[key] = settings[key][0](settings[key][1])
            addedAnything = True
    if addedAnything:
        file.write("\n")
    file.close()

    return values

def parse_polar(string):
    # Parses an answer to a polar question.
    # Can be "YES" (True) or "NO" (False), case-insensitive.
    # Raises an error if it's not one of those.
    # Returns the answer as a boolean.

    string = string.upper()
    if string == "YES":
        return True
    if string == "NO":
        return False
    raise ValueError(f"Expected `YES` or `NO`, but got `{string}`.")

def parse_percentage(string):
    # Parses a percentage.
    # Returns it as a float where 0% = 0 and 100% = 1.

    if string[-1] == "%":
        string = string[:-1]

    return float(string) / 100

def parse_list(string):
    # Parses a comma-separated list of strings.

    things = string.split(",")
    for i in range(0, len(things)):
        things[i] = things[i].strip()
    return things

def parse_duration(string):
    # Parses an amount of time specified as hours, minutes, and seconds.
    # These units are separated by colons and are all optional.
    # Returns the time in seconds.

    sections = string.split(":")
    multiplier = 1
    total = 0
    for i in range(len(sections) - 1, -1, -1):
        total += float(sections[i]) * multiplier
        multiplier *= 60
    return total

def parse_color(string):
    # Parses a hex code for a color.
    # Returns a tuple containing red, green, and blue values.

    if string[0] == "#":
        string = string[1:]
    if len(string) == 6:
        return (int(string[0:2], 16), int(string[2:4], 16), int(string[4:6], 16))
    if len(string) == 3:
        return (int(string[0], 16), int(string[1], 16), int(string[2], 16))
    raise ValueError("Color code must be 3 or 6 characters long; got {len(string)}.")
