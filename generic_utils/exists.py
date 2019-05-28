from models.binary_search_tree import BinarySearchTree
from models.list import List
from models.queue import Queue
from models.stack import Stack


def exists(value, structure):
    if isinstance(structure, (List, Queue, Stack)):
        aux = structure.head

        while aux:
            if aux.value == value:
                return True
            aux = aux.next_node

        return False

    elif isinstance(structure, BinarySearchTree):
        return __exists_binary_tree_recursive(structure.root, value)


def __exists_binary_tree_recursive(node, value):
    if not node:
        return False
    elif value == node.value:
        return True
    elif value > node.value:
        return __exists_binary_tree_recursive(node.right, value)
    else:
        return __exists_binary_tree_recursive(node.left, value)
