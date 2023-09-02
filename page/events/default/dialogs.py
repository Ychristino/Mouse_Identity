import flet as ft


class dialog:
    """
    Create Dialogs to iteract with user
    """
    def __init__(self):
        self.dialog = None
        self.page = None

    def error(self,
              title: str,
              content: str,
              page: ft.Page
              ) -> ft.AlertDialog:
        """
        Create an ERROR window with the error message in the page
        :param title: Title of the Error
        :param content: Error message
        :param page: Page that should display the message
        :return: Dialog window
        """
        self.dialog = ft.AlertDialog(
            modal=True,
            open=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("Ok", on_click=self.__close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page = page
        self.__show()
        return self.dialog

    def alert(self,
              title: str,
              content: str,
              page: ft.Page
              ) -> ft.AlertDialog:
        """
        Create an Alert window with the Alert message in the page
        :param title: Title of the Alert
        :param content: Alert message
        :param page: Page that should display the message
        :return: Dialog window
        """
        self.dialog = ft.AlertDialog(
            modal=True,
            open=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("Ok", on_click=self.__close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page = page
        self.__show()
        return self.dialog

    def confirm(self,
                title: str,
                content: str,
                page: ft.Page
                ) -> ft.AlertDialog:
        """
        Create an Confirm window with the message in the page
        :param title: Title of the Confirm
        :param content: Confirm message
        :param page: Page that should display the message
        :return: Dialog window
        """
        self.dialog = ft.AlertDialog(
            modal=True,
            open=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("Yes", on_click=self.__close_dialog),
                ft.TextButton("No", on_click=self.__close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page = page
        self.__show()
        return self.dialog

    def warning(self,
                title: str,
                content: str,
                page: ft.Page
                ) -> ft.AlertDialog:
        """
        Create an Warning window with the Warning message in the page
        :param title: Title of the Warning
        :param content: Warning message
        :param page: Page that should display the message
        :return: Dialog window
        """
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(content),
            actions=[
                ft.TextButton("Ok", on_click=self.__close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page = page
        self.__show()
        return self.dialog

    def __show(self) -> None:
        """
        Funcion that display the dialog into the screen
        """
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def __close_dialog(self,
                       event
                       ) -> None:
        """
        Function that Closes the dialog
        """
        self.dialog.open = False
        self.page.update()
