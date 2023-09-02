import flet as ft
from page.elements.element_record_data import switch_main_user, input_text_username, select_game, button_play, button_stop


def Record_Data(page: ft.Page):
    """
    Page for recording data. The construction was compound by Three components: User Container Represents the user
    information, just like the name of the user if the current user is the main user of the system Game Container
    Represents the Game that will be recorded, since we have to separate each game for file to be analysed and
    compared as it should Action Container Represents the final interaction, consists in a play and stop button to
    start recording mouse movements or stop recording it. Interface Properties: The User Container should hide or
    block the username field if the Main user button was Enabled. The username is only used to select a right folder
    for data separation. If the button is disabled, the selected folder will be the Suspect_Data, where the username
    will name the child folder with your data. Action Container can trigger events like show and hide ProgressBar on
    screen, to let user know when the record is running or not; Also, Action container should disable the selected
    button, so user can not play 2 records or stop a non-running application
    """
    page.title = 'Record Data'

    # CONTAINERS
    user_container = ft.Container(margin=10,
                                  padding=10,
                                  alignment=ft.alignment.top_center,
                                  content=ft.Column(
                                      [
                                          ft.Row([
                                              ft.Column(
                                                  [
                                                      ft.Text('Main User'),
                                                      switch_main_user,
                                                  ],
                                                  spacing=2
                                              )
                                          ]),
                                          ft.Row(
                                              [
                                                  input_text_username
                                              ]
                                          )
                                      ],
                                      spacing=5
                                  ))

    game_container = ft.Container(margin=10,
                                  padding=10,
                                  alignment=ft.alignment.top_center,
                                  content=ft.Column(
                                      [
                                          ft.Row([
                                              select_game
                                          ])
                                      ]
                                  ))

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

    action_container.id = 'action_container'
    game_container.id = 'game_container'
    user_container.id = 'user_container'

    page.scroll = ft.ScrollMode.AUTO
    # PAGE
    page.add(
        user_container,
        game_container,
        action_container
    )


ft.app(target=Record_Data)
