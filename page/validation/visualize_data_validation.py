from page.elements.function.find_element import get_element_by_id


def generate_graph_validation(field_list: list):
    game_name = get_element_by_id('game_name', field_list)
    graph_type = get_element_by_id('graph_type', field_list)

    if game_name.value is None:
        raise Exception('Please, select a game in the list before start Recording.')
    if graph_type.value is None:
        raise Exception('Please, select a Graph type in the list to plot.')
