import core
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    my_fin = core.Finances()
    xtree = ET.parse('finance_ex.xml')
    xroot = xtree.getroot()
    for child in xroot:
        money_item_dict = {}
        money_item_dict['key'] = int(child.attrib['key'])
        for subchild in child:
            money_item_dict[subchild.tag] = subchild.text
        my_fin.add_item(core.MoneyItem(money_item_dict['amount'],
                                        money_item_dict['repeats'],
                                        money_item_dict['repeat_period'],
                                        money_item_dict['label']), money_item_dict['key'])
    my_fin.print_summary()
