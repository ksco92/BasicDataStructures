class Node:

    def __init__(self, value):
        self.value = value
        self.next_node = None

    def set_next(self, node):
        self.next_node = node

    def __str__(self):
        return '{value: ' + str(self.value) + ', next_node: ' + str(self.next_node) + '}'
