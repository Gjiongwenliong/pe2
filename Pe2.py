import curses
"""
A simple terminal-based text editor using the curses library.
This script creates a split terminal interface with an editor area and a command area.
- The editor area allows for basic text editing and cursor movement.
- The command area displays instructions and status messages.
Functions:
    main(stdscr): Initializes the curses environment, sets up the editor and command windows,
                  handles user input for navigation and mode switching, and manages the main event loop.
Usage:
    Run the script in a terminal. Use arrow keys to move the cursor, 'i' to activate insert mode,
    'ESC' to exit insert mode, 's' to save, and 'q' to quit the editor, and 'n' to set the filename, and 
    'f' to find a string.
"""

def find_string_in_content(editor_content, search_term, start_line=0, start_col=0):
    """
    在編輯器內容中搜尋字串,返回所有匹配的位置
    
    Args:
        editor_content: 編輯器內容列表
        search_term: 要搜尋的字串
        start_line: 開始搜尋的行號
        start_col: 開始搜尋的列號
    
    Returns:
        list: 包含 (line, col) 元組的列表,表示所有匹配位置
    """
    results = []
    
    for line_idx in range(len(editor_content)):
        line = editor_content[line_idx]
        col_idx = 0
        
        # 如果是起始行,從指定列開始搜尋
        if line_idx == start_line:
            col_idx = start_col
        
        while col_idx < len(line):
            pos = line.find(search_term, col_idx)
            if pos == -1:
                break
            
            # 只記錄在起始位置之後的結果
            if line_idx > start_line or (line_idx == start_line and pos >= start_col):
                results.append((line_idx, pos))
            
            col_idx = pos + 1
    
    return results

