import flet as ft
from consts import games
from events.event_record_data import switch_change, start_record, stop_record

"""
Document contains the elements needed for the page, as input fields, select boxes, etc.
Some other stuff can happen, just like the progress bar that should be added for a process that control your current 
step.
Elements should be constructed as basic variables and added into page element into your frame (container).
Containers will be rendered at the end of the page, building the user interface properly.
"""
# ELEMENTS
# USER CONTAINER
switch_main_user = ft.Switch(
    active_track_color='green300',
    inactive_track_color='red300',
    value=True,
    on_change=lambda event: switch_change(event, block_when_enabled=[input_text_username])
)

input_text_username = ft.TextField(
    label="User Name",
    border=ft.InputBorder.UNDERLINE,
    filled=True,
    hint_text="Suspect Name",
    expand=True,
    disabled=True
)

# GAME CONTAINER
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

# ACTION_CONTAINER
button_play = ft.IconButton(
    icon=ft.icons.PLAY_CIRCLE,
    icon_color="green400",
    icon_size=60,
    tooltip="Start record",
    on_click=lambda element: start_record(element,
                                          enable=[button_stop],
                                          validate=[switch_main_user,
                                                    input_text_username,
                                                    select_game
                                                    ]
                                          )
)

button_stop = ft.IconButton(
    icon=ft.icons.STOP_CIRCLE,
    icon_color=ft.colors.with_opacity(0.2, 'black400'),
    icon_size=60,
    tooltip="Stop record",
    on_click=lambda element: stop_record(element, enable=[button_play]),
    disabled=True
)
