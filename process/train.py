import os

import Consts.Paths as Paths
import Consts.Games as Games
import Consts.Models as Models
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Models import Linear, Gaussian, SVC, Tree


def read_input_data(folder ='./',
                    game 	= None,
                    log  	= False
                    ):

    dict_data = pd.DataFrame()

    if game is not None:
        game = game.replace(' ', '_')

    for file in os.listdir(folder):
        if log:
            print(f'reading {folder}/{file}')

        if game is not None:
            if game in file:

                if log:
                    print(f'adding to data frame...')

                dict_data = pd.concat([dict_data, pd.read_csv(f'{folder}/{file}', sep=';')], ignore_index=False)
        else:
            if log:
                print(f'adding to data frame...')

            dict_data = pd.concat([dict_data, pd.read_csv(f'{folder}/{file}', sep=';')], ignore_index=False)

    return dict_data

def run(lst_models     = None,
        class_names    = None,
        selected_game  = None,
        ):

    # Execution Parameters
    SEED = 1563
    np.random.seed(SEED)

    # Variables
    model_data = pd.DataFrame()

    # Control Variables
    run_linear = (Models.LINEAR   in lst_models)
    run_gauss  = (Models.GAUSSIAN in lst_models)
    run_svc    = (Models.SVC 	  in lst_models)
    run_tree   = (Models.TREE 	  in lst_models)

    # Populating DataFrame with all selected files
    for count in range(len(class_names)):

        path = Paths.USER_STATS if class_names[count] == 'User' else Paths.SUSPECT_STATS.replace('{SUSPECT_NAME}', class_names[count])

        new_data = read_input_data(folder=path, game=selected_game, log=False)
        new_data['class'] = class_names[count]

        model_data = pd.concat([model_data, new_data], ignore_index=False)

    model_data = model_data.dropna()

    # Filtering Util Columns Only
    x = model_data.drop(['class', 'total_capture_time'], axis=1)
    y = model_data['class']

    # Create Selected Models
    if run_linear:
        linear = Linear.Linear()
        linear = linear.execute(x_data=x, y_data=y, filename=f'{Models.LINEAR}_result')

    if run_gauss:
        gauss = Gaussian.Gaussian()
        gauss = gauss.execute(x_data=x, y_data=y, filename=f'{Models.GAUSSIAN}_result')

    if run_svc:
        svc = SVC.SVC()
        svc = svc.execute(x_data=x, y_data=y, filename=f'{Models.SVC}_result')

    if run_tree:
        tree = Tree.Tree()
        tree = tree.execute(x_data=x, y_data=y, filename=f'{Models.TREE}_result')

if __name__ == "__main__":
    run()
