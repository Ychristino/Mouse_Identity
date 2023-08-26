import flet as ft


def generate_graph(event, enable: list = None, disable: list = None):
    """
    The function will create a Progress bar on the bottom of the page to inform the user about the status of the
    recording. Usually, will be a no limited progress bar, since the record should only stop when the stop button was
    clicked. By default, the clicked button will be set as disabled, since the user can not trigger the event twice.
    :param event: Event from the element, is passed automatically when an event is triggered. If used in a lambda expression, you should declare it as a parameter and also inform it on your parameters
    :param enable: List of elements on page that should be enabled when this event happen
    :param disable: List of elements on page that should be disabled when this event happen
    """
    event.control.disabled = True
    event.control.icon_color = ft.colors.with_opacity(0.2, 'black400')

    if enable is not None:
        for el in enable:
            el.disabled = False
            el.icon_color = 'red400'

    if disable is not None:
        for el in disable:
            el.disabled = True
            el.icon_color = ft.colors.with_opacity(0.2, 'black400')

    progress_bar = ft.Container(margin=10,
                                padding=10,
                                alignment=ft.alignment.bottom_center,
                                expand=False,
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Column([
                                                    ft.Text('Running Record'),
                                                    ft.ProgressBar(width=800, color="green300", bgcolor="#eeeeee"),
                                                ])
                                            ],
                                            tight=True
                                        ),
                                    ],
                                    tight=True
                                ))

    event.page.add(progress_bar)
    event.page.update()


def stop_record(event, enable: list = None, disable: list = None):
    """
    The function will delete the Progress bar on the bottom of the page to inform the user the recording is no longer running.
    By default, the clicked button will be set as disabled, since the user can not trigger the event twice.
    :param event: Event from the element, is passed automatically when an event is triggered, if used in a lambda expression, tou should declare it as a parameter and also inform it on your parameters
    :param enable: List of elements on page that should be enabled when this event happen
    :param disable: List of elements on page that should be disabled when this event happen
    """
    event.control.disabled = True
    event.control.icon_color = ft.colors.with_opacity(0.2, 'black400')
    if enable is not None:
        for el in enable:
            el.disabled = False
            el.icon_color = 'green400'

    if disable is not None:
        for el in disable:
            el.disabled = True
            el.icon_color = ft.colors.with_opacity(0.2, 'black400')

    event.page.controls.pop(3)
    event.page.update()


def graph_navigation(chart, chart_list, direction):
    pass
