from models.node import Node


class BinarySearchTree:

    def __init__(self):
        self.root = None

    def __str__(self):
        return self.__str_recursive(self.root)

    def __str_recursive(self, node):
        main_str = '\n' + ('\t' * self.get_level(node)) + 'Value: ' + str(node.value) + '\n'

        if node.left:
            main_str += ('\t' * self.get_level(node)) + 'Left: ' + self.__str_recursive(node.left) + '\n'
        else:
            main_str += ('\t' * self.get_level(node)) + 'Left: None \n'

        if node.right:
            main_str += ('\t' * self.get_level(node)) + 'Right: ' + self.__str_recursive(node.right) + ''
        else:
            main_str += ('\t' * self.get_level(node)) + 'Right: None'

        return main_str

    @staticmethod
    def get_level(node):
        count = 0
        while node.parent:
            node = node.parent
            count += 1

        return count

    def add_element(self, value):
        if not self.root:
            self.root = Node(value, left=None, right=None, parent=None, balance_factor=0)

        else:
            self.__add_element_recursive(self.root, value)

    def __add_element_recursive(self, parent, value):
        if value > parent.value:
            if parent.right:
                self.__add_element_recursive(parent.right, value)
            else:
                node = Node(value, left=None, right=None, parent=parent, balance_factor=0)
                parent.right = node
                self.__update_balance_factor(node)
        elif parent.left:
            self.__add_element_recursive(parent.left, value)
        else:
            node = Node(value, left=None, right=None, parent=parent, balance_factor=0)
            parent.left = node
            self.__update_balance_factor(node)

    def is_empty(self):
        if not self.root:
            return True
        else:
            return False

    def height(self, node):
        if not node:
            return 0
        return max(self.height(node.left), self.height(node.right)) + 1

    def __update_balance_factor(self, node):
        if node.balance_factor < -1 or node.balance_factor > 1:
            self.__balance(node)
            return

        if node.parent:
            if node == node.parent.left:
                node.parent.balance_factor -= 1

            if node == node.parent.right:
                node.parent.balance_factor += 1

            if node.parent.balance_factor != 0:
                self.__update_balance_factor(node.parent)

    def __balance(self, node):
        if node.balance_factor > 0:
            if node.right.balance_factor < 0:
                self.right_rotate(node.right)
                self.left_rotate(node)
            else:
                self.left_rotate(node)
        elif node.balance_factor < 0:
            if node.left.balance_factor > 0:
                self.left_rotate(node.left)
                self.right_rotate(node)
            else:
                self.right_rotate(node)

    def left_rotate(self, node):
        aux = node.right
        node.right = aux.left

        if aux.left:
            aux.left.parent = node

        aux.parent = node.parent

        if not node.parent:
            self.root = aux
        elif node == node.parent.left:
            node.parent.left = aux
        else:
            node.parent.right = aux

        aux.left = node
        node.parent = aux

        node.balance_factor = node.balance_factor - 1 - max(0, aux.balance_factor)
        aux.balance_factor = aux.balance_factor - 1 + min(0, node.balance_factor)

    def right_rotate(self, node):
        aux = node.left
        node.left = aux.right

        if aux.right:
            aux.right.parent = node

        aux.parent = node.parent

        if not node.parent:
            self.root = aux
        elif node == node.parent.right:
            node.parent.right = aux
        else:
            node.parent.left = aux

        aux.right = node
        node.parent = aux

        node.balance_factor = node.balance_factor + 1 - min(0, aux.balance_factor)
        aux.balance_factor = aux.balance_factor + 1 + max(0, node.balance_factor)

    def pre_order(self):
        return self.__pre_order_recursive(self.root)

    def __pre_order_recursive(self, node):
        main_str = ''

        if node:
            main_str += str(node.value) + ' - '
            main_str += self.__pre_order_recursive(node.left)
            main_str += self.__pre_order_recursive(node.right)

        return main_str

    def in_order(self):
        return self.__in_order_recursive(self.root)

    def __in_order_recursive(self, node):
        main_str = ''

        if node:
            main_str += self.__in_order_recursive(node.left)
            main_str += str(node.value) + ' - '
            main_str += self.__in_order_recursive(node.right)

        return main_str

    def post_order(self):
        return self.__post_order_recursive(self.root)

    def __post_order_recursive(self, node):
        main_str = ''

        if node:
            main_str += self.__post_order_recursive(node.left)
            main_str += self.__post_order_recursive(node.right)
            main_str += str(node.value) + ' - '

        return main_str
