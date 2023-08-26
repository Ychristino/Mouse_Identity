import flet as ft

from elements.element_run_training import checkbox_user_list, checkbox_model_list, select_game, button_play, button_stop


def Visualize_Data(page: ft.Page):
    """
    Page for the training process. The construction was compound by 2 components: Filter Container Represents the
    Users of the application, should contain the main user and the list of the other users registered. This Container
    should also contain the Model list, giving the user the capability to choose one or more models to train, just like
    a linear model, SVC model or Tree Model.
    The results will be added to a folder on separated files for each model.
    The Action Container Represents the final interaction, consists in a Run button to execute the selected(s) model(s)
    for the selected(s) user(s), generating the files with the data about the training data, just like accuracy,
    precision score or recall score, etc.
    """
    page.title = 'Train Model'

    filter_container = ft.Container(margin=10,
                                    padding=10,
                                    alignment=ft.alignment.center,
                                    content=ft.Column([
                                        ft.Row([
                                            select_game
                                        ]),
                                        ft.Row(
                                            [
                                                ft.Column(
                                                    checkbox_user_list,
                                                    run_spacing=10,
                                                ),
                                                ft.Column(
                                                    checkbox_model_list,
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                                        )
                                        ],
                                        spacing=50,
                                        )
                                    )

    action_container = ft.Container(margin=10,
                                    padding=10,
                                    alignment=ft.alignment.bottom_center,
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    button_play,
                                                    button_stop
                                                ],
                                                tight=True,
                                            )
                                        ],
                                        tight=True
                                    ))

    page.scroll = ft.ScrollMode.AUTO
    # PAGE
    page.add(
        filter_container,
        action_container,
    )


ft.app(target=Visualize_Data)
