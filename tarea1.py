from controllers import StructureController
from views import main_menu_view, add_value_view, invalid_selection_view

if __name__ == '__main__':

    controller = StructureController()

    while True:
        user_selection = main_menu_view()
        if controller.is_selection_valid(user_selection):
            user_selection = int(user_selection)
            if user_selection in (1, 2, 3, ):
                controller.main_menu_selection(user_selection, extra_value=add_value_view())
            else:
                controller.main_menu_selection(user_selection)
        else:
            invalid_selection_view()
