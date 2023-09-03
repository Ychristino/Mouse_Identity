import time
import win32api
from consts import movement
import pandas as pd
import pyautogui as pgui
from process.data import save_data


def get_resolution() -> tuple:
    """
    Get the user Screen Resolution
    :return: Tuple with the user Screen resolution
    """
    return pgui.size()


def click_status_changed(click_status: bool,
                         mouse_button: bool
                         ) -> bool:
    """
    Inform if the Click status has changed
    :param click_status: Inform if the button is currently clicked
    :param mouse_button: button to compare, used as old_value for the button
    :return: Bool value informing if the button click has changed
    """
    return is_pressed(click_status) != mouse_button


def movement_status_changed(old_position,
                            current_position,
                            old_state
                            ) -> bool:
    """
    Inform if the movement status has changed
    :param old_position: Pointer last position. Should be passed as X for horizontal change or Y for vertical (separately)
    :param current_position: Pointer current position. Should be passed as X for horizontal change or Y for vertical (separately)
    :param old_state: The status of the last verification... Was mouse moving or stopped
    :return: Bool value informing if the movement has changed
    """
    return (old_position != current_position) != old_state


def is_pressed(button) -> bool:
    """
    Inform if the button is currently pressed
    :param button: Button to validate
    :return: Bool value informing if the button is currently pressed or not
    """
    return button < 0


