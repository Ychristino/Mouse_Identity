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


def update_barchart(barchart: ft.BarChart,
                    new_barchart: ft.BarChart
                    ) -> ft.BarChart:
    barchart.bar_groups = new_barchart.bar_groups
    barchart.groups_space = new_barchart.groups_space
    barchart.animate = new_barchart.animate
    barchart.interactive = new_barchart.interactive
    barchart.bgcolor = new_barchart.bgcolor
    barchart.tooltip_bgcolor = new_barchart.tooltip_bgcolor
    barchart.border = new_barchart.border
    barchart.horizontal_grid_lines = new_barchart.horizontal_grid_lines
    barchart.vertical_grid_lines = new_barchart.vertical_grid_lines
    barchart.left_axis = new_barchart.left_axis
    barchart.right_axis = new_barchart.right_axis
    barchart.top_axis = new_barchart.top_axis
    barchart.bottom_axis = new_barchart.bottom_axis
    barchart.min_y = new_barchart.min_y
    barchart.max_y = new_barchart.max_y

    return barchart


def remove_element(elements_list: list) -> None:
    """
    Remove an element from the interface
    :param elements_list: Element List to be removed
    """
    page = None
    for element in elements_list:
        page = element.page
        page.remove(element)

    page.update()


def show_into_container(container,
                        element
                        ):
    container.content.controls.append(element)
