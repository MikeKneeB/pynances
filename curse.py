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

    selected_item = 0

    curses.curs_set(False)
    curses.use_default_colors()
    stdscr.clear()
    curses.init_pair(1, -1, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    stdscr.bkgd(' ', curses.color_pair(1))

    title_win = curses.newwin(curses.LINES - 5, curses.COLS - 1, 0, 0)
    display_pad = curses.newpad(curses.LINES - 1, curses.COLS - 3)
    command_win = curses.newwin(5, curses.COLS - 1, curses.LINES - 5, 0)

    command_win.border()
    stdscr.refresh()

    running = True
    while running:
        draw_title(title_win, working_finances)
        draw_finances(display_pad, working_finances, selected_item)
        draw_command(command_win, selected_item = selected_item)

        title_win.refresh()
        display_pad.refresh(0, 0, 1, 1, curses.LINES - 7, curses.COLS - 3)
        command_win.refresh()

        inp = stdscr.getkey()
        if inp is 'q':
            running = False
        elif inp == curses.KEY_DOWN or inp == 'j':
            selected_item += 1
        elif inp == curses.KEY_UP or inp == 'k':
            selected_item -= 1
    curses.curs_set(True)

def draw_title(win, finances):
    win.border()
    win.addstr(0, 1, finances.name)

def draw_finances(pad, finances, selected_item):
    line_count = 1
    for key, item in finances.money_items.items():
        if item.repeats:
            pad.addstr(line_count, 3, '({})'.format(key))
            if item.amount < 0:
                pad.addstr(' {}'.format(item.label), curses.color_pair(2))
            else:
                pad.addstr(' {}'.format(item.label), curses.color_pair(3))
            line_count += 1
            pad.addstr(line_count, 3,'\tEvery: {}'.format(item.repeat_period))
            line_count += 1
            pad.addstr(line_count, 3, '\tAmount: {:.2f}'.format(item.amount))
            line_count += 2
    pad.addstr((selected_item * 4) + 1, 1, '>')

def draw_command(win, **kwargs):
    for key, item in kwargs.items():
        win.addstr('{}:{} '.format(key, item))

if __name__ == '__main__':
    curses.wrapper(main)
