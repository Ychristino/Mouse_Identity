import pandas as pd
import os

import consts.plot
from consts import paths


def get_dataframe(path: str = None,
                  file: str = None
                  ) -> pd.DataFrame:
    """
    Get file data and read it as a Pandas.DataFrame
    :param path: Path where the file is located
    :param file: Name of the file
    :return: Pandas.Dataframe with the containing Data
    """
    return pd.read_csv(f'{path}/{file}', sep=';')


def get_graph_data(is_main: bool = True,
                   user_name: str = None,
                   game_name: str = None,
                   graph_type=None
                   ) -> pd.DataFrame:
    """
    Get a Graph Data. Used to read graphs available on the Consts.Graphs file, such as Heatmap, Mouse Statistics and Mouse Events.
    :param is_main: Inform if data should be read from the Main user Folder
    :param user_name: If not the Main User, should inform which Suspect to read
    :param game_name: Name of the Game that should be read
    :param graph_type: Type of the Graph, available on the Consts.Graphs file, such as Heatmap, Mouse Statistics and Mouse Events.
    :return: Pandas.Dataframe with the filtered Data for the plot type selected
    """
    data = pd.DataFrame

    match graph_type:
        case consts.plot.MOUSE_STATS:

            data = __get_stats_dataframe(is_main=is_main,
                                         user_name=user_name,
                                         game_name=game_name
                                         )
        case consts.plot.HEATMAP:
            data = __get_event_dataframe(is_main=is_main,
                                         user_name=user_name,
                                         game_name=game_name
                                         )
            data = data[['x','y','width','height']]
        case consts.plot.CLICK_MAP:
            data = __get_event_dataframe(is_main=is_main,
                                         user_name=user_name,
                                         game_name=game_name
                                         )
            data = data[['x','y','l_click','r_click','width','height']]
            data = data.query('l_click == 1 or r_click == 1')
        case _:
            raise Exception('Invalid Graph Type.')

    return data


def __get_event_dataframe(is_main: bool = True,
                          user_name: str = None,
                          game_name: str = None
                          ) -> pd.DataFrame:
    """
    Internal Function to get the Event Data frame.
    :param is_main: Inform if data should be read from the Main user Folder
    :param user_name: If not the Main User, should inform which Suspect to read
    :param game_name: Name of the Game that should be read
    :return: Pandas.Dataframe with the Event Data from the Main User or the Suspect
    """
    if is_main:
        path = consts.paths.USER_EVENT
    else:
        path = f'{consts.paths.SUSPECT_EVENT}/{user_name}'

    file = game_name.replace(' ', '_')

    return pd.read_csv(f'{path}/{file}_mouse_event', sep=';')


def __get_stats_dataframe(is_main: bool = True,
                          user_name: str = None,
                          game_name: str = None
                          ) -> pd.DataFrame:
    """
    Internal Function to get the Statistics Data frame.
    :param is_main: Inform if data should be read from the Main user Folder
    :param user_name: If not the Main User, should inform which Suspect to read
    :param game_name: Name of the Game that should be read
    :return: Pandas.Dataframe with the Statistics Data from the Main User or the Suspect
    """
    if is_main:
        path = consts.paths.USER_STATS
    else:
        path = f'{consts.paths.SUSPECT_STATS}/{user_name}'

    file = game_name.replace(' ', '_')

    return pd.read_csv(f'{path}/{file}_mouse_stats', sep=';')


def save_data(data: pd.DataFrame | str,
              path: str = None,
              file: str = None,
              override: bool = True
              ) -> None:
    """
    Save the data at the informed locale. Used make a consistent way to save the data.
    :param path: Path where the file is located
    :param file: Name of the file
    :param data: Data that has to be saved
    :param override: True if you want to override existing data with the same name
    """
    if not os.path.exists(path):
        os.makedirs(path)

    if isinstance(data, pd.DataFrame):
        __save_dataframe(path=path,
                         file=file,
                         data=data,
                         override=override
                         )
    elif isinstance(data, str):
        __save_string(path=path,
                      file=file,
                      data=data,
                      override=override
                      )


def __save_dataframe(data: pd.DataFrame,
                     path: str = None,
                     file: str = None,
                     override: bool = True
                     ) -> None:
    """
    Internal function to save data as a DataFrame Format
    :param data: Data that has to be saved
    :param path: Path where the file is located
    :param file: Name of the file
    :param override: True if you want to override existing data with the same name
    """
    if override:
        data.to_csv(f'{path}/{file}', mode='w', index=False, sep=';')
    else:
        if os.path.exists(f'{path}/{file}'):
            data.to_csv(f'{path}/{file}', mode='a', index=False, sep=';', header=None)
        else:
            data.to_csv(f'{path}/{file}', mode='a', index=False, sep=';')


def __save_string(data: str,
                  path: str = None,
                  file: str = None,
                  override: bool = True
                  ) -> None:
    """
    Internal function to save data as a String Format
    :param data: Data that has to be saved
    :param path: Path where the file is located
    :param file: Name of the file
    :param override: True if you want to override existing data with the same name
    """
    if override:
        file = open(f'{path}/{file}', 'w')
    else:
        file = open(f'{path}/{file}', 'a')

    file.writelines(data)
