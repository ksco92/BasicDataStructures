from models.list import List
from models.queue import Queue
from models.stack import Stack
from views import print_all_structures, invalid_selection_view, repeated_value, not_in_list
from generic_utils.exists import exists


class StructureController:

    def __init__(self):
        self.main_list = List()
        self.main_queue = Queue()
        self.main_stack = Stack()

    @staticmethod
    def add_to_structure(value, structure):
        if type(structure).__name__ == 'List':
            structure.insert_ordered(value)

        elif type(structure).__name__ == 'Stack':
            structure.push(value)

        elif type(structure).__name__ == 'Queue':
            structure.receive(value)

        else:
            raise ValueError('Provided structure has an invalid type.')

    @staticmethod
    def remove_from_structure(structure, value=None):
        if type(structure).__name__ == 'List' and value:
            pass

        elif type(structure).__name__ == 'Stack' and not value:
            return structure.pop(value)

        elif type(structure).__name__ == 'Queue' and not value:
            structure.send()

    @staticmethod
    def is_selection_valid(selection):
        try:
            int(selection)
            return True
        except ValueError:
            return False

    def main_menu_selection(self, selection, extra_value=None):

        if selection == 1:
            if exists(extra_value, self.main_list):
                repeated_value()
            else:
                self.main_list.insert_ordered(extra_value)

        elif selection == 2:
            if exists(extra_value, self.main_stack):
                repeated_value()
            else:
                self.main_stack.push(extra_value)

        elif selection == 3:
            if exists(extra_value, self.main_queue):
                repeated_value()
            else:
                self.main_queue.receive(extra_value)

        elif selection == 4:
            self.main_list.remove(extra_value)

        elif selection == 5:
            self.main_list.insert_ordered(self.main_queue.send())

        elif selection == 6:
            self.main_stack.push(self.main_queue.send())

        elif selection == 7:
            self.main_list.insert_ordered(self.main_stack.pop())

        elif selection == 8:
            self.main_queue.receive(self.main_stack.pop())

        elif selection == 9:
            if not exists(extra_value, self.main_list):
                not_in_list()
            elif exists(extra_value, self.main_queue):
                repeated_value()
            else:
                self.main_list.remove(extra_value)
                self.main_queue.receive(extra_value)

        elif selection == 10:
            if not exists(extra_value, self.main_list):
                not_in_list()
            elif exists(extra_value, self.main_stack):
                repeated_value()
            else:
                self.main_list.remove(extra_value)
                self.main_stack.push(extra_value)

        elif selection == 11:
            print_all_structures(self.main_list, self.main_queue, self.main_stack)

        elif selection == 12:
            self.main_list = List()
            self.main_queue = Queue()
            self.main_stack = Stack()

        else:
            invalid_selection_view()
