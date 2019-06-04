class Node:

    def __init__(self, value, **kwargs):
        self.value = value

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        main_str = '{value: ' + str(self.value)
        for attribute in [a for a in dir(self) if not a.startswith('__') and a not in ('value', 'parent',
                                                                                       'balance_factor')]:
            main_str += ', ' + str(attribute) + ': ' + str(getattr(self, attribute))
        main_str += '}'

        return main_str
