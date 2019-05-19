def main_menu_view():
    print('1. Add an element to the list.')
    print('2. Add an element to the stack.')
    print('3. Add an element to the queue.')
    print('4. Delete an element from a list.')
    print('5. Move element from the queue to the list.')
    print('6. Move element from the queue to the stack.')
    print('7. Move element from the stack to the list.')
    print('8. Move element from the stack to the queue.')
    print('9. Print all structures.')
    print('10. Reset all structures.')
    return input('Select an option: ')


def add_value_view():
    return input('Type the value you want to add: ')


def invalid_selection_view():
    print('Invalid selection, please choose an option from the menu.')


def print_all_structures(list, queue, stack):
    print('List: ' + str(list))
    print('Queue: ' + str(queue))
    print('Stack: ' + str(stack))
