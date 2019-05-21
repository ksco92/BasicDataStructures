from models.node import Node


class Queue:

    def __init__(self):
        self.head = None
        self.tail = None

    def receive(self, value):
        node = Node(value, next_node=None)

        if not self.head and not self.tail:
            self.head = node
            self.tail = node

        elif self.head == self.tail:
            self.head.next_node = node
            self.tail = node

        else:
            self.tail.next_node = node
            self.tail = node

    def send(self):

        if not self.head and not self.tail:
            return None

        elif self.head == self.tail:
            current_head = self.head
            self.head = None
            self.tail = None
            return current_head.value

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
