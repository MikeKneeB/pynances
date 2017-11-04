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

    def modify_amount(self, new_amount):
        self.amount = new_amount

    def modify_label(self, new_label):
        self.label = new_label

class Finances:

    def __init__(self, name = None):
        self.money_items = {}
        self.next_key = 0
        self.year_budget = 0
        self.name = name

    def add_item(self, new_item, key = None):
        if key is not None:
            self.next_key = int(key)
        if self.next_key in self.money_items.keys():
            self.next_key = max(self.money_items.keys()) + 1
        self.money_items[self.next_key] = new_item
        self.next_key += 1

    def calculate_yearly(self):
        budget = 0
        for key in self.money_items:
            item = self.money_items[key]
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
        for key in self.money_items:
            item = self.money_items[key]
            print('({}) {}'.format(key, item.label))
            print('\tAmount: {:.2f}'.format(item.amount))
            if item.repeats:
                print('\tEvery: {}'.format(item.repeat_period))
            print()
        print('Monthly budget: {:.2f}'.format(self.calculate_monthly()))
        print('Weekly budget: {:.2f}'.format(self.calculate_weekly()))

def load_from_xml(xml_file, finances):
    xtree = ET.parse(xml_file)
    xroot = xtree.getroot()
    finances.name = xroot.attrib['name']
    for child in xroot:
        money_item_dict = {}
        money_item_dict['key'] = int(child.attrib['key'])
        for subchild in child:
            money_item_dict[subchild.tag] = subchild.text
        finances.add_item(MoneyItem(money_item_dict['amount'],
                            money_item_dict['repeats'],
                            money_item_dict['repeat_period'],
                            money_item_dict['label']), money_item_dict['key'])

def load_from_yaml(yaml_file, finances):
    with open(yaml_file, 'r') as _file:
        yaml_obj = yaml.load(_file)
    if len(yaml_obj.keys()) != 1:
        print('This doesn\'t look right.')
    else:
        finances.name = list(yaml_obj.keys())[0]
        for key, item in yaml_obj[finances.name].items():
            id_no = int(key)
            amount = item['amount']
            repeats = item['repeats']
            repeat_period = item['repeat_period']
            label = item['label']
            finances.add_item(MoneyItem(amount, repeats, repeat_period, label), id_no)

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
    for key, item in finances.money_items.items():
        yaml_obj[finances.name][str(key)] = {'amount': item.amount,
                                            'repeats': item.repeats,
                                            'repeat_period': item.repeat_period,
                                            'label': item.label}
    with open(yaml_file, 'w') as _file:
        _file.write(yaml.dump(yaml_obj))
