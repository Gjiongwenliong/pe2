import sys

# class LineBuffer:
#     def __init__(self):
#         self.lines = []

#     def add_line(self, text):
#         self.lines.append(text)

#     def save(self, filename="voucher.txt"):
#         with open(filename, "w", encoding="utf-8") as f:
#             for line in self.lines:
#                 f.write(line + "\n")

# class InputLayer:
#     def __init__(self, buffer):
#         self.buffer = buffer

#     def enter_Line(self):
#         print("=== 文字輸入端 ===")
#         self.text = input("字串輸入並選擇儲存: :save 或退出: :exit >")
#         credit = input("貸方科目: ")
#         self.buffer.add_line(f"{debit} -> {credit} : {amount}")

# class CommandLayer:
#     def __init__(self, buffer):
#         self.buffer = buffer

#     def run_command(self, cmd):
#         if cmd == ":save":
#             self.buffer.save()
#             print("已儲存傳票")
#         elif cmd == ":exit":
#             print("退出程式")
#             sys.exit(0)
#         else:
#             print("未知指令")

# def main():
#     buffer = LineBuffer()
#     input_layer = InputLayer(buffer)
#     command_layer = CommandLayer(buffer)

#     while True:
#         mode = input("選擇模式 (i=輸入, c=命令): ")
#         if mode == "i":
#             input_layer.enter_Line()
#         elif mode == "c":
#             cmd = input("命令列: ")
#             command_layer.run_command(cmd)

# if __name__ == "__main__":
#     main()
    

# 使用 curses 建立一個整頁式借貸傳票輸入畫面


import curses
import json
from datetime import datetime
from typing import List, Dict

# class VoucherEntry:
#     """借貸傳票輸入系統"""
    
