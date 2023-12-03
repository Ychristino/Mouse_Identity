import flet as ft


class progress_bar:
    """
    Create a progress bar at the bottom of the screen, used to let user know when the task is running
    """

    def __init__(self):
        self.progress_bar_container = None
        self.page = None
        self.progress_bar = None

    def create_progress_bar(self,
                            page: ft.Page,
                            label: str = None
                            ):
        """
        Function to create the Progress Bar and its Container.
        :param page: Page where the Progress Bar should be positioned
        :param label: Label upside the Progress Bar... If don't want to show any labels, inform None (or let the default value)
        :return: ft.Container with the Progress Bar and the Text Label
        """
        self.page = page

        self.progress_bar = ft.ProgressBar(width=800,
                                           color="green300",
                                           bgcolor="#eeeeee"
                                           )
        self.progress_bar_container = ft.Container(margin=10,
                                                   padding=10,
                                                   alignment=ft.alignment.bottom_center,
                                                   expand=False,
                                                   content=ft.Column(
                                                       [
                                                           ft.Row(
                                                               [
                                                                   ft.Column([
                                                                       ft.Text(label),
                                                                       self.progress_bar
                                                                   ])
                                                               ],
                                                               tight=True
                                                           ),
                                                       ],
                                                       tight=True
                                                   ))
        return self.progress_bar_container

    def start(self):
        """
        Set the progress bar on screen and update the page to show the progress
        """
        self.page.add(self.progress_bar_container)
        self.page.update()

    def stop(self):
        """
        Remove the progress bar of the screen and refresh the page
        """
        self.page.controls.remove(self.progress_bar_container)
        self.page.update()
