import flet as ft
from page.events.default import dialogs
from page.validation.record_data_validation import start_record_validation
from page.events.default.progress_bar import progress_bar
from page.elements.function.iteract_element import disable_element_list, enable_element_list, disable_element

__progress_bar = progress_bar()


def start_record(event,
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
        start_record_validation(validate)
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

def stop_record(event,
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


def switch_change(event,
                  block_when_enabled: list = None
                  ):
    """
    :param event: Event from the element, is passed automatically when an event is triggered. If used in a lambda
    :param block_when_enabled: List of elements that should be disabled when the Switch is set to True, if the Switch get clicked again and set to False, the elements on the list should be Enabled again. When the element is disabled the value is set to <<Empty>>.
    """

    if event.control.value:
        disable_element_list(block_when_enabled)
    else:
        enable_element_list(block_when_enabled)

    event.page.update()
