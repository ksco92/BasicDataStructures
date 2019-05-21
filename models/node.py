class Node:

    def __init__(self, value, **kwargs):
        self.value = value
        self.kwargs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        main_str = '{value: ' + str(self.value)
        for key, value in self.kwargs.items():
            main_str += ', ' + str(key) + ': ' + str(value)

        return main_str