class record:
    """
    Class to perform data Record.
    Should track the mouse cursor and register data like mouse movement, clicks, time, speed, etc.
    All the data will be stored in separated files named as the task informed on the run method.
    Data files will have a suffix informing what the file contains, status or events.
    Event Files will contain all the tracking data, when a click was performed, which direction the cursor is running and what time is this beeing recorded.
    Status Files will contain a general analysys of the run. Will show how many times the click was active, the distance traveled by the mouse cursor, etc.
    """

    def __init__(self,
                 sample_size: int = 2000,
                 sample_collection_interval: float = 0.01,
                 interval_between_collection: int = 10
                 ):
        """
        Initialize the general parameters to register any run of the record
        :param sample_size: How many samples should be collected.
        :param sample_collection_interval: Interval between a sample collection and the next one.
        :param interval_between_collection: Interval between a run and another. If the user wants to record multiple times with spaced time between collection.
        """
        self.sample_size = sample_size
        self.sample_collection_interval = sample_collection_interval
        self.interval_between_collection = interval_between_collection
        self.__set_configuration()

    def __set_configuration(self):
        """
        Run setup Configuration, initialize all the variables and dataframes to record data.
        """
        self.screen_width, self.screen_height = get_resolution()
        self.__init_click_variables()
        self.__init_movement_variables()
        self.mouse_event_dataframe = pd.DataFrame()
        self.mouse_stats_dataframe = pd.DataFrame()

    def __init_click_variables(self):
        """
        Create and initialize all the variables used on the Click analysys.
        """
        self.l_click = False
        self.r_click = False

        self.qt_l_click = 0
        self.qt_r_click = 0

        self.avg_time_l_click = 0
        self.avg_time_r_click = 0

        self.total_time_l_click = 0
        self.total_time_r_click = 0

        self.delta_left_click = 0
        self.delta_right_click = 0

    def __init_movement_variables(self):
        """
        Create and initialize all the variables used in the movement analysis.
        """
        self.l_mov = False
        self.r_mov = False

        self.is_moving_hor = False
        self.is_moving_ver = False

        self.mov_hor_dir = 0
        self.mov_ver_dir = 0

        self.delta_hor_mov = 0
        self.delta_ver_mov = 0

        self.mov_hor_dist = 0
        self.mov_ver_dist = 0

        self.total_time_l_mov = 0
        self.total_time_r_mov = 0

        self.l_mov_count = 0
        self.r_mov_count = 0

        self.total_time_u_mov = 0
        self.total_time_d_mov = 0

        self.u_mov_count = 0
        self.d_mov_count = 0

        self.tot_hor_dist = 0
        self.tot_ver_dist = 0

        self.total_dist_l_mov = 0
        self.total_dist_r_mov = 0
        self.total_dist_u_mov = 0
        self.total_dist_d_mov = 0

        self.tot_hor_time = 0
        self.tot_ver_time = 0

    def __set_hor_dist(self,
                       hor_dist: int
                       ):
        """
        Set the horizontal distance for the sample.
        If the value is negative, the cursor will be running to the left side of the screen.
        Else, the cursor will be running to the right side of the screen.
        :param hor_dist: The current distance traveled by the mouse (interval between last sample and current one)
        """
        if hor_dist < 0:
            self.mov_hor_dir = movement.LEFT
            self.total_time_l_mov += self.delta_hor_mov
            self.total_dist_l_mov += abs(hor_dist)
            self.l_mov_count += 1
        else:
            self.mov_hor_dir = movement.RIGHT
            self.total_time_r_mov += self.delta_hor_mov
            self.total_dist_r_mov += abs(hor_dist)
            self.r_mov_count += 1

    def __set_ver_dist(self,
                       ver_dist: int
                       ):
        """
        Set the vertical distance for the sample.
        If the value is negative, the cursor will be running to the top side of the screen.
        Else, the cursor will be running to the bottom side of the screen.
        :param ver_dist: The current distance traveled by the mouse (interval between last sample and current one)
        """
        if ver_dist < 0:
            self.mov_ver_dir = movement.UP
            self.total_time_u_mov += self.delta_ver_mov
            self.total_dist_u_mov += abs(ver_dist)
            self.u_mov_count += 1
        else:
            self.mov_ver_dir = movement.DOWN
            self.total_time_d_mov += self.delta_ver_mov
            self.total_dist_d_mov += abs(ver_dist)
            self.d_mov_count += 1

    def new_mouse_event_record(self,
                               start_time: time,
                               mouse_position: tuple
                               ) -> pd.DataFrame:
        """
        Save the event record, a single sample of the run, into the dataframe with all the information collected
        :param start_time: When the record began
        :param mouse_position: The current position of the cursor
        :return: Dataframe that contains all the data stored until the method calls
        """
        x_position, y_position = mouse_position
        new_data = pd.DataFrame(
            {'x': x_position,
             'y': y_position,

             'l_click': (1 if self.l_click else 0),
             'r_click': (1 if self.r_click else 0),

             'l_click_count': self.qt_l_click,
             'r_click_count': self.qt_r_click,

             'total_time_l_click': f'{self.total_time_l_click:.2f}',
             'total_time_r_click': f'{self.total_time_r_click:.2f}',

             'avg_time_l_click': f'{(self.total_time_l_click / (self.qt_r_click if self.qt_r_click > 0 else 1)):.2f}',
             'avg_time_r_click': f'{(self.total_time_r_click / (self.qt_r_click if self.qt_r_click > 0 else 1)):.2f}',

             'is_moving_horizontal': (1 if self.is_moving_hor else 0),
             'is_moving_vertical': (1 if self.is_moving_ver else 0),

             'horizontal_dist': (x_position - self.mov_hor_dist) if self.is_moving_hor else 0,
             'vertical_dist': (y_position - self.mov_ver_dist) if self.is_moving_ver else 0,

             'hor_movement_time': f'{(time.time() - self.delta_hor_mov):.2f}' if self.is_moving_hor else f'{0:.2f}',
             'ver_movement_time': f'{(time.time() - self.delta_ver_mov):.2f}' if self.is_moving_ver else f'{0:.2f}',

             'l_mov_count': self.l_mov_count,
             'r_mov_count': self.r_mov_count,
             'u_mov_count': self.u_mov_count,
             'd_mov_count': self.d_mov_count,

             'total_dist_l_mov': self.total_dist_l_mov,
             'total_dist_r_mov': self.total_dist_r_mov,
             'total_dist_u_mov': self.total_dist_u_mov,
             'total_dist_d_mov': self.total_dist_d_mov,

             'total_time_l_mov': f'{self.total_time_l_mov:.2f}',
             'total_time_r_mov': f'{self.total_time_r_mov:.2f}',
             'total_time_u_mov': f'{self.total_time_u_mov:.2f}',
             'total_time_d_mov': f'{self.total_time_d_mov:.2f}',

             'avg_time_l_mov': f'{(self.total_time_l_mov / (self.l_mov_count if self.l_mov_count > 0 else 1)):.2f}',
             'avg_time_r_mov': f'{(self.total_time_r_mov / (self.r_mov_count if self.r_mov_count > 0 else 1)):.2f}',
             'avg_time_u_mov': f'{(self.total_time_u_mov / (self.u_mov_count if self.u_mov_count > 0 else 1)):.2f}',
             'avg_time_d_mov': f'{(self.total_time_d_mov / (self.d_mov_count if self.d_mov_count > 0 else 1)):.2f}',

             'time': f'{(time.time() - start_time):.2f}',
             'width': self.screen_width,
             'height': self.screen_height
             }, index=[len(self.mouse_event_dataframe)]
        )

        self.mouse_event_dataframe = pd.concat([self.mouse_event_dataframe, new_data],
                                               ignore_index=True,
                                               copy=False
                                               )
        return self.mouse_event_dataframe

    def new_mouse_stats_record(self,
                               start_time: time
                               ) -> pd.DataFrame:
        """
        Save the statistics record into the dataframe with all the metrics collected
        :param start_time: When the record began
        :return: Dataframe that contains all the metrics stored for the executed run
        """
        new_data = pd.DataFrame(
            {
                'qt_l_click': self.qt_l_click,
                'qt_r_click': self.qt_r_click,

                'total_time_l_click': f'{self.total_time_l_click :.2f}',
                'total_time_r_click': f'{self.total_time_r_click :.2f}',

                'avg_time_l_click': f'{(self.total_time_l_click / (self.qt_r_click if self.qt_r_click > 0 else 1)):.2f}',
                'avg_time_r_click': f'{(self.total_time_r_click / (self.qt_r_click if self.qt_r_click > 0 else 1)):.2f}',

                'l_mov_count': self.l_mov_count,
                'r_mov_count': self.r_mov_count,
                'u_mov_count': self.u_mov_count,
                'd_mov_count': self.d_mov_count,

                'total_hor_dist': self.tot_hor_dist,
                'total_ver_dist': self.tot_ver_dist,

                'total_hor_time': f'{self.tot_hor_time:.2f}',
                'total_ver_time': f'{self.tot_ver_time:.2f}',

                'total_dist_l_mov': self.total_dist_l_mov,
                'total_dist_r_mov': self.total_dist_r_mov,
                'total_dist_u_mov': self.total_dist_u_mov,
                'total_dist_d_mov': self.total_dist_d_mov,

                'total_time_l_mov': f'{self.total_time_l_mov:.2f}',
                'total_time_r_mov': f'{self.total_time_r_mov:.2f}',
                'total_time_u_mov': f'{self.total_time_u_mov:.2f}',
                'total_time_d_mov': f'{self.total_time_d_mov:.2f}',

                'avg_time_l_mov': f'{(self.total_time_l_mov / (self.l_mov_count if self.l_mov_count > 0 else 1)):.2f}',
                'avg_time_r_mov': f'{(self.total_time_r_mov / (self.r_mov_count if self.r_mov_count > 0 else 1)):.2f}',
                'avg_time_u_mov': f'{(self.total_time_u_mov / (self.u_mov_count if self.u_mov_count > 0 else 1)):.2f}',
                'avg_time_d_mov': f'{(self.total_time_d_mov / (self.d_mov_count if self.d_mov_count > 0 else 1)):.2f}',

                'hor_speed': f'{(self.tot_hor_dist / self.tot_hor_time if self.tot_hor_time > 0 else 1):.2f}',
                'ver_speed': f'{(self.tot_ver_dist / self.tot_ver_time if self.tot_ver_time > 0 else 1):.2f}',

                'l_speed': f'{(self.total_dist_l_mov / self.total_time_l_mov if self.total_time_l_mov > 0 else 1):.2f}',
                'r_speed': f'{(self.total_dist_r_mov / self.total_time_r_mov if self.total_time_r_mov > 0 else 1):.2f}',
                'u_speed': f'{(self.total_dist_u_mov / self.total_time_u_mov if self.total_time_u_mov > 0 else 1):.2f}',
                'd_speed': f'{(self.total_dist_d_mov / self.total_time_d_mov if self.total_time_d_mov > 0 else 1):.2f}',

                'total_capture_time': f'{(time.time() - start_time) :.2f}'

            }, index=[len(self.mouse_stats_dataframe)]
        )

        self.mouse_stats_dataframe = pd.concat([self.mouse_stats_dataframe, new_data],
                                               ignore_index=True
                                               )

        return self.mouse_stats_dataframe

    def __click_status(self):
        """
        Check if a click is performed and record it on the dataframe
        """
        if click_status_changed(win32api.GetKeyState(0x01), self.l_click):
            if is_pressed(win32api.GetKeyState(0x01)):
                self.delta_left_click = time.time()
                self.l_click = True
            else:
                self.delta_left_click = time.time() - self.delta_left_click
                self.total_time_l_click += self.delta_left_click
                self.qt_l_click += 1
                self.l_click = False

        if click_status_changed(win32api.GetKeyState(0x02), self.r_click):
            if is_pressed(win32api.GetKeyState(0x02)):
                self.delta_right_click = time.time()
                self.r_click = True
            else:
                self.delta_right_click = time.time() - self.delta_right_click
                self.total_time_r_click += self.delta_right_click
                self.qt_r_click += 1
                self.r_click = False

    def __movement_status(self,
                          old_position: tuple,
                          current_position: tuple
                          ):
        """
        Check if the mouse is moving and, if it is, which position
        :param old_position: Where the mouse was on the last interaction
        :param current_position: Where the mouse is on the current interaction
        """
        x_old_position, y_old_position = old_position
        x_current_position, y_current_position = current_position

        if movement_status_changed(x_old_position,
                                   x_current_position,
                                   self.is_moving_hor
                                   ):
            if x_old_position != x_current_position:
                self.delta_hor_mov = time.time()
                self.mov_hor_dist = x_old_position
                self.is_moving_hor = True
            else:
                self.delta_hor_mov = time.time() - self.delta_hor_mov
                self.mov_hor_dist = x_current_position - self.mov_hor_dist
                self.tot_hor_dist += abs(self.mov_hor_dist)
                self.tot_hor_time += self.delta_hor_mov
                self.is_moving_hor = False
                self.__set_hor_dist(self.mov_hor_dist)

        if movement_status_changed(y_old_position,
                                   y_current_position,
                                   self.is_moving_ver
                                   ):
            if y_old_position != y_current_position:
                self.delta_ver_mov = time.time()
                self.mov_ver_dist = y_old_position
                self.is_moving_ver = True
            else:
                self.delta_ver_mov = time.time() - self.delta_ver_mov
                self.mov_ver_dist = y_current_position - self.mov_ver_dist
                self.tot_ver_dist += abs(self.mov_ver_dist)
                self.tot_ver_time += self.delta_ver_mov
                self.is_moving_ver = False
                self.__set_ver_dist(self.mov_ver_dist)

    def start_data_reading(self) -> pd.DataFrame:
        """
        Control the samples collection and steps that should be analysed.
        Check if click is being performed or the mouse is currently moving
        :return: Dataframe with the samples collected for every event and Dataframe with the statistics collected for the entire run
        """

        old_position = pgui.position()
        delta_start = time.time()

        for count in range(self.sample_size):
            current_position = pgui.position()

            self.__click_status()
            self.__movement_status(old_position=old_position,
                                   current_position=current_position
                                   )

            self.new_mouse_event_record(delta_start, current_position)

            old_position = current_position
            time.sleep(self.sample_collection_interval)

        # FINAL DATA
        self.new_mouse_stats_record(delta_start)
        return self.mouse_event_dataframe, self.mouse_stats_dataframe

    def run(self,
            path: str = './record_data',
            task: str = 'simple'
            ):
        """
        Execution method to simplify the usage. Call the method to start record a basic example with 2000 sample collects with a hundredth second interval
        :param path: Where the file should be saved
        :param task: Task recorded, used to name the file stored
        """
        df_mouse_event, df_mouse_stats = self.start_data_reading()

        save_data(data=df_mouse_event,
                  path=path,
                  file=f"{task.replace(' ', '_')}_mouse_event.csv"
                  )

        save_data(data=df_mouse_stats,
                  path=path,
                  file=f"{task.replace(' ', '_')}_mouse_stats.csv"
                  )

        time.sleep(self.interval_between_collection)


if __name__ == '__main__':
    data_gen = record(sample_size=100)

    steps = 1

    for step in range(steps):
        data_gen.run()

        print(f'step {step + 1} of {steps}')
