import xml.etree.ElementTree as ET
import yaml

class MoneyItem:

    def __init__(self, amount = 0, repeats = False, repeat_period = None, label = ''):
        self.amount = float(amount)
        self.repeats = bool(repeats)
        if self.repeats:
            self.repeat_period = repeat_period
        else:
            self.repeat_period = None
        self.label = label

class Finances:

    def __init__(self, name = None):
        self.money_items = []
        self.year_budget = 0
        self.name = name

    def add_item(self, new_item):
        self.money_items.append(new_item)

    def remove_item(self, index):
        self.money_items.pop(index)

    def calculate_yearly(self):
        budget = 0
        for item in self.money_items:
            if item.repeats:
                if item.repeat_period == 'day':
                    budget += item.amount*365
                elif item.repeat_period == 'week':
                    budget += item.amount*52
                elif item.repeat_period == 'month':
                    budget += item.amount*12
                elif item.repeat_period == 'year':
                    budget += item.amount
        return budget

    def calculate_monthly(self):
        return self.calculate_yearly()/12

    def calculate_weekly(self):
        return self.calculate_yearly()/52

    def update(self):
        self.year_budget = self.calculate_yearly()

    def print_summary(self):
        for key, item in enumerate(self.money_items):
            print('({}) {}'.format(key, item.label))
            print('\tAmount: {:.2f}'.format(item.amount))
            if item.repeats:
                print('\tEvery: {}'.format(item.repeat_period))
            print()
        print('Monthly budget: {:.2f}'.format(self.calculate_monthly()))
        print('Weekly budget: {:.2f}'.format(self.calculate_weekly()))

    def string_summary(self):
        ret_str = ''
        for key, item in enumerate(self.money_items):
            item = self.money_items[key]
            ret_str += '({}) {}\n'.format(key, item.label)
            ret_str += '\tAmount: {:.2f}\n'.format(item.amount)
            if item.repeats:
                ret_str += '\tEvery: {}\n\n'.format(item.repeat_period)
        ret_str += 'Monthly budget: {:.2f}\n'.format(self.calculate_monthly())
        ret_str += 'Weekly budget: {:.2f}'.format(self.calculate_weekly())
        return ret_str

def load_from_yaml(yaml_file, finances):
    with open(yaml_file, 'r') as _file:
        yaml_obj = yaml.load(_file)
    if len(yaml_obj.keys()) != 1:
        print('This doesn\'t look right.')
    else:
        finances.name = list(yaml_obj.keys())[0]
        for key, item in yaml_obj[finances.name].items():
            amount = item['amount']
            repeats = item['repeats']
            repeat_period = item['repeat_period']
            label = item['label']
            finances.add_item(MoneyItem(amount, repeats, repeat_period, label))

def write_to_xml(xml_file, finances):
    xroot = ET.Element('finance', attrib = {'name': finances.name})
    for key in finances.money_items.keys():
        temp_element = ET.Element('item', attrib = {'key': str(key)})
        temp_sub_element = ET.Element('amount')
        temp_sub_element.text = str(finances.money_items[key].amount)
        temp_element.append(temp_sub_element)
        temp_sub_element = ET.Element('repeats')
        temp_sub_element.text = str(finances.money_items[key].repeats)
        temp_element.append(temp_sub_element)
        temp_sub_element = ET.Element('repeat_period')
        temp_sub_element.text = str(finances.money_items[key].repeat_period)
        temp_element.append(temp_sub_element)
        temp_sub_element = ET.Element('label')
        temp_sub_element.text = str(finances.money_items[key].label)
        temp_element.append(temp_sub_element)
        xroot.append(temp_element)
    xtree = ET.ElementTree(element = xroot)
    xtree.write(xml_file)

def write_to_yaml(yaml_file, finances):
    yaml_obj = {}
    yaml_obj[finances.name] = {}
    for key, item in enumerate(finances.money_items):
        yaml_obj[finances.name][str(key)] = {'amount': item.amount,
                                            'repeats': item.repeats,
                                            'repeat_period': item.repeat_period,
                                            'label': item.label}
    with open(yaml_file, 'w') as _file:
        _file.write(yaml.dump(yaml_obj))
