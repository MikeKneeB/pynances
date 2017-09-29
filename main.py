import core

import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser(description = 'REEEE')
parser.add_argument('finance_file', type = str, nargs = '?',
                    help = 'File location for an exisitng finances file.')

if __name__ == '__main__':
    args = parser.parse_args()
    working_finances = core.Finances()
    if args.finance_file is not None:
        xtree = ET.parse(args.finance_file)
        xroot = xtree.getroot()
        for child in xroot:
            money_item_dict = {}
            money_item_dict['key'] = int(child.attrib['key'])
            for subchild in child:
                money_item_dict[subchild.tag] = subchild.text
            working_finances.add_item(core.MoneyItem(money_item_dict['amount'],
                                        money_item_dict['repeats'],
                                        money_item_dict['repeat_period'],
                                        money_item_dict['label']), money_item_dict['key'])
        working_finances.print_summary()
    else:
        pass
