# This file is an overengineered logging system.

# Message categories.
C_ALL = 255 # Shorthand for every category combined.
C_INFO = 1 # Messages about things going as they should.
C_WARNING = 2 # Messages about minor or potential problems.
C_ERROR = 4 # Messages about significant problems.
C_CRITICAL = 8 # Messages about critical/fatal errors.
C_ISSUE = 128 # Messages about problems with remote files.

# Categories of messages to show in the terminal.
terminal_categories = C_ALL

# Categories of messages to write to the local log.
local_categories = C_CRITICAL | C_ISSUE

def out(text, categories = C_INFO):
    if categories & terminal_categories:
        print(text + "\n")

    if categories & local_categories:
        file = open("./Local Log.txt", "a")
        file.write(f"\n{text}\n")
        file.close()
