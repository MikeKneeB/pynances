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

    def __init__(self):
        self.money_items = {}
        self.next_key = 0
        self.year_budget = 0
        self.name = None

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
