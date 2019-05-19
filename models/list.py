from models.node import Node


class List:

    def __init__(self):
        self.head = None

    def insert_ordered(self, value):
        node = Node(value)

        if not self.head:
            self.head = node

        elif not self.head.next_node:
            if self.head.value < value:
                self.head.set_next(node)
            else:
                current_head = self.head
                self.head = node
                self.head.set_next(current_head)

        else:
            aux = self.head

            if aux.value > value:
                node.set_next(aux)
                self.head = node

            else:
                while aux.next_node and aux.next_node.value < value:
                    aux = aux.next_node

                next = aux.next_node
                aux.set_next(node)
                node.set_next(next)

    def insert_beginning(self, value):
        node = Node(value)

        if not self.head:
            self.head = node

        else:
            node.set_next(self.head)
            self.head = node

    def insert_end(self, value):
        node = Node(value)

        if not self.head:
            self.head = node

        elif not self.head.next_node:
            self.head.next_node = node

        else:
            aux = self.head

            while aux.next_node:
                aux = aux.next_node

            aux.set_next(node)

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
