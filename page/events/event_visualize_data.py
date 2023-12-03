import pandas as pd
from flet_core.matplotlib_chart import MatplotlibChart

import consts.plot
from page.elements.function.graph_element import build_graph_frame
from process.data import get_graph_data
from process.generate.generate_heatmap_graph import generate_heatmap_graph
from process.generate.generate_statistics_graph import generate_statistics_graph
from page.elements.function.find_element import get_element_by_id
from page.elements.function.iteract_element import disable_element_list, enable_element_list, disable_element, \
    enable_element, show_into_container
from page.events.default import dialogs
from page.validation.visualize_data_validation import generate_graph_validation
from page.events.default.progress_bar import progress_bar

__progress_bar = progress_bar()


def generate_graph(event,
                   enable: list = None,
                   disable: list = None,
                   validate: list = None,
                   params: tuple = None
                   ):
    """
    The function will create a Progress bar on the bottom of the page to inform the user about the status of the
    recording. Usually, will be a no limited progress bar, since the record should only stop when the stop button was
    clicked. By default, the clicked button will be set as disabled, since the user can not trigger the event twice.
    :param event: Event from the element, is passed automatically when an event is triggered. If used in a lambda expression, you should declare it as a parameter and also inform it on your parameters
    :param enable: List of elements on page that should be enabled when this event happen
    :param disable: List of elements on page that should be disabled when this event happen
    :param validate: List of elements that should be validated by the __start_record_validation function
    :param params: Tuple with elements that should be used to define plot type and which data file should read for the plot
    """
    global __progress_bar

    try:
        generate_graph_validation(validate)
    except Exception as err:
        dialog = dialogs.dialog()
        dialog.error("Ops, something went wrong...", str(err), event.page)
        return

    container_graph = get_element_by_id('container_graph', event.page)
    container_graph.content.controls.clear()

    __progress_bar.create_progress_bar(event.page, 'Generating Graph')
    __progress_bar.start()

    disable_element(event.control)

    if disable is not None:
        disable_element_list(disable)

    if enable is not None:
        enable_element_list(enable)

    graph_type = get_element_by_id('graph_type', params)
    game_name = get_element_by_id('game_name', params)

    data = get_graph_data(is_main=True,
                          game_name=game_name.value,
                          graph_type=graph_type.value
                          )

    chart = __generate_chart(graph_type=graph_type.value,
                             data=data
                             )
    chart_frame = build_graph_frame(chart)
    show_into_container(container_graph, chart_frame)

    enable_element(event.control)

    if disable is not None:
        enable_element_list(disable)

    if enable is not None:
        disable_element_list(enable)

    __progress_bar.stop()
    event.page.update()


def __generate_chart(graph_type,
                     data: pd.DataFrame
                     ):
    match graph_type:
        case consts.plot.MOUSE_STATS:
            return __chart_stats(data)
        case consts.plot.HEATMAP:
            return __chart_heatmap(data)


def __chart_stats(dataframe: pd.DataFrame):
    graph_click = dataframe[['qt_l_click',
                             'qt_r_click'
                             ]]
    graph_movement = dataframe[['l_mov_count',
                                'r_mov_count',
                                'u_mov_count',
                                'd_mov_count'
                                ]]

    graph_avg_time = dataframe[['avg_time_l_click',
                                'avg_time_r_click',
                                'avg_time_l_mov',
                                'avg_time_r_mov',
                                'avg_time_u_mov',
                                'avg_time_d_mov'
                                ]]

    graph_total_time = dataframe[['total_time_l_click',
                                  'total_time_r_click',
                                  'total_time_l_mov',
                                  'total_time_r_mov',
                                  'total_time_u_mov',
                                  'total_time_d_mov',
                                  'total_hor_time',
                                  'total_ver_time'
                                  ]]

    graph_distance = dataframe[['total_dist_l_mov',
                                'total_dist_r_mov',
                                'total_dist_u_mov',
                                'total_dist_d_mov',
                                'total_hor_dist',
                                'total_ver_dist'
                                ]]

    graph_speed = dataframe[['hor_speed',
                             'ver_speed',
                             'l_speed',
                             'r_speed',
                             'u_speed',
                             'd_speed',
                             'total_capture_time'
                             ]]

    _, chart_click = generate_statistics_graph(data=graph_click).bar()
    _, chart_movement = generate_statistics_graph(data=graph_movement).bar()
    _, chart_avg_time = generate_statistics_graph(data=graph_avg_time).bar()
    _, chart_total_time = generate_statistics_graph(data=graph_total_time).bar()
    _, chart_distance = generate_statistics_graph(data=graph_distance).bar()
    _, chart_speed = generate_statistics_graph(data=graph_speed).bar()
    _, chart_general = generate_statistics_graph(data=dataframe).bar()

    chart_list = [
        chart_click,
        chart_movement,
        chart_avg_time,
        chart_total_time,
        chart_distance,
        chart_speed,
        chart_general
    ]

    return chart_list


def __chart_heatmap(dataframe: pd.DataFrame):
    fig = generate_heatmap_graph(dataframe).generate()
    chart = MatplotlibChart(fig,
                            expand=True,
                            isolated=True,
                            original_size=True,
                            transparent=True
                            )

    return chart
