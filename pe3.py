import curses
import json


class VoucherEntry:
    def __init__(self):
        self.current_field = 0
        self.current_col = 0
        self.entries = []
        self.voucher_no = ""
        self.voucher_date = ""
        self.description = ""

    def run(self, stdscr):
        """主執行函數"""
        curses.curs_set(1)  # 顯示游標
        stdscr.clear()
        while True:
            self.draw_screen(stdscr)
            key = stdscr.getch()
            if key == curses.KEY_F1:
                break
            elif key == curses.KEY_UP:
                self.move_up()
            elif key == curses.KEY_DOWN or key == ord('\t'):
                self.move_down()
            elif key == curses.KEY_LEFT:
                self.move_left()
            elif key == curses.KEY_RIGHT:
                self.move_right()
            elif key == curses.KEY_F2:
                self.add_entry()
            elif key == curses.KEY_F3:
                self.delete_entry()
            elif key == curses.KEY_F10:
                self.save_voucher(stdscr)
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                self.handle_backspace()
            elif 32 <= key <= 126:  # 可列印字元
                self.handle_input(chr(key))

    def move_up(self):
        """上移欄位"""
        self.current_field = max(0, self.current_field - 1)

    def move_down(self):
        """下移欄位"""
        self.current_field = min(2, self.current_field + 1)

    def move_left(self):
        """左移欄位 (僅在明細區)"""
        self.current_col = max(0, self.current_col - 1)

    def move_right(self):
        """右移欄位 (僅在明細區)"""
        self.current_col = min(4, self.current_col + 1)

    def draw_screen(self, stdscr):
        """繪製整個畫面"""
        stdscr.clear()
        stdscr.addstr(1, 2, "Voucher Entry (F1 離開)")
        stdscr.addstr(3, 2, f"voucher_no   : {self.voucher_no}")
        stdscr.addstr(4, 2, f"voucher_date : {self.voucher_date}")
        stdscr.addstr(5, 2, f"description  : {self.description}")
        stdscr.refresh()

    def add_entry(self):
        self.entries.append({})

    def delete_entry(self):
        if self.entries:
            self.entries.pop()

    def save_voucher(self, stdscr):
        # 先做最小可執行版本，避免 AttributeError
        pass

    def handle_backspace(self):
        if self.current_field == 0 and self.voucher_no:
            self.voucher_no = self.voucher_no[:-1]
        elif self.current_field == 1 and self.voucher_date:
            self.voucher_date = self.voucher_date[:-1]
        elif self.current_field == 2 and self.description:
            self.description = self.description[:-1]

    def handle_input(self, char):
        if self.current_field == 0:
            self.voucher_no += char
        elif self.current_field == 1:
            self.voucher_date += char
        elif self.current_field == 2:
            self.description += char


def main():
    """主程式進入點"""
    app = VoucherEntry()
    curses.wrapper(app.run)


if __name__ == "__main__":
    main()