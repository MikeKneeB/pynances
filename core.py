class MoneyItem:

    def __init__(self, amount = 0, repeats = false, repeat_period = None, label = ""):
        self.amount = amount
        self.repeats = repeats
        self.repeat_period = repeat_period
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

    def add_item(self, new_item):
        self.money_items[next_key] = new_item
        self.next_key++

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
        return calculate_yearly(self)/12

    def calculate_weekly(self):
        return calculate_yearly(self)/52

    def update(self):
        self.year_budget = self.calculate_yearly()
