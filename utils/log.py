# This file contains logging functionality.
# Right now, it's very basic, but I intend to make it more complex later on.

terminal_priority = 1

def log(text, priority = 0):
    if priority >= terminal_priority:
        print(text)
