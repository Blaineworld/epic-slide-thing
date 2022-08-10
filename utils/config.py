# This file contains configuration file parsing functionality.

def parse_polar(string):
    # Parses an answer to a polar question.
    # Can be "YES" (True) or "NO" (False), case-insensitive.
    # Raises an error if it's not one of those.
    string = string.upper()
    if string == "YES":
        return True
    if string == "NO":
        return False
    raise ValueError("Expected `YES` or `NO`, but got `" + string + "`.")

def parse_time(string):
    # Parses an amount of time specified as seconds, minutes, and hours.
    # These units are separated by colons and are all optional.
    # Technically goes up in powers of 60 forever.
    # Returns a number of seconds.

    # NOTE TO SELF: WRITE THIS FUNCTION LATER!
    pass

def parse_settings(lines):
    # Parses the lines of a configuration file.
    # A case-insensitive key per line, then a colon, then a value.
    # Whitespace around both key and value is always stripped.
    # Blank lines and lines beginning with two spaces are ignored.
    # Returns a tuple with a dictionary and a list of lines with missing colons.
    settings = {}
    missing_colon_line_numbers = []

    for index in range(0, len(lines)):
        line = lines[index]
        if line != "\n" and line[0:2] != "  ":
            try:
                colon = line.index(":")
                settings[line[0:colon].strip().lower()] = line[colon + 1:].strip()
            except:
                missing_colon_line_numbers.append(index + 1)

    return (settings, missing_colon_line_numbers)

print(parse_polar("nn"))
