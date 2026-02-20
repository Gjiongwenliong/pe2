# pe2 - Line Editor

A simple line-oriented text editor inspired by the classic Unix `ed` editor, built with Python 3.

## Overview

This is a command-line line editor that allows you to edit text files line by line. It's designed for situations where you need precise control over individual lines of text or when working in environments without a full-screen editor.

## Features

- Load and save text files
- Insert, append, and delete lines
- Change (replace) lines
- Print lines with or without line numbers
- Support for line addressing (numbers, ranges, relative positions)
- Warning on quit if file is modified
- Built-in help system

## Installation

No installation required! Just make sure you have Python 3 installed:

```bash
python3 --version
```

Make the script executable (Linux/Mac):
```bash
chmod +x line_editor.py
```

## Usage

### Starting the Editor

```bash
# Start with a new empty buffer
python3 line_editor.py

# Open an existing file
python3 line_editor.py filename.txt

# Or if executable
./line_editor.py filename.txt
```

### Commands

| Command | Description |
|---------|-------------|
| `[n]p` | Print line n (or current line if n is omitted) |
| `[m,n]p` | Print lines m through n |
| `[n]a` | Append text after line n (or current line) |
| `[n]i` | Insert text before line n (or current line) |
| `[m,n]d` | Delete lines m through n |
| `[m,n]c` | Change (replace) lines m through n |
| `[m,n]n` | Print lines with line numbers |
| `w [file]` | Write buffer to file |
| `r [file]` | Read file into buffer |
| `q` | Quit (warns if modified) |
| `Q` | Quit without saving |
| `h` | Show help |

### Address Syntax

| Address | Meaning |
|---------|---------|
| `n` | Line number n |
| `.` | Current line |
| `$` | Last line |
| `+[n]` | n lines forward (default 1) |
| `-[n]` | n lines backward (default 1) |
| `m,n` | Range from line m to line n |

### Examples

```bash
# Print all lines
1,$p

# Print current line through end
.,$p

# Append text after line 3
3a
Hello World
.

# Delete lines 1 through 10
1,10d

# Print lines with numbers
1,$n

# Save to file
w output.txt

# Change lines 5-7
5,7c
New line 5
New line 6
New line 7
.
```

### Interactive Session Example

```
$ python3 line_editor.py
Line Editor - Type 'h' for help, 'q' to quit
:0a
Enter text (type '.' on a line by itself to finish):
Hello, World!
This is my first line.
And this is my second line.
.
:1,$p
Hello, World!
This is my first line.
And this is my second line.
:w greeting.txt
3 lines written to greeting.txt
:q
```

## Testing

Run the included test script:

```bash
python3 test_editor.py
```

## Requirements

- Python 3.6 or higher
- No external dependencies

## License

This is a simple educational project. Feel free to use and modify as needed.