def main(stdscr):
    # 初始化 curses 設定
    curses.curs_set(1)  # 顯示游標
    stdscr.clear()
    stdscr.keypad(True)  # 啟用特殊按鍵
    
    # 初始化顏色配對
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # 反白效果 (整行)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # 游標字元底線效果
    
    # 取得終端機大小
    height, width = stdscr.getmaxyx()

    # 計算編輯區和命令區的大小
    editor_height = height - 3  # 預留 3 行給命令區
    command_height = 3
    
    # 建立編輯區視窗
    editor_win = curses.newwin(editor_height, width, 0, 0)
    editor_win.keypad(True)
    
    # 建立命令區視窗
    command_win = curses.newwin(command_height, width, editor_height, 0)
    
    # 初始化編輯器狀態
    editor_content = [""]
    cursor_x = 0
    cursor_y = 0
    insert_mode = False
    filename = "untitled.txt"
    
    # 搜尋相關狀態
    search_results = []
    current_search_index = 0
    last_search_term = ""
    
    # 主迴圈
    while True:
        # 更新編輯區顯示
        editor_win.clear()
        editor_win.box()
        mode_indicator = "[INSERT]" if insert_mode else "[NORMAL]"
        
        # 如果有搜尋結果,在標題列顯示
        search_info = ""
        if search_results:
            search_info = f" | Found: {current_search_index + 1}/{len(search_results)}"
        
        editor_win.addstr(0, 2, f" Editor - {filename} {mode_indicator} | Line: {cursor_y + 1}, Col: {cursor_x + 1}{search_info} ")
        
        # 顯示編輯內容,游標所在行使用反白
        for idx, line in enumerate(editor_content):
            if idx < editor_height - 2:
                display_line = line[:width-3]
                
                # 如果是游標所在行,使用反白顯示並在游標位置加底線
                if idx == cursor_y:
                    # 顯示游標前的文字
                    if cursor_x > 0:
                        editor_win.addstr(idx + 1, 1, display_line[:cursor_x], curses.color_pair(1))
                    
                    # 顯示游標位置的字元 (加上底線)
                    if cursor_x < len(display_line):
                        cursor_char = display_line[cursor_x]
                        editor_win.addstr(idx + 1, 1 + cursor_x, cursor_char, 
                                        curses.color_pair(1) | curses.A_UNDERLINE)
                    else:
                        # 如果游標在行尾,顯示空格加底線
                        editor_win.addstr(idx + 1, 1 + cursor_x, " ", 
                                        curses.color_pair(1) | curses.A_UNDERLINE)
                    
                    # 顯示游標後的文字
                    if cursor_x + 1 < len(display_line):
                        editor_win.addstr(idx + 1, 2 + cursor_x, display_line[cursor_x + 1:], curses.color_pair(1))
                    
                    # 填充剩餘空間使整行反白
                    remaining = width - 3 - len(display_line)
                    if remaining > 0:
                        editor_win.addstr(idx + 1, 1 + len(display_line), " " * remaining, curses.color_pair(1))
                else:
                    editor_win.addstr(idx + 1, 1, display_line)
        
        # 設定游標位置 (確保不超出範圍)
        cursor_x = min(cursor_x, len(editor_content[cursor_y]))
        editor_win.move(cursor_y + 1, cursor_x + 1)
        editor_win.refresh()
        
        # 更新命令區顯示
        command_win.clear()
        command_win.box()
        command_win.addstr(0, 2, " Commands ")
        if insert_mode:
            command_win.addstr(1, 1, "ESC: Normal mode | Type to edit")
        else:
            command_win.addstr(1, 1, "i: Insert | s: Save | q: Quit | n: Name | f: Find | Arrow keys: Move")
        command_win.refresh()
        
        # 取得使用者輸入
        key = editor_win.getch()
        
        # 處理按鍵
        if not insert_mode:
            # Normal mode
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord('i') or key == ord('I'):
                insert_mode = True
            elif key == ord('f') or key == ord('F'):
                # 搜尋功能
                curses.echo()
                command_win.addstr(1, 1, "Find: ".ljust(width-3))
                command_win.refresh()
                search_term = command_win.getstr(1, 7, 60).decode('utf-8')
                curses.noecho()
                
                if search_term:
                    # 執行搜尋
                    last_search_term = search_term
                    search_results = find_string_in_content(editor_content, search_term)
                    
                    if search_results:
                        current_search_index = 0
                        # 移動游標到第一個搜尋結果
                        cursor_y, cursor_x = search_results[0]
                        command_win.addstr(1, 1, f"Found {len(search_results)} match(es). Press 'n' for next.".ljust(width-3))
                    else:
                        search_results = []
                        command_win.addstr(1, 1, f"Pattern not found: {search_term}".ljust(width-3))
                    
                    command_win.refresh()
                    curses.napms(1500)
            elif key == ord('n') and search_results:
                # 移動到下一個搜尋結果
                current_search_index = (current_search_index + 1) % len(search_results)
                cursor_y, cursor_x = search_results[current_search_index]
            elif key == ord('N') and search_results:
                # 移動到上一個搜尋結果
                current_search_index = (current_search_index - 1) % len(search_results)
                cursor_y, cursor_x = search_results[current_search_index]
            elif key == ord('n') or key == ord('N'):
                # 輸入檔名
                curses.echo()
                command_win.addstr(1, 1, "Enter filename: ".ljust(width-3))
                command_win.refresh()
                filename = command_win.getstr(1, 17, 60).decode('utf-8')
                filename = filename + ".txt" if not filename.endswith(".txt") else filename     
                curses.noecho()
            elif key == ord('s') or key == ord('S'):
                # 儲存檔案
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(editor_content))
                    command_win.addstr(1, 1, f"Saved to {filename}!".ljust(width-3))
                    command_win.refresh()
                    curses.napms(1000)  # 顯示 1 秒
                except Exception as e:
                    command_win.addstr(1, 1, f"Error: {str(e)}"[:width-3])
                    command_win.refresh()
                    curses.napms(2000)
            elif key == curses.KEY_UP and cursor_y > 0:
                cursor_y -= 1
                cursor_x = min(cursor_x, len(editor_content[cursor_y]))
            elif key == curses.KEY_DOWN and cursor_y < len(editor_content) - 1:
                cursor_y += 1
                cursor_x = min(cursor_x, len(editor_content[cursor_y]))
            elif key == curses.KEY_LEFT and cursor_x > 0:
                cursor_x -= 1
            elif key == curses.KEY_RIGHT and cursor_x < len(editor_content[cursor_y]):
                cursor_x += 1
        else:
            # Insert mode
            if key == 27:  # ESC 鍵
                insert_mode = False
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                # 刪除字元
                if cursor_x > 0:
                    line = editor_content[cursor_y]
                    editor_content[cursor_y] = line[:cursor_x-1] + line[cursor_x:]
                    cursor_x -= 1
                elif cursor_y > 0:
                    # 合併到上一行
                    cursor_x = len(editor_content[cursor_y - 1])
                    editor_content[cursor_y - 1] += editor_content[cursor_y]
                    editor_content.pop(cursor_y)
                    cursor_y -= 1
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                # 換行
                line = editor_content[cursor_y]
                editor_content[cursor_y] = line[:cursor_x]
                editor_content.insert(cursor_y + 1, line[cursor_x:])
                cursor_y += 1
                cursor_x = 0
            elif key == curses.KEY_UP and cursor_y > 0:
                cursor_y -= 1
                cursor_x = min(cursor_x, len(editor_content[cursor_y]))
            elif key == curses.KEY_DOWN and cursor_y < len(editor_content) - 1:
                cursor_y += 1
                cursor_x = min(cursor_x, len(editor_content[cursor_y]))
            elif key == curses.KEY_LEFT and cursor_x > 0:
                cursor_x -= 1
            elif key == curses.KEY_RIGHT and cursor_x < len(editor_content[cursor_y]):
                cursor_x += 1
            elif 32 <= key <= 126:  # 可列印字元
                char = chr(key)
                line = editor_content[cursor_y]
                editor_content[cursor_y] = line[:cursor_x] + char + line[cursor_x:]
                cursor_x += 1

if __name__ == "__main__":
    print("程式開始執行...")
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        print("程式結束")