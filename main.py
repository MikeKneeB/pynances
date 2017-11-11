import core

import argparse, os

parser = argparse.ArgumentParser(description = 'REEEE')
parser.add_argument('finance_file', type = str, nargs = '?',
                    help = 'File location for an exisitng finances file.')

def add_to_finances(finances):
    label = input('\nPlease enter a label for the new item: ')
    amount = get_float(text = 'Please enter an amount in pounds: ')
    repeats = False if input('Enter "n" for no repeat, anything else for repeating: ') == 'n' else True
    if repeats:
        repeat_period = get_repeat_period()
    else:
        repeat_period = None
    new_item = core.MoneyItem(amount, repeats, repeat_period, label)
    finances.add_item(new_item)

def remove_from_finances(finances):
    choice = None
    while choice is None:
        try:
            choice = int(input('Please enter the key number of the item you wish to remove: '))
        except Exception as e:
            print('Please make a valid choice.')
            choice = None
        if choice not in range(len(finances.money_items))s:
            choice = None
            print('Please make a valid choice.')
    finances.money_items.pop(choice)

def menu_choice(up_to):
    choice = None
    while choice is None:
        try:
            choice = int(input('Please make a choice: '))
        except Exception as e:
            print('Please make a valid choice.')
            choice = None
        if choice < 1 or choice > up_to:
            choice = None
            print('Please make a valid choice.')
    return choice

def get_repeat_period():
    period = None
    while period is None:
        try:
            period = input('Please enter y, m or w for yearly repeat, monthly repeat or weekly repeat: ')
            if period == 'y':
                period = 'year'
            elif period == 'm':
                period = 'month'
            elif period == 'w':
                period = 'week'
            else:
                print('Please enter a valid option.')
                period = None
        except Exception as e:
            print('Please enter a valid options.')
            period = None
    return period

def get_float(text = None):
    flo = None
    while flo is None:
        try:
            flo = float(input('Please enter a float: ' if text is None else text))
        except Exception as e:
            print('Please enter a valid float.')
            flo = None
    return flo

def main_loop(working_finances, file_name):
    running = True
    while running:
        working_finances.print_summary()
        print('\nWhat would you like to do?')
        print('\t(1) Add finance item')
        print('\t(2) Remove finance item')
        print('\t(3) Quit')
        choice = menu_choice(3)
        if choice == 1:
            working_finances_temp = working_finances
            add_to_finances(working_finances)
            working_finances.update()
            working_finances.print_summary()
            print('\nEnter 1 to save changes, 2 to discard.')
            choice = menu_choice(2)
            if choice == 1:
                core.write_to_yaml(file_name, working_finances)
            else:
                working_finances = working_finances_temp
        elif choice == 2:
            working_finances_temp = working_finances
            remove_from_finances(working_finances)
            working_finances.update()
            working_finances.print_summary()
            print('\nEnter 1 to save changes, 2 to discard.')
            choice = menu_choice(2)
            if choice == 1:
                core.write_to_yaml(file_name, working_finances)
            else:
                working_finances = working_finances_temp
        elif choice == 3:
            running = False

if __name__ == '__main__':
    args = parser.parse_args()
    working_finances = core.Finances()
    if args.finance_file is not None:
        core.load_from_yaml(args.finance_file, working_finances)
        working_finances.update()
        main_loop(working_finances, args.finance_file)
    else:
        running = True
        while running:
            print('What would you like to do?')
            print('\t(1) Create new finances file')
            print('\t(2) Load finances file')
            print('\t(3) Quit')
            choice = menu_choice(3)
            if choice == 1:
                new_name = input('\nPlease enter a new name for the finances: ')
                working_finances = core.Finances(name = new_name)
                file_name = str(new_name.replace(' ', '_') + '.yaml')
                with open(file_name, 'a'):
                    os.utime(file_name)
                working_finances.update()
                main_loop(working_finances, file_name)
            elif choice == 2:
                file_name = str(input('\nPlease enter the file name for the finances file: '))
                working_finances = core.Finances()
                try:
                    core.load_from_yaml(file_name, working_finances)
                    working_finances.update()
                    main_loop(working_finances, file_name)
                except FileNotFoundError as e:
                    print('No such file.')
            elif choice == 3:
                running = False
