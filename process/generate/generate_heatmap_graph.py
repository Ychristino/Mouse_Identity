import numpy as np
import pandas as pd
import cv2
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt


class generate_heatmap_graph:
    colors = [(0, 0, 1), (0, 1, 1), (0, 1, 0.75), (0, 1, 0), (0.75, 1, 0),
              (1, 1, 0), (1, 0.8, 0), (1, 0.7, 0), (1, 0, 0)]

    cm = LinearSegmentedColormap.from_list('sample', colors)

    def __init__(self,
                 data: list[int] | list[float] | np.ndarray | pd.DataFrame = None,
                 x: list[int] | list[float] | np.ndarray | str = None,
                 y: list[int] | list[float] | np.ndarray | str = None,
                 screen_width_resolution: int = 1920,
                 screen_height_resolution: int = 1080,
                 screen_width_proportion: int = None,
                 screen_height_proportion: int = None
                 ):
        """
        Class used for plot construction, provides Heatmap plot of the information passed to it.
        Basically reads a Pandas Dataframe and group it for the same occurrences. With the X and Y Labels and the count
        of the occurrences of each value, the Plot canvas is built.
        :param data: Data with the X and Y Values. The data will be adjusted by internal methods to fit its patterns.
        :param x: List of all the X values, the internal processes will use it to fit to the corresponding Y value, so have to be on the same shape of Y value.
        :param y: List of all the Y values, the internal processes will use it to fit to the corresponding X value, so have to be on the same shape of X value.
        :param screen_width_resolution: The value of the screen width resolution, used to draw the complete area of action to the graph.
        :param screen_height_resolution: The value of the screen height resolution, used to draw the complete area of action to the graph.
        :param screen_width_proportion: The width proportion of the screen, used to rescale the image to smaller graphs like 16:9 resolution or 32:18. The default value is the same of the screen_width_resolution, to have a 1:1 proportion with it.
        :param screen_height_proportion: The height proportion of the screen, used to rescale the image to smaller graphs like 16:9 resolution or 32:18. The default value is the same of the screen_heigth_resolution, to have a 1:1 proportion with it.
        """
        self.data = data
        self.x = x
        self.y = y
        self.screen_width_resolution = screen_width_resolution
        self.screen_height_resolution = screen_height_resolution
        self.screen_width_proportion = screen_width_proportion
        self.screen_height_proportion = screen_height_proportion
        self.__init_data()

    def __init_data(self):
        """
        The method is only used to adjust the data into the dataframe used for generating the graph marks.
        The user should inform a DataFrame with the respective columns for X and Y axis.
        If the user wants, they can use as separated vectors, X and Y, that will fit the DataFrame later, into this
        method.
        It is possible to inform only Y vector for the Bar plot, to make it, use the DataFrame or inform X label as None
        """
        if self.screen_width_proportion is None:
            self.screen_width_proportion = self.screen_width_resolution
        if self.screen_height_proportion is None:
            self.screen_height_proportion = self.screen_height_resolution

        if self.data is None:
            if (self.x is not None and self.y is not None) and (len(self.x) != len(self.y)):
                raise Exception('The length of the X and Y axis are divergent. You may have to adjust your data '
                                'to attend the cartesian pattern (X,Y)')

            elif len(self.x) > 0:
                self.data['x'] = self.x

            elif len(self.y) > 0:
                self.data['y'] = self.y
            else:
                raise Exception('No data Record was informed. You should consider passing it.')
        else:
            if 'x' not in self.data.columns and self.x is not None:
                if type(self.x) != str:
                    raise Exception('The X parameter should contain the column name for the X axis.')
                self.data['x'] = self.data[self.x]

            if 'y' not in self.data.columns:
                if type(self.y) != str:
                    raise Exception('The Y parameter should contain the column name for the Y axis.')
                self.data['y'] = self.data[self.y]

        return self.data

    def pre_processor(self,
                      data: list[int] | list[float] | np.ndarray | pd.DataFrame = None,
                      x: list[int] | list[float] | np.ndarray | str = None,
                      y: list[int] | list[float] | np.ndarray | str = None,
                      ):
        """
        Pre-processor used to build the correct shape of the data. The data will be set on the dataframe. The Dataframe
        contains an X and Y column with all the positions accessed. The values will be Grouped and the occurrences of
        each one will be counted on the respective Index. The graph size adjustment will Also happen in here, if the
        screen resolution is informed.
        :param data: Data with the X and Y Values. The data will be adjusted by internal methods to fit its patterns.
        :param x: List of all the X values, the internal processes will use it to fit to the corresponding Y value, so have to be on the same shape of Y value.
        :param y: List of all the Y values, the internal processes will use it to fit to the corresponding X value, so have to be on the same shape of X value.
        :return: Correct Dataframe with the X and Y position with the respective count for each coordinate.
        """
        if data is not None:
            self.data = data
            self.__init_data()
        elif x is not None and y is not None:
            self.x = x
            self.y = y
            self.__init_data()

        col_size = self.screen_width_resolution / self.screen_width_proportion
        row_size = self.screen_height_resolution / self.screen_height_proportion

        heatmap_dataframe = pd.DataFrame()

        heatmap_dataframe['x'] = self.data.x / col_size
        heatmap_dataframe['y'] = self.data.y / row_size

        heatmap_dataframe = heatmap_dataframe.groupby(heatmap_dataframe.columns.tolist(), as_index=False).size().astype(
            int)
        heatmap_dataframe = heatmap_dataframe.drop_duplicates()
        heatmap_dataframe = heatmap_dataframe.pivot_table(values='size', index='y', columns='x').replace(np.nan,
                                                                                                         0).astype(int)
        return heatmap_dataframe

    @staticmethod
    def set_filter(data,
                   kernel_width: int = 15,
                   kernel_height: int = 15,
                   sigma: int | float = 6
                   ):
        """
        Applies a GaussianBlur to the image. Used to show a more effective plot with a area of effect of each point.
        These area can be controlled by the parameters.
        The parameters will control a radius range for each coordinate, getting the value of the incidence based on the
        sigma parameter and the distance to the current mark.
        :param data: Data with the X and Y Values. The data will be adjusted by internal methods to fit its patterns.
        :param kernel_width: Width area of effect for the position. The elements present into these area of effect will be counted by his weight based of your distance to the reference point and the sigma value.
        :param kernel_height: Height area of effect for the position. The elements present into these area of effect will be counted by his weight based of your distance to the reference point and the sigma value.
        :param sigma: Controls a weight for the coordinates around. The coordinates around should be controlled by the Kernel Width and Height.
        :return: cv2.GaussianBlur Image with the applied filter
        """
        return cv2.GaussianBlur(data.to_numpy(dtype=np.uint8), (kernel_width, kernel_height), sigma)

    def generate_image(self,
                       title: str = None,
                       show_colorbar: bool = False
                       ):
        """
        Image generation. Built of the matplot Figure.
        :param title: Title of the Graph. Will be displayed upside the image.
        :param show_colorbar: Show the colorbar of the values and the corresponding color.
        :return: Figure based on Matplot.Pyplot lib
        """
        fig = plt.figure(figsize=(16,9),
                         frameon=True,
                         layout='tight',
                         dpi=100
                         )
        ax = fig.add_subplot()
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        plt.imshow(self.data, cmap=generate_heatmap_graph.cm)

        if show_colorbar:
            plt.colorbar()

        plt.title(title)

        return fig

    def generate(self):
        """
        Run all the necessary methods for the filter and plot of the image.
        :return: Figure from Matplot.Pyplot class. The returned value can be used to plot with plot.show from Matplot method or can be used to display the image into the flet frame.
        """
        self.data = self.pre_processor()
        self.data = self.set_filter(self.data)
        return self.generate_image()
