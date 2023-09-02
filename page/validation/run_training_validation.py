from page.elements.function.find_element import get_element_by_id, get_element_by_group_name, get_checked_checkbox


def run_training_validation(field_list: list):
    game_name = get_element_by_id('game_name', field_list)

    user_list = get_element_by_group_name('user_list', field_list)
    model_list = get_element_by_group_name('model_list', field_list)

    checked_users = get_checked_checkbox(user_list)
    checked_models = get_checked_checkbox(model_list)

    if game_name.value is None:
        raise Exception('Please, select a game in the list before start Recording.')
    if len(checked_users) < 2:
        raise Exception('Please, select at least two users to run the training validation.')
    if len(checked_models) < 1:
        raise Exception('Please, select at least one model to run the training validation.')
