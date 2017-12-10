import core
import os, curses, argparse, math

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
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, -1, curses.COLOR_BLACK)
    curses.init_pair(6, -1, curses.COLOR_BLUE)
    stdscr.clear()
    stdscr.bkgd(' ', curses.color_pair(1))
    display_window = DisplayWindow(working_finances)
    command_window = CommandWindow(working_finances)
    stdscr.refresh()
    running = True
    while running:
        display_window.draw_title()
        display_window.draw_finances()
        display_window.draw_budget()
        command_window.make_command_pages()
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

def round_to_factor(x, base):
    return int(base * math.floor(x/base))

class DisplayWindow(object):

    def __init__(self, finances):
        self.title_win = curses.newwin(curses.LINES - 4, curses.COLS, 0, 0)
        self.title_win.border()
        self.middle = int(curses.COLS / 2)
        for i in range(1, curses.LINES - 5):
            self.title_win.addch(i, self.middle, curses.ACS_VLINE)
        self.title_win.addch(0, self.middle, curses.ACS_TTEE)
        self.title_win.addch(curses.LINES - 5, self.middle, curses.ACS_BTEE)
        self.title_win.addch(curses.LINES - 5, 0, curses.ACS_LTEE)
        self.title_win.addch(curses.LINES - 5, curses.COLS - 2, curses.ACS_RTEE)
        self.finances = finances
        self.finance_display_pad = curses.newpad(len(self.finances.money_items) * 4, self.middle - 1)
        self.budget_display_pad = curses.newpad(20, self.middle - 1)
        self.selected_index = 0
        self.top_of_page = 0
        self.bottom_of_page = self.top_of_page + curses.LINES - 6

    def draw_title(self):
        self.title_win.addstr(0, 1, self.finances.name)
        self.title_win.refresh()

    def draw_finances(self):
        line_count = 1
        for key, item in enumerate(self.finances.money_items):
            if item.repeats and not item.hidden:
                if key == self.selected_index:
                    self.finance_display_pad.addstr(line_count, 1, '> ({})'.format(key))
                else:
                    self.finance_display_pad.addstr(line_count, 1, '  ({})'.format(key))
                if item.amount < 0:
                    self.finance_display_pad.addstr(' {}'.format(item.label), curses.color_pair(2))
                else:
                    self.finance_display_pad.addstr(' {}'.format(item.label), curses.color_pair(3))
                line_count += 1
                self.finance_display_pad.addstr(line_count, 3,'\tEvery:\t{}'.format(item.repeat_period))
                line_count += 1
                self.finance_display_pad.addstr(line_count, 3, '\tAmount:\t{:.2f}'.format(item.amount))
                line_count += 2
        if (self.selected_index + 1) * 4 > self.bottom_of_page:
            self.top_of_page += 4
            self.bottom_of_page += 4
        elif (self.selected_index) * 4 < self.top_of_page:
            self.top_of_page -= 4
            self.bottom_of_page -= 4
        self.finance_display_pad.refresh(self.top_of_page, 0, 1, 1, round_to_factor(curses.LINES - 6, 4), curses.COLS - 3)

    def draw_budget(self):
        self.budget_display_pad.addstr(1, 2, 'Monthly Budget: ', curses.A_BOLD)
        self.budget_display_pad.addstr('{:.2f}'.format(self.finances.calculate_monthly()))
        self.budget_display_pad.addstr(3, 2, 'Weekly Budget: ', curses.A_BOLD)
        self.budget_display_pad.addstr('{:.2f}'.format(self.finances.calculate_weekly()))
        self.budget_display_pad.refresh(0, 0, 1, self.middle + 1, curses.LINES - 5, curses.COLS - 3)

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

    def __init__(self, finances):
        self.command_win = curses.newwin(5, curses.COLS, curses.LINES - 5, 0)
        self.command_win.border(0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_RTEE, 0, 0)
        self.command_win.addch(0, int(curses.COLS / 2), curses.ACS_BTEE)
        self.command_page = 0
        self.commands_per_line = 0
        self.commands_per_page = 0
        self.number_of_command_pages = 0
        self._commands_finance = (('  a ', 'add'), ('  d ', 'delete'), ('  l ', 'load'),
                        ('  s ', 'save'), ('  n ', 'new'), ('TAB ', 'change view'),
                        ('  k ', 'up'), ('  j ', 'down'), ('  h ', 'hidden'))
        self._commands_budget = ()
        self._commands = self._commands_finance
        self._command_width = 15
        self.selected_screen = 0

    def draw_commands(self):
        start = self.command_page * self.commands_per_page
        for i in range(start, start + self.commands_per_page):
            x = ((i - start) * self._command_width) % (self.commands_per_line * self._command_width)
            y = (i - start) // self.commands_per_line
            if i < len(self._commands):
                self.command_win.addstr(y + 1, x + 1, self._commands[i][0], curses.color_pair(4))
                self.command_win.addstr('{:<12}'.format(self._commands[i][1]))
        self.command_win.addstr(3, curses.COLS - 6, '< {} >'.format(self.command_page))
        self.command_win.refresh()

    def make_command_pages(self):
        self.commands_per_line = int((curses.COLS - 2) / self._command_width)
        self.commands_per_page = self.commands_per_line * 2
        self.number_of_command_pages = len(self._commands) // self.commands_per_page

    def change_selection(self):
        self.selected_screen = (self.selected_screen + 1) % 2
        if self.selected_screen == 0:
            self._commands = self._commands_finance
        elif self.selected_screen == 1:
            self._commands = self._commands_budget
        self.command_page = 0

if __name__ == '__main__':
    curses.wrapper(main)
