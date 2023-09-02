import flet as ft


def get_element_by_id(id: str,
                      element_list
                      ):
    """
    Finds an element with the informed ID
    :param id: ID of certain Elements
    :param element_list: List of Element that have to be filtered
    :return: Element with the searched ID
    """
    if isinstance(element_list, ft.Page):
        element_list = element_list.controls

    for element in element_list:
        if isinstance(element, list):
            return_value = get_element_by_id(id, element)
            if return_value is not None:
                return return_value

        if hasattr(element, 'id'):
            if element.id == id:
                return element

    return None


def get_element_by_class_name(className: str,
                              element_list
                              ):
    """
    Finds an element with the informed Class Name
    :param className: className of the Elements
    :param element_list: List of Element that have to be filtered
    :return: List of Element with the searched className
    """
    return_list = []

    if isinstance(element_list, ft.Page):
        element_list = element_list.controls

    for element in element_list:
        if isinstance(element, list):
            return_list += get_element_by_class_name(className, element)
        if hasattr(element, 'className'):
            if element.className == className:
                return_list.append(element)

    return return_list


def get_element_by_group_name(groupName: str,
                              element_list
                              ):
    """
    Finds an element with the informed Group Name
    :param groupName: Group Name of the Elements
    :param element_list: List of Element that have to be filtered
    :return: List of Element with the searched groupName
    """
    return_list = []

    if isinstance(element_list, ft.Page):
        element_list = element_list.controls

    for element in element_list:
        if isinstance(element, list):
            return_list += get_element_by_group_name(groupName, element)
        if hasattr(element, 'groupName'):
            if element.groupName == groupName:
                return_list.append(element)
    return return_list


def get_element_by_element_type(element_type: object,
                                element_list
                                ):
    """
    Finds an element with the informed Element Type
    :param element_type: Element Type of the Elements. EX: ft.Switch
    :param element_list: List of Element that have to be filtered
    :return: List of Element with the searched element_type
    """

    return_list = []

    if isinstance(element_list, ft.Page):
        element_list = element_list.controls

    for element in element_list:
        if isinstance(element, list):
            return_list += get_element_by_element_type(element_type, element)
        if type(element) == list:
            get_element_by_element_type(element_type, element)
        if hasattr(element, 'className'):
            if isinstance(element, element_type):
                return_list.append(element)

    return return_list


def get_checked_checkbox(checkbox_list: list):
    """
    Filter every Checked checkbox on the list
    :param checkbox_list: List of checkbox group
    :return: List of checkbox elements that are set to True (checked)
    """
    return [checked for checked in checkbox_list if checked.value]


def get_unchecked_checkbox(checkbox_list: list):
    """
    Filter every Unchecked checkbox on the list
    :param checkbox_list: List of checkbox group
    :return: List of checkbox elements that are set to False (unchecked)
    """
    return [checked for checked in checkbox_list if not checked.value]
