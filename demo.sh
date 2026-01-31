#!/bin/bash
# Demo script for the line editor

echo "========================================="
echo "Line Editor Demo"
echo "========================================="
echo ""

echo "1. Creating a new file with the editor..."
echo ""

python3 line_editor.py << 'EOF'
0a
Welcome to the Line Editor!
This is a demonstration of its capabilities.
You can edit text line by line.
.
1,$n
w demo.txt
q
EOF

echo ""
echo "2. Viewing the created file..."
cat demo.txt
echo ""

echo "3. Editing the file - deleting line 2..."
python3 line_editor.py demo.txt << 'EOF'
2d
1,$n
w
q
EOF

echo ""
echo "4. Final content:"
cat demo.txt
echo ""

echo "========================================="
echo "Demo completed! Check out demo.txt"
echo "========================================="
