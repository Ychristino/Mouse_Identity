import flet as ft
from consts import games, plot
from page.events.event_visualize_data import generate_graph

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
    on_click=lambda event: generate_graph(event, validate=[select_graph_type,select_game], params=(select_graph_type,select_game)),
    expand=True
)

button_preview = ft.IconButton(
    icon=ft.icons.NAVIGATE_BEFORE,
    icon_color="blue400",
    icon_size=60,
    tooltip="Preview",
#    on_click=lambda: graph_navigation(chart_list, -1)
)
button_next = ft.IconButton(
    icon=ft.icons.NAVIGATE_NEXT,
    icon_color="blue400",
    icon_size=60,
    tooltip="Next",
#    on_click=lambda: graph_navigation(chart_list, 1)
)


select_graph_type.id = 'graph_type'
select_game.id = 'game_name'
