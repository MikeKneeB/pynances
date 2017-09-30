import core

import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser(description = 'REEEE')
parser.add_argument('finance_file', type = str, nargs = '?',
                    help = 'File location for an exisitng finances file.')

def load_from_xml(xml_file, finances):
    xtree = ET.parse(xml_file)
    xroot = xtree.getroot()
    for child in xroot:
        money_item_dict = {}
        money_item_dict['key'] = int(child.attrib['key'])
        for subchild in child:
            money_item_dict[subchild.tag] = subchild.text
        finances.add_item(core.MoneyItem(money_item_dict['amount'],
                            money_item_dict['repeats'],
                            money_item_dict['repeat_period'],
                            money_item_dict['label']), money_item_dict['key'])

def write_to_xml(xml_file, finances):
    pass

def add_to_finances(finances):
    label = input('\nPlease enter a label for the new item: ')
    amount = get_float(text = 'Please enter an amount in pounds: ')
    repeats = False if input('Enter "n" for no repeat, anything else for repeating: ') == 'n' else True
    if repeats = True:
        repeat_period = get_repeat_period()
    else:
        repeat_period = None
    new_item = Item(amount, repeats, repeat_period, label)
    finances.add_item(new_item)

def remove_from_finances(finances):
    pass

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
            if period == 'y'
                period = 'year'
            elif period == 'm':
                period = 'month'
            elif period == 'w':
                period == 'week'
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


if __name__ == '__main__':
    args = parser.parse_args()
    working_finances = core.Finances()
    if args.finance_file is not None:
        load_from_xml(args.finance_file, working_finances)
        working_finances.update()
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
                    write_to_xml(args.finance_file, working_finances)
                else:
                    working_finances = working_finances_temp
            elif choice == 2:
                remove_from_finances(working_finances)
            elif choice == 3:
                running = False
    else:
        pass
