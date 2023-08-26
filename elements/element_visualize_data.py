import flet as ft
import pandas as pd

import consts.paths
from consts import games, plot
from events.event_visualize_data import generate_graph, graph_navigation
from generate_heatmap_graph import generate_heatmap_graph
from generate_statistics_graph import generate_statistics_graph
from flet.matplotlib_chart import MatplotlibChart

select_graph_type = ft.Dropdown(
    label="Graph",
    hint_text="Which graph you wanna see?",
    border=ft.InputBorder.UNDERLINE,
    filled=True,
    options=[ft.dropdown.Option(value) for name, value in
             vars(plot).items() if not name.startswith('_')],
    autofocus=True,
    expand=True
)

select_game = ft.Dropdown(
    label="Game",
    hint_text="Which game you wanna play?",
    border=ft.InputBorder.UNDERLINE,
    filled=True,
    options=[ft.dropdown.Option(value) for name, value in
             vars(games).items() if not name.startswith('_')],
    autofocus=True,
    expand=True
)

button_generate_graph = ft.FilledTonalButton(
    'Generate Graph',
    icon=ft.icons.BROKEN_IMAGE_OUTLINED,
    icon_color="green400",
    tooltip="Generate Graph",
    on_click=lambda event: generate_graph(event),
    expand=True
)

button_preview = ft.IconButton(
    icon=ft.icons.NAVIGATE_BEFORE,
    icon_color="blue400",
    icon_size=60,
    tooltip="Preview",
    on_click=lambda: graph_navigation(chart_list, -1)
)
button_next = ft.IconButton(
    icon=ft.icons.NAVIGATE_NEXT,
    icon_color="blue400",
    icon_size=60,
    tooltip="Next",
    on_click=lambda: graph_navigation(chart_list, 1)
)

dataframe = pd.read_csv(f'{consts.paths.USER_STATS}/League_of_Legends_mouse_stats', sep=';')
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

chart_list = [chart_click,
              chart_movement,
              chart_avg_time,
              chart_total_time,
              chart_distance,
              chart_speed,
              chart_general
              ]

#chart = chart_distance

dataframe = pd.read_csv(f'{consts.paths.USER_EVENT}/Valorant_mouse_event', sep=';')
fig = generate_heatmap_graph(dataframe).generate()
chart = MatplotlibChart(fig,
                        expand=True,
                        isolated=True,
                        original_size=True,
                        transparent=False
                        )