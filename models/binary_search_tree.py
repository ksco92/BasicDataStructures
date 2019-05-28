from models.node import Node


class BinarySearchTree:

    def __init__(self):
        self.root = None

    def __str__(self):
        return str(self.root)

    def add_element(self, value):
        node = Node(value, left=None, right=None)

        if not self.root:
            self.root = node

        else:
            self.__add_element_recursive(self.root, value)

    def __add_element_recursive(self, parent, value):
        if value > parent.value:
            if parent.right:
                self.__add_element_recursive(parent.right, value)
            else:
                parent.right = Node(value, left=None, right=None)
        elif parent.left:
            self.__add_element_recursive(parent.left, value)
        else:
            parent.left = Node(value, left=None, right=None)

    # ask about this condition
    def is_leaf(self):
        if not self.root or not self.root.left or not self.root.right:
            return False
        else:
            return True

    def is_empty(self):
        if not self.root:
            return True
        else:
            return False