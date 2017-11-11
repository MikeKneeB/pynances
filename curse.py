import core
import os, curses, argparse

parser = argparse.ArgumentParser(description = 'REEEE')
parser.add_argument('finance_file', type = str, nargs = '?',
                    help = 'File location for an exisitng finances file.')

def main(stdscr):
    args = parser.parse_args()
    working_finances = core.Finances()
    if args.finance_file is not None:
        core.load_from_yaml(args.finance_file, working_finances)
        working_finances.update()
    else:
        return
    curses.curs_set(False)
    curses.use_default_colors()
    curses.init_pair(1, -1, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    curses.init_pair(4, -1, curses.COLOR_BLACK)
    curses.init_pair(5, -1, curses.COLOR_BLUE)
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))
    display_window = DisplayWindow(working_finances)
    command_window = CommandWindow()
    stdscr.refresh()
    running = True
    while running:
        display_window.draw_title()
        display_window.draw_finances()
        display_window.draw_budget()
        command_window.draw_commands()
        inp = stdscr.getkey()
        if inp is 'q':
            running = False
        elif inp == 'KEY_DOWN' or inp == 'j':
            display_window.increment_selection()
            display_window.draw_finances()
        elif inp == 'KEY_UP' or inp == 'k':
            display_window.decrement_selection()
            display_window.draw_finances()

class DisplayWindow(object):

    def __init__(self, finances):
        self.title_win = curses.newwin(curses.LINES - 5, curses.COLS, 0, 0)
        self.title_win.border()
        self.middle = int(curses.COLS / 2)
        for i in range(1, curses.LINES - 6):
            self.title_win.addch(i, self.middle, curses.ACS_VLINE)
        self.title_win.addch(0, self.middle, curses.ACS_TTEE)
        self.title_win.addch(curses.LINES - 6, self.middle, curses.ACS_BTEE)
        self.finances = finances
        self.recurring_display_pad = curses.newpad(len(self.finances.money_items) * 4, self.middle - 1)
        self.recurring_display_pad.bkgd(' ', curses.color_pair(4))
        self.spending_display_pad = curses.newpad(10, self.middle - 1)
        self.spending_display_pad.bkgd(' ', curses.color_pair(5))
        self.selected_index = 0

    def draw_title(self):
        self.title_win.addstr(0, 1, self.finances.name)
        self.title_win.refresh()

    def draw_finances(self):
        line_count = 1
        for key, item in enumerate(self.finances.money_items):
            if item.repeats:
                if key == self.selected_index:
                    self.recurring_display_pad.addstr(line_count, 1, '> ({})'.format(key))
                else:
                    self.recurring_display_pad.addstr(line_count, 1, '  ({})'.format(key))
                if item.amount < 0:
                    self.recurring_display_pad.addstr(' {}'.format(item.label), curses.color_pair(2))
                else:
                    self.recurring_display_pad.addstr(' {}'.format(item.label), curses.color_pair(3))
                line_count += 1
                self.recurring_display_pad.addstr(line_count, 3,'\tEvery:\t{}'.format(item.repeat_period))
                line_count += 1
                self.recurring_display_pad.addstr(line_count, 3, '\tAmount:\t{:.2f}'.format(item.amount))
                line_count += 2
        self.recurring_display_pad.refresh(0, 0, 1, 1, curses.LINES - 7, curses.COLS - 3)

    def draw_budget(self):
        self.spending_display_pad.refresh(0, 0, 1, self.middle + 1, curses.LINES - 7, curses.COLS - 3)

    def increment_selection(self):
        if self.selected_index == len(self.finances.money_items) - 1:
            pass
        else:
            self.selected_index += 1

    def decrement_selection(self):
        if self.selected_index == 0:
            pass
        else:
            self.selected_index -= 1

class CommandWindow(object):

    def __init__(self):
        self.command_win = curses.newwin(5, curses.COLS - 1, curses.LINES - 5, 0)
        self.command_win.border()
        self.command_page = 0

    def draw_commands(self):
        self.command_win.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
