#!/usr/bin/env python3
"""
Practical examples of using the line editor.
This script demonstrates various use cases.
"""

import subprocess
import os


def run_example(title, description, commands, filename=None):
    """Run an example and display the results."""
    print(f"\n{'='*60}")
    print(f"Example: {title}")
    print(f"{'='*60}")
    print(f"Description: {description}\n")
    
    print("Commands:")
    for cmd in commands.split('\n'):
        if cmd.strip():
            print(f"  {cmd}")
    print()
    
    cmd_list = ['python3', 'line_editor.py']
    if filename:
        cmd_list.append(filename)
    
    process = subprocess.Popen(
        cmd_list,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=commands)
    print("Output:")
    print(stdout)
    if stderr:
        print("Errors:", stderr)


def main():
    """Run all examples."""
    print("Line Editor - Practical Examples")
    print("="*60)
    
    # Example 1: Creating a simple TODO list
    run_example(
        "Creating a TODO List",
        "Use the line editor to create a simple task list",
        """0a
TODO List:
- Buy groceries
- Fix the bug in line_editor.py
- Write documentation
- Call the client
.
1,$n
w todo.txt
q
"""
    )
    
    # Example 2: Editing a configuration file
    run_example(
        "Viewing and Editing a Config",
        "Load a file, view it, and make changes",
        """1,$p
3d
2a
- Updated task
.
1,$n
w
q
""",
        filename="todo.txt"
    )
    
    # Example 3: Quick text processing
    run_example(
        "Replacing Multiple Lines",
        "Change a range of lines in one operation",
        """1,$p
2,4c
=== COMPLETED TASKS ===
✓ Task 1 done
✓ Task 2 done
.
1,$p
w
q
""",
        filename="todo.txt"
    )
    
    print(f"\n{'='*60}")
    print("Examples completed!")
    print(f"{'='*60}")
    
    # Show final file
    if os.path.exists('todo.txt'):
        print("\nFinal todo.txt content:")
        with open('todo.txt', 'r') as f:
            print(f.read())


if __name__ == '__main__':
    main()
