import flet as ft


def enable_element(element) -> None:
    """
    Enable a single element and uses the Attribute avail_color to set the Icon Color... if don't have the attribute set, or if it is None, will set the element icon_color to Primary Color
    :param element: Element to be set as enabled
    """
    element.disabled = False

    if hasattr(element, 'avail_color') and element.avail_color is not None:
        element.icon_color = element.avail_color
    else:
        element.icon_color = ft.colors.PRIMARY

    element.page.update()


def enable_element_list(elements_list: list) -> None:
    """
    Enable a list of elements and uses the Attribute avail_color to set the Icon Color... if don't have the attribute set, or if it is None, will set the element icon_color to Primary Color
    :param elements_list: Element List to be set as enabled
    """

    for element in elements_list:
        element.disabled = False

        if hasattr(element, 'avail_color') and element.avail_color is not None:
            element.icon_color = element.avail_color
        else:
            element.icon_color = ft.colors.PRIMARY
        element.page.update()


def disable_element(element) -> None:
    """
    Disable a single element and set the current color to the Attribute avail_color, the attribute will be used later to enable item with the same color as before
    :param element: Element to be set as disabled
    """
    element.disabled = True

    if not hasattr(element, 'avail_color') or element.avail_color is None:
        element.avail_color = element.icon_color

    element.icon_color = 'black400'
    element.page.update()


def disable_element_list(elements_list: list) -> None:
    """
    Disable a list of elements and set the current color to the Attribute avail_color, the attribute will be used later to enable item with the same color as before
    :param elements_list: Element List to be set as disabled
    """
    for element in elements_list:
        element.disabled = True

        if not hasattr(element, 'avail_color') or element.avail_color is None:
            element.avail_color = element.icon_color

        element.icon_color = 'black400'
        element.page.update()


def show_into_container(container,
                        element
                        ):
    container.content.controls.append(element)

