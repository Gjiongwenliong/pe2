#!/usr/bin/env python3
"""
A simple line-oriented text editor.
Inspired by classic Unix 'ed' editor but with a more user-friendly interface.
"""

import sys
import os
import re


class LineEditor:
    """A simple line editor for text files."""
    
    def __init__(self, filename=None):
        self.lines = []
        self.current_line = 0
        self.filename = filename
        self.modified = False
        
        if filename and os.path.exists(filename):
            self.load_file(filename)
    
    def load_file(self, filename):
        """Load a file into the editor."""
        try:
            with open(filename, 'r') as f:
                self.lines = [line.rstrip('\n') for line in f]
            self.filename = filename
            self.current_line = len(self.lines)
            self.modified = False
            print(f"{len(self.lines)} lines read from {filename}")
        except IOError as e:
            print(f"Error reading file: {e}")
    
    def save_file(self, filename=None):
        """Save the buffer to a file."""
        if filename:
            self.filename = filename
        
        if not self.filename:
            print("No filename specified")
            return False
        
        try:
            with open(self.filename, 'w') as f:
                for line in self.lines:
                    f.write(line + '\n')
            self.modified = False
            print(f"{len(self.lines)} lines written to {self.filename}")
            return True
        except IOError as e:
            print(f"Error writing file: {e}")
            return False
    
    def parse_address(self, addr_str):
        """Parse line address (supports numbers, $, ., +, -)."""
        if not addr_str or addr_str == '.':
            return self.current_line
        elif addr_str == '$':
            return len(self.lines)
        elif addr_str.startswith('+'):
            offset = int(addr_str[1:]) if len(addr_str) > 1 else 1
            return min(self.current_line + offset, len(self.lines))
        elif addr_str.startswith('-'):
            offset = int(addr_str[1:]) if len(addr_str) > 1 else 1
            return max(self.current_line - offset, 0)
        else:
            try:
                return int(addr_str)
            except ValueError:
                return None
    
    def parse_range(self, range_str):
        """Parse address range (e.g., '1,5' or '.,+3' or '1,$')."""
        if not range_str:
            return self.current_line, self.current_line
        
        if ',' in range_str:
            parts = range_str.split(',', 1)
            start = self.parse_address(parts[0].strip())
            end = self.parse_address(parts[1].strip())
        else:
            addr = self.parse_address(range_str.strip())
            start = end = addr
        
        if start is None or end is None:
            return None, None
        
        return start, end
    
    def print_lines(self, start, end, show_numbers=False):
        """Print lines in the specified range."""
        if start < 1 or end > len(self.lines):
            print("Invalid line range")
            return
        
        for i in range(start - 1, end):
            if show_numbers:
                print(f"{i + 1}\t{self.lines[i]}")
            else:
                print(self.lines[i])
        
        self.current_line = end
    
    def append_lines(self, after_line):
        """Append lines after the specified line."""
        if after_line < 0 or after_line > len(self.lines):
            print("Invalid line number")
            return
        
        print("Enter text (type '.' on a line by itself to finish):")
        new_lines = []
        while True:
            try:
                line = input()
                if line == '.':
                    break
                new_lines.append(line)
            except EOFError:
                break
        
        self.lines[after_line:after_line] = new_lines
        self.current_line = after_line + len(new_lines)
        self.modified = True
    
    def insert_lines(self, before_line):
        """Insert lines before the specified line."""
        self.append_lines(before_line - 1)
    
    def delete_lines(self, start, end):
        """Delete lines in the specified range."""
        if start < 1 or end > len(self.lines):
            print("Invalid line range")
            return
        
        del self.lines[start - 1:end]
        self.current_line = min(start, len(self.lines))
        self.modified = True
    
    def change_lines(self, start, end):
        """Change (replace) lines in the specified range."""
        if start < 1 or end > len(self.lines):
            print("Invalid line range")
            return
        
        print("Enter replacement text (type '.' on a line by itself to finish):")
        new_lines = []
        while True:
            try:
                line = input()
                if line == '.':
                    break
                new_lines.append(line)
            except EOFError:
                break
        
        self.lines[start - 1:end] = new_lines
        self.current_line = start - 1 + len(new_lines)
        self.modified = True
    
    def show_help(self):
        """Display help information."""
        help_text = """
Line Editor Commands:
  [n]p          Print line n (or current line)
  [m,n]p        Print lines m through n
  [n]a          Append text after line n (or current line)
  [n]i          Insert text before line n (or current line)
  [m,n]d        Delete lines m through n
  [m,n]c        Change (replace) lines m through n
  [m,n]n        Print lines with line numbers
  w [file]      Write buffer to file
  r [file]      Read file into buffer
  q             Quit (warns if modified)
  Q             Quit without saving
  h             Show this help

Address Syntax:
  n             Line number n
  .             Current line
  $             Last line
  +[n]          n lines forward (default 1)
  -[n]          n lines backward (default 1)
  m,n           Range from line m to line n

Examples:
  1,5p          Print lines 1 through 5
  .,$p          Print current line through end
  3a            Append after line 3
  1,10d         Delete lines 1 through 10
"""
        print(help_text)
    
    def run(self):
        """Main editor loop."""
        print("Line Editor - Type 'h' for help, 'q' to quit")
        
        while True:
            try:
                # Get command from user
                try:
                    command = input(":")
                except EOFError:
                    print()
                    break
                
                command = command.strip()
                if not command:
                    continue
                
                # Parse command
                match = re.match(r'^([\d\.\$\+\-,]*)([a-zA-Z]?)(.*)$', command)
                if not match:
                    print("Invalid command")
                    continue
                
                addr_part = match.group(1)
                cmd = match.group(2)
                arg = match.group(3).strip()
                
                # Execute command
                if cmd == 'q':
                    if self.modified:
                        print("Warning: buffer modified. Use 'Q' to quit without saving, 'w' to save.")
                        continue
                    break
                elif cmd == 'Q':
                    break
                elif cmd == 'h':
                    self.show_help()
                elif cmd == 'w':
                    filename = arg if arg else self.filename
                    self.save_file(filename)
                elif cmd == 'r':
                    if arg:
                        self.load_file(arg)
                    else:
                        print("No filename specified")
                elif cmd == 'p':
                    start, end = self.parse_range(addr_part)
                    if start is not None:
                        self.print_lines(start, end)
                elif cmd == 'n':
                    start, end = self.parse_range(addr_part)
                    if start is not None:
                        self.print_lines(start, end, show_numbers=True)
                elif cmd == 'a':
                    addr = self.parse_address(addr_part) if addr_part else self.current_line
                    if addr is not None:
                        self.append_lines(addr)
                elif cmd == 'i':
                    addr = self.parse_address(addr_part) if addr_part else self.current_line
                    if addr is not None:
                        self.insert_lines(addr)
                elif cmd == 'd':
                    start, end = self.parse_range(addr_part)
                    if start is not None:
                        self.delete_lines(start, end)
                elif cmd == 'c':
                    start, end = self.parse_range(addr_part)
                    if start is not None:
                        self.change_lines(start, end)
                else:
                    print("Unknown command. Type 'h' for help.")
            
            except KeyboardInterrupt:
                print()
                continue
            except Exception as e:
                print(f"Error: {e}")
                continue


def main():
    """Main entry point."""
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    editor = LineEditor(filename)
    editor.run()


if __name__ == '__main__':
    main()
