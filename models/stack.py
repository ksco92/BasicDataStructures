from models.node import Node


class Stack:

    def __init__(self):
        self.head = None

    def push(self, value):
        node = Node(value, next_node=None)

        if not self.head:
            self.head = node

        else:
            old_head = self.head
            self.head = node
            self.head.next_node = old_head

    def pop(self):

        if not self.head:
            return None

        else:
            current_head = self.head
            self.head = current_head.next_node
            return current_head.value

    def __str__(self):
        displayed = '['

        if self.head:
            displayed += str(self.head.value) + ', '
            aux = self.head

            while aux.next_node:
                displayed += str(aux.next_node.value) + ', '
                aux = aux.next_node

        displayed += ']'

        return displayed
