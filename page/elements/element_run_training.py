import os
import flet as ft
from consts import paths, models, games
from page.events.event_run_training import run_training, stop_training

user_list = list(filter(lambda x: os.path.isdir(os.path.join(paths.SUSPECT_DATA, x)), os.listdir(paths.SUSPECT_DATA)))
model_list = [value for name, value in vars(models).items() if not name.startswith('_')]

checkbox_user_list = [ft.Checkbox(label=user, value=True) for user in user_list]
checkbox_model_list = [ft.Checkbox(label=model, value=True) for model in model_list]

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

button_play = ft.IconButton(
    icon=ft.icons.PLAY_CIRCLE,
    icon_color="green400",
    icon_size=60,
    tooltip="Start record",
    on_click=lambda element: run_training(element, enable=[button_stop], validate=[checkbox_user_list,checkbox_model_list,select_game])
)

button_stop = ft.IconButton(
    icon=ft.icons.STOP_CIRCLE,
    icon_color=ft.colors.with_opacity(0.2, 'black400'),
    icon_size=60,
    tooltip="Stop record",
    on_click=lambda element: stop_training(element, enable=[button_play]),
    disabled=True
)

for item in checkbox_user_list:
    item.groupName = 'user_list'

for item in checkbox_model_list:
    item.groupName = 'model_list'

select_game.id = 'game_name'

button_play.avail_color = 'green400'
button_stop.avail_color = 'red300'
