#!/usr/bin/env python3
"""
Test script for the line editor.
"""

import subprocess
import os
import sys


def run_editor_commands(filename, commands):
    """Run the editor with a series of commands."""
    # Join commands with newlines
    input_text = '\n'.join(commands) + '\n'
    
    # Run the editor
    process = subprocess.Popen(
        ['python3', 'line_editor.py', filename] if filename else ['python3', 'line_editor.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=input_text)
    return stdout, stderr, process.returncode


def test_basic_operations():
    """Test basic editor operations."""
    print("Testing basic operations...")
    
    # Test 1: Load file and print
    print("\n1. Loading and printing file:")
    stdout, stderr, _ = run_editor_commands('test_file.txt', ['1,$p', 'q'])
    print(stdout)
    
    # Test 2: Print with line numbers
    print("\n2. Print with line numbers:")
    stdout, stderr, _ = run_editor_commands('test_file.txt', ['1,$n', 'q'])
    print(stdout)
    
    # Test 3: Create new file with append
    print("\n3. Creating new content:")
    commands = [
        '0a',
        'Hello, World!',
        'This is a test.',
        'Line editor works!',
        '.',
        '1,$p',
        'w test_output.txt',
        'q'
    ]
    stdout, stderr, _ = run_editor_commands(None, commands)
    print(stdout)
    
    # Verify the output file
    if os.path.exists('test_output.txt'):
        print("\nContent of test_output.txt:")
        with open('test_output.txt', 'r') as f:
            print(f.read())
    
    # Test 4: Delete lines
    print("\n4. Testing delete operation:")
    commands = [
        '1,$p',
        '2,3d',
        '1,$p',
        'Q'
    ]
    stdout, stderr, _ = run_editor_commands('test_file.txt', commands)
    print(stdout)
    
    print("\n✅ All tests completed!")


def test_help():
    """Test help command."""
    print("\nTesting help command:")
    stdout, stderr, _ = run_editor_commands(None, ['h', 'q'])
    print(stdout)


if __name__ == '__main__':
    test_help()
    test_basic_operations()
