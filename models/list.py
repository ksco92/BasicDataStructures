from models.node import Node


class List:

    def __init__(self):
        self.head = None

    def remove(self, value):
        aux = self.head
        while aux:
            if aux.value == value:
                if aux == self.head:
                    self.head = aux.next_node
                    return
                else:
                    previous = self.head
                    while previous.next_node != aux:
                        previous = previous.next_node
                    previous.next_node = aux.next_node
                    return

            else:
                aux = aux.next_node

    def insert_ordered(self, value):
        node = Node(value, next_node=None)

        if not self.head:
            self.head = node

        elif not self.head.next_node:
            if self.head.value < value:
                self.head.next_node = node
            else:
                current_head = self.head
                self.head = node
                self.head.next_node = current_head

        else:
            aux = self.head

            if aux.value > value:
                node.next_node = aux
                self.head = node

            else:
                while aux.next_node and aux.next_node.value < value:
                    aux = aux.next_node

                next = aux.next_node
                aux.next_node = node
                node.next_node = next

    def insert_beginning(self, value):
        node = Node(value, next_node=None)

        if not self.head:
            self.head = node

        else:
            node.next_node = self.head
            self.head = node

    def insert_end(self, value):
        node = Node(value, next_node=None)

        if not self.head:
            self.head = node

        elif not self.head.next_node:
            self.head.next_node = node

        else:
            aux = self.head

            while aux.next_node:
                aux = aux.next_node

            aux.next_node = node

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