class LineBuffer:
    def __init__(self):
        self.lines = []

    def add_line(self, text):
        self.lines.append(text)    

    def save(self, filename="voucher.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for line in self.lines:
                f.write(line + "\n")

class InputLayer:
    def __init__(self, buffer):
        self.buffer = buffer

    def enter_Line(self):
        print("=== 文字輸入端 ===")
        self.text = input("字串輸入並選擇儲存: :save 或退出: :exit >")
        self.buffer.add_line(self.text)

class CommandLayer:
    def __init__(self, buffer):
        self.buffer = buffer

    def run_command(self, cmd):
        if cmd == ":save":
            self.buffer.save()
            print("已儲存傳票")
        elif cmd == ":exit":
            print("退出程式")
            sys.exit(0)
        else:
            print("未知指令")

def main():
    buffer = LineBuffer()
    input_layer = InputLayer(buffer)
    command_layer = CommandLayer(buffer)

    while True:
        mode = input("選擇模式 (i=輸入, c=命令): ")
        if mode == "i":
            input_layer.enter_Line()
        elif mode == "c":
            cmd = input("命令列: ")
            command_layer.run_command(cmd)

if __name__ == "__main__":
    main()


#     def run(self, stdscr):

#         """主執行函數"""
#         curses.curs_set(1)  # 顯示游標
#         stdscr.clear()
        
#         # 定義顏色配對
#         curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)    # 標題
#         curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)    # 輸入欄位
#         curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # 標籤
#         curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # 明細表頭
        
#         while True:
#             self.draw_screen(stdscr)
            
#             key = stdscr.getch()
            
#             if key == curses.KEY_F1:
#                 break
#             elif key == curses.KEY_UP:
#                 self.move_up()
#             elif key == curses.KEY_DOWN or key == ord('\t'):
#                 self.move_down()
#             elif key == curses.KEY_LEFT:
#                 self.move_left()
#             elif key == curses.KEY_RIGHT:
#                 self.move_right()
#             elif key == curses.KEY_F2:
#                 self.add_entry()
#             elif key == curses.KEY_F3:
#                 self.delete_entry()
#             elif key == curses.KEY_F10:
#                 self.save_voucher(stdscr)
#             elif key in (curses.KEY_BACKSPACE, 127, 8):
#                 self.handle_backspace()
#             elif 32 <= key <= 126:  # 可列印字元
#                 self.handle_input(chr(key))
    
#     def move_up(self):
#         """上移欄位"""
#         if self.current_field >= 3:  # 在明細區
#             if self.current_entry > 0:
#                 self.current_entry -= 1
#             else:
#                 self.current_field = 2  # 回到摘要欄
#         else:
#             self.current_field = max(0, self.current_field - 1)
    
#     def move_down(self):
#         """下移欄位"""
#         if self.current_field < 3:
#             if self.entries:  # 如果有明細資料
#                 self.current_field = 3
#                 self.current_entry = 0
#             else:
#                 self.current_field = min(2, self.current_field + 1)
#         else:  # 在明細區
#             if self.current_entry < len(self.entries) - 1:
#                 self.current_entry += 1
    
#     def move_left(self):
#         """左移欄位 (僅在明細區)"""
#         if self.current_field >= 3:
#             self.current_col = max(0, self.current_col - 1)
    
#     def move_right(self):
#         """右移欄位 (僅在明細區)"""
#         if self.current_field >= 3:
#             self.current_col = min(4, self.current_col + 1)
                
#     def draw_screen(self, stdscr):
#         """繪製整個畫面"""
#         height, width = stdscr.getmaxyx()
#         stdscr.clear()
        
#         # 繪製標題
#         title = "借貸傳票輸入系統"
#         stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
#         stdscr.addstr(0, (width - len(title)) // 2, title)
#         stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
        
#         # 繪製輸入欄位區域
#         self.draw_header_fields(stdscr, 2)
        
#         # 繪製明細表格
#         self.draw_entries_table(stdscr, 10)
        
#         # 繪製功能鍵說明
#         self.draw_footer(stdscr, height - 2)
        
#         # 繪製總計
#         self.draw_totals(stdscr, height - 4)
        
#         stdscr.refresh()
        
#     def draw_header_fields(self, stdscr, start_row):
#         """繪製表頭輸入欄位"""
#         fields = [
#             ("傳票號碼:", self.voucher_no, 0),
#             ("傳票日期:", self.voucher_date, 1),
#             ("摘要說明:", self.description, 2)
#         ]
        
#         for i, (label, value, field_idx) in enumerate(fields):
#             row = start_row + i * 2
            
#             # 繪製標籤
#             stdscr.attron(curses.color_pair(3))
#             stdscr.addstr(row, 2, label)
#             stdscr.attroff(curses.color_pair(3))
            
#             # 繪製輸入欄位
#             field_width = 60
#             if self.current_field == field_idx:
#                 stdscr.attron(curses.color_pair(2))
#             stdscr.addstr(row, 15, value.ljust(field_width))
#             if self.current_field == field_idx:
#                 stdscr.attroff(curses.color_pair(2))
                
#     def draw_entries_table(self, stdscr, start_row):
#         """繪製明細表格"""
#         # 表頭
#         headers = ["項次", "科目代碼", "科目名稱", "借方金額", "貸方金額", "說明"]
#         col_widths = [6, 12, 20, 15, 15, 25]
        
#         stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
#         col_pos = 2
#         for header, width in zip(headers, col_widths):
#             stdscr.addstr(start_row, col_pos, header.ljust(width))
#             col_pos += width + 1
#         stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
        
#         # 分隔線
#         stdscr.addstr(start_row + 1, 2, "─" * 95)
        
#         # 明細資料
#         for i, entry in enumerate(self.entries[:10]):  # 最多顯示10筆
#             row = start_row + 2 + i
#             col_pos = 2
            
#             values = [
#                 str(i + 1),
#                 entry.get('account_code', ''),
#                 entry.get('account_name', ''),
#                 entry.get('debit', ''),
#                 entry.get('credit', ''),
#                 entry.get('note', '')
#             ]
            
#             # 繪製每個欄位
#             for col_idx, (value, width) in enumerate(zip(values, col_widths)):
#                 is_current = (self.current_field >= 3 and 
#                              self.current_entry == i and 
#                              self.current_col == col_idx - 1)  # -1 因為項次不可編輯
                
#                 if is_current:
#                     stdscr.attron(curses.color_pair(2))
#                 elif self.current_field >= 3 and self.current_entry == i:
#                     stdscr.attron(curses.A_DIM)
                    
#                 stdscr.addstr(row, col_pos, str(value).ljust(width))
                
#                 if is_current:
#                     stdscr.attroff(curses.color_pair(2))
#                 elif self.current_field >= 3 and self.current_entry == i:
#                     stdscr.attroff(curses.A_DIM)
                    
#                 col_pos += width + 1
            
#     def draw_totals(self, stdscr, row):
#         """繪製借貸總計"""
#         total_debit = sum(float(e.get('debit', '0') or '0') for e in self.entries)
#         total_credit = sum(float(e.get('credit', '0') or '0') for e in self.entries)
#         balance = total_debit - total_credit
        
#         stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
#         stdscr.addstr(row, 2, f"借方合計: {total_debit:>15,.2f}  ")
#         stdscr.addstr(row, 40, f"貸方合計: {total_credit:>15,.2f}  ")
#         stdscr.addstr(row, 78, f"差額: {balance:>12,.2f}")
#         stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
        
#     def draw_footer(self, stdscr, row):
#         """繪製功能鍵說明"""
#         footer = "F2:新增明細 F3:刪除明細 F10:儲存 ↑↓←→:移動欄位 F1:離開"
#         stdscr.attron(curses.color_pair(1))
#         stdscr.addstr(row, 2, footer)
#         stdscr.attroff(curses.color_pair(1))
        
#     def handle_input(self, char):
#         """處理文字輸入"""
#         if self.current_field == 0:
#             self.voucher_no += char
#         elif self.current_field == 1:
#             self.voucher_date += char
#         elif self.current_field == 2:
#             self.description += char
#         elif self.current_field >= 3 and self.current_entry < len(self.entries):
#             # 在明細區輸入
#             entry = self.entries[self.current_entry]
#             col_keys = ['account_code', 'account_name', 'debit', 'credit', 'note']
#             if self.current_col < len(col_keys):
#                 entry[col_keys[self.current_col]] = entry.get(col_keys[self.current_col], '') + char
            
#     def handle_backspace(self):
#         """處理退格鍵"""
#         if self.current_field == 0 and self.voucher_no:
#             self.voucher_no = self.voucher_no[:-1]
#         elif self.current_field == 1 and self.voucher_date:
#             self.voucher_date = self.voucher_date[:-1]
#         elif self.current_field == 2 and self.description:
#             self.description = self.description[:-1]
#         elif self.current_field >= 3 and self.current_entry < len(self.entries):
#             # 在明細區刪除
#             entry = self.entries[self.current_entry]
#             col_keys = ['account_code', 'account_name', 'debit', 'credit', 'note']
#             if self.current_col < len(col_keys):
#                 key = col_keys[self.current_col]
#                 if entry.get(key):
#                     entry[key] = entry[key][:-1]
            
#     def add_entry(self):
#         """新增明細"""
#         self.entries.append({
#             'account_code': '',
#             'account_name': '',
#             'debit': '',
#             'credit': '',
#             'note': ''
#         })
#         self.current_entry = len(self.entries) - 1
#         self.current_field = 3
#         self.current_col = 0
        
#     def delete_entry(self):
#         """刪除明細"""
#         if self.entries and self.current_entry < len(self.entries):
#             self.entries.pop(self.current_entry)
#             if self.current_entry > 0:
#                 self.current_entry -= 1
#             if not self.entries:
#                 self.current_field = 2  # 回到摘要欄
                
#     def save_voucher(self, stdscr):
#         """儲存傳票到 JSON 檔案"""
#         voucher_data = {
#             'voucher_no': self.voucher_no,
#             'voucher_date': self.voucher_date,
#             'description': self.description,
#             'entries': self.entries,
#             'created_at': datetime.now().isoformat()
#         }
        
#         try:
#             # 讀取現有資料
#             try:
#                 with open('vouchers.json', 'r', encoding='utf-8') as f:
#                     all_vouchers = json.load(f)
#             except FileNotFoundError:
#                 all_vouchers = []
            
#             # 加入新傳票
#             all_vouchers.append(voucher_data)
            
#             # 寫入檔案
#             with open('vouchers.json', 'w', encoding='utf-8') as f:
#                 json.dump(all_vouchers, f, ensure_ascii=False, indent=2)
            
#             msg = f"傳票 {self.voucher_no} 已儲存！按任意鍵繼續..."
            
#         except Exception as e:
#             msg = f"儲存失敗: {str(e)} 按任意鍵繼續..."
        
#         height, width = stdscr.getmaxyx()
#         stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
#         stdscr.addstr(height // 2, (width - len(msg)) // 2, msg)
#         stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
#         stdscr.getch()

# def main():
#     """主程式進入點"""
#     app = VoucherEntry()
#     curses.wrapper(app.run)

# if __name__ == "__main__":
#     main()