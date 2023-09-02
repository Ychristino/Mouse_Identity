from page.elements.function.find_element import get_element_by_id


def start_record_validation(field_list: list):
    is_main_user = get_element_by_id('is_main_user', field_list)
    user_name = get_element_by_id('user_name', field_list)
    game_name = get_element_by_id('game_name', field_list)

    if not is_main_user.value:
        if user_name.value is None or user_name.value.strip() == "":
            raise Exception('Non main Users should inform an Unique UserName.')
    if game_name.value is None:
        raise Exception('Please, select a game in the list before start Recording.')

