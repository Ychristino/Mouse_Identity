import flet as ft

from page.elements.function.iteract_element import enable_element_list, disable_element_list, disable_element
from page.validation.run_training_validation import run_training_validation
from page.events.default.progress_bar import progress_bar
from page.events.default import dialogs

__progress_bar = progress_bar()


def run_training(event,
                 enable: list = None,
                 disable: list = None,
                 validate: list = None
                 ):
    """
    The function will create a Progress bar on the bottom of the page to inform the user about the status of the
    recording. Usually, will be a no limited progress bar, since the record should only stop when the stop button was
    clicked. By default, the clicked button will be set as disabled, since the user can not trigger the event twice.
    :param event: Event from the element, is passed automatically when an event is triggered. If used in a lambda expression, you should declare it as a parameter and also inform it on your parameters
    :param enable: List of elements on page that should be enabled when this event happen
    :param disable: List of elements on page that should be disabled when this event happen
    :param validate: List of elements that should be validated by the __start_record_validation function
    """
    global __progress_bar

    try:
        run_training_validation(validate)
    except Exception as err:
        dialog = dialogs.dialog()
        dialog.error("Ops, something went wrong...", str(err), event.page)
        return

    disable_element(event.control)

    if disable is not None:
        disable_element_list(disable)

    if enable is not None:
        enable_element_list(enable)

    __progress_bar.create_progress_bar(event.page, 'Running Train')
    __progress_bar.start()
    event.page.update()


def stop_training(event,
                  enable: list = None,
                  disable: list = None
                  ):
    """
    The function will create a Progress bar on the bottom of the page to inform the user about the status of the
    recording. Usually, will be a no limited progress bar, since the record should only stop when the stop button was
    clicked. By default, the clicked button will be set as disabled, since the user can not trigger the event twice.
    :param event: Event from the element, is passed automatically when an event is triggered. If used in a lambda expression, you should declare it as a parameter and also inform it on your parameters
    :param enable: List of elements on page that should be enabled when this event happen
    :param disable: List of elements on page that should be disabled when this event happen
    """
    global __progress_bar

    disable_element(event.control)

    if disable is not None:
        disable_element_list(disable)

    if enable is not None:
        enable_element_list(enable)

    __progress_bar.stop()
    event.page.update()
