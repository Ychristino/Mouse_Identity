import flet as ft

from page.elements.element_visualize_data import select_graph_type, select_game, button_generate_graph, button_preview, \
    button_next  # , chart


def Visualize_Data(page: ft.Page):
    """
    Page for visualizing data. The construction was compound by Three components: Filter Container Represents the data
    information, like the game recorded and the plot/type of data you want to see. Plot Container Represents the
    place where the image should be displayed, will be rendered when the action container were activated. Action
    Container Represents the final interaction, consists in a plot button to show selected graph of a game. Interface
    Properties: The Filter Container will filter files to get the data file with the game name and filter the
    expected fields. Action Container can trigger events like show and hide ProgressBar on screen, to let user know
    when the plot is running or not; Action Container will also run the image generator and place it into the Plot
    Container according the Filter Container selection.
    """
    page.title = 'Visualize Data'

    filter_container = ft.Container(margin=10,
                                    padding=10,
                                    alignment=ft.alignment.top_center,
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    select_graph_type
                                                ]
                                            ),
                                            ft.Row(
                                                [
                                                    select_game
                                                ]
                                            )
                                        ],
                                        spacing=50
                                    ))

    action_container = ft.Container(margin=5,
                                    padding=10,
                                    alignment=ft.alignment.bottom_center,
                                    content=ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    button_generate_graph
                                                ],
                                                tight=True,
                                            )
                                        ],
                                        tight=True
                                    ))

    graph_control_container = ft.Container(margin=5,
                                           padding=10,
                                           alignment=ft.alignment.bottom_left,
                                           expand=True,
                                           content=ft.Row(
                                               [
                                                   button_preview,
                                                   button_next
                                               ],
                                               alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                           ))

    plot_container = ft.Container(margin=5,
                                  padding=10,
                                  alignment=ft.alignment.bottom_center,
                                  content=ft.Column(
                                      [
                                      ],
                                      spacing=0
                                  ))

    filter_container.id = 'container_filter'
    graph_control_container.id = 'container_controls'
    action_container.id = 'container_action'
    plot_container.id = 'container_graph'

    page.scroll = ft.ScrollMode.AUTO
    # PAGE
    page.add(
        filter_container,
        action_container,
        plot_container,
    )


ft.app(target=Visualize_Data)
