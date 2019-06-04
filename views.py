def main_menu_view():
    print('#####################################################')
    print('#####################################################')
    print('#####################################################')
    print('#####################################################')
    print('#####################################################')
    print('#####################################################')
    print('1. Add an element to the list.')
    print('2. Add an element to the stack.')
    print('3. Add an element to the queue.')
    print('4. Delete an element from a list.')
    print('5. Move element from the queue to the list.')
    print('6. Move element from the queue to the stack.')
    print('7. Move element from the stack to the list.')
    print('8. Move element from the stack to the queue.')
    print('9. Move element from list to queue.')
    print('10. Move element from list to stack.')
    print('11. Add an element to the tree.')
    print('12. Show tree orders.')
    print('13. Print all structures.')
    print('14. Reset all structures.')
    return input('Select an option: ')


def not_in_list():
    print('The selected element is not in the list.')


def move_value_view():
    return input('Type the value you want to move: ')


def add_value_view():
    return input('Type the value you want to add: ')


def remove_value_view():
    return input('Type the value you want to remove: ')


def invalid_selection_view():
    print('Invalid selection, please choose an option from the menu.')


def print_all_structures(list, queue, stack, tree):
    print('List: ' + str(list))
    print('Queue: ' + str(queue))
    print('Stack: ' + str(stack))
    print('Tree: ' + str(tree))


def repeated_value():
    print('That value already exists in the selected structure, values can\'t be repeated.')


def print_tree_orders(tree):
    print('Pre-Order: ' + tree.pre_order())
    print('Post-Order: ' + tree.post_order())
    print('In-Order: ' + tree.in_order())


def int_only_tree_error():
    print('This tree supports only integers.')
