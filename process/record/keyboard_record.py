import time
import keyboard
import threading
import pandas as pd

from process.data import save_data


class keyboard_record:
    """
    Class to perform data Record.
    Should track the keyboard events and register data like button pressed, time pressed, etc.
    All the data will be stored in a single file named as the task informed on the run method.
    """

    def __init__(self,
                 data_dict: dict = None
                 ) -> None:
        """
        Initialize the general parameters to register any run of the record
        """
        self.data_dict = dict()
        self.active_record = False

    def read_keyboard(self) -> pd.DataFrame:
        assert self.active_record
        delta_start = time.time()

        while self.active_record:
            event = keyboard.read_event()
            if event.name not in self.data_dict:
                self.data_dict[event.name] = {
                    'key_down': [],
                    'key_up': [],
                    'time_pressed': [],
                    'total_time_pressed': 0,
                    'count': 0,
                    'average': 0,
                    'is_pressed': False
                }

            if event.event_type == keyboard.KEY_DOWN and not self.data_dict[event.name]['is_pressed']:
                self.data_dict[event.name]['key_down'].append(time.time() - delta_start)
                self.data_dict[event.name]['is_pressed'] = True
                # print('Down: ' + event.name)

            if event.event_type == keyboard.KEY_UP and self.data_dict[event.name]['is_pressed']:
                self.data_dict[event.name]['key_up'].append(time.time() - delta_start)
                time_pressed = self.data_dict[event.name]['key_up'][-1] - self.data_dict[event.name]['key_down'][-1]
                self.data_dict[event.name]['time_pressed'].append(time_pressed)
                self.data_dict[event.name]['total_time_pressed'] += time_pressed
                self.data_dict[event.name]['count'] += 1
                self.data_dict[event.name]['average'] = self.data_dict[event.name]['total_time_pressed'] / \
                                                        self.data_dict[event.name]['count']
                self.data_dict[event.name]['is_pressed'] = False
                # print('Up:' + event.name)

        return pd.DataFrame(self.data_dict)

    def __set_configuration(self) -> None:
        """
        Run setup Configuration, initialize all the variables and dataframes to record data.
        """
        pass

    def stop_record(self) -> None:
        self.active_record = False

    def start_record(self,
                     path: str = './data',
                     task: str = 'keyboard_read'
                     ) -> None:
        """
        Execution method to simplify the usage. Call the method to start record a basic example with 2000 sample collects with a hundredth second interval
        :param path: Where the file should be saved
        :param task: Task recorded, used to name the file stored
        """
        self.active_record = True
        data_frame = self.read_keyboard()
        save_data(data=data_frame,
                  path=path,
                  file=f"{task.replace(' ', '_')}.csv",
                  override=True
                  )


if __name__ == '__main__':
    m = keyboard_record()
    threading.Thread(target=m.start_record).start()

    time.sleep(10)
    m.stop_record()
