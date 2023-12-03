import flet as ft

from page.elements.function.find_element import get_element_by_id
from page.elements.function.iteract_element import update_barchart, enable_element, disable_element


__current_chart, __chart_group = None, None

def prev_graph_navigation(event):
    global __current_chart, __chart_group

    chart = get_element_by_id('chart', event.page)

    if __current_chart > 0:
        __current_chart -= 1
        chart = update_barchart(chart, __chart_group[__current_chart])
        enable_element(get_element_by_id('next_chart', event.page))
        chart.update()
    else:
        disable_element(get_element_by_id('prev_chart', event.page))


def next_graph_navigation(event):
    global __current_chart, __chart_group

    chart = get_element_by_id('chart', event.page)

    if __current_chart < len(__chart_group) - 2:
        __current_chart += 1
        chart = update_barchart(chart, __chart_group[__current_chart])
        enable_element(get_element_by_id('prev_chart', event.page))
        chart.update()
    else:
        disable_element(get_element_by_id('next_chart', event.page))


def __build_graph_control():
    button_preview = ft.IconButton(
        icon=ft.icons.NAVIGATE_BEFORE,
        icon_color="black400",
        icon_size=60,
        tooltip="Preview",
        on_click=prev_graph_navigation,
        disabled=True
    )
    button_next = ft.IconButton(
        icon=ft.icons.NAVIGATE_NEXT,
        icon_color="primary",
        icon_size=60,
        tooltip="Next",
        on_click=next_graph_navigation,
    )
    graph_control_container = ft.Row(
        [
            button_preview,
            button_next
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=False
    )
    button_next.id = 'next_chart'
    button_preview.id = 'prev_chart'

    return graph_control_container


def build_graph_frame(data):
    global __current_chart, __chart_group
    row_content = []

    if isinstance(data, list):
        __chart_group = data
        __current_chart = 0

        row_content.append(__build_graph_control())
        data = data[__current_chart]

        for chart in __chart_group:
            chart.id = 'chart'

    row_content.append(ft.Row(
        [
            data
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        expand=False
    ))

    return ft.Column(row_content,
                     spacing=0
                     )
