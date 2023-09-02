import numpy
import pandas
import flet as ft
from consts import colors


class generate_statistics_graph:
    def __init__(self,
                 data: pandas.DataFrame | list = None,
                 x: list[int] | list[float] | numpy.ndarray = None,
                 y: list[int] | list[float] | numpy.ndarray = None,
                 chart_data=None
                 ):
        """
        Class used for plot construction, provides a Linear plot or a Bar plot of the information passed to it.
        Basically add subplot into a board returning a complete image with multiple lines or bars to visualize data in
        an easier way.
        :param data: Dataframe or List with tuples of (X,Y) Reference for a LinePlot, you can also pass A Vector with
        all the limits for the bar plot
        :param x: Data for the X axis (Width)
        :param y: Data for the Y axis (Height)
        :param chart_data: You can inform it if you already have a plot and want to add more Data, use None if you want
        to start a new board
        """
        if chart_data is None:
            chart_data = []
        self.data = data
        self.x = x
        self.y = y
        self.chart_data = chart_data
        self.chart = None
        self.__init_data()

    def __add_line_data(self,
                        x: list[int] | list[float] | numpy.ndarray = None,
                        y: list[int] | list[float] | numpy.ndarray = None,
                        color: str = None,
                        below_line_bgcolor: bool = False,
                        stroke_width: int | float = 4,
                        curved: bool = True,
                        stroke_cap_round: bool = True
                        ):
        """
        Private method to add subplots into the figure as linear data
        :param x: Data for the X axis (Width)
        :param y: Data for the Y axis (Height)
        :param color: Color for the line
        :param below_line_bgcolor: Make a colored area below the line till the bottom
        :param stroke_width: Width of the stroke of the line
        :param curved: Is a Curved line or Straight one between the marks
        :param stroke_cap_round: Set a rounded line cap
        :return: return an chartData array with all line plots inserted
        """
        self.chart_data.append(
            ft.LineChartDataPoint(
                x,
                y
            ),
            color=color,
            below_line_bgcolor=ft.colors.with_opacity(0.2, color) if below_line_bgcolor else None,
            stroke_width=stroke_width,
            curved=curved,
            stroke_cap_round=stroke_cap_round
        )
        return self.chart_data

    def __add_bar_data(self,
                       max_value: int | float,
                       min_value: int | float = 0,
                       width: int | float = 40,
                       color: str = None,
                       tooltip: str = "",
                       border_radius: int | float = 0
                       ):
        """
        Private method to add subplots into the figure as bar plots
        :param max_value: the max value of this bar
        :param min_value: the min value of this bar, for default, 0
        :param width: the thickness of the bar
        :param color: the color of the bar
        :param tooltip: label for the plot
        :param border_radius: corner radius, make rounded corners
        :return: return an chartData array with all bar plots inserted
        """
        if color is None:
            colors_list = [value for name, value in vars(colors).items() if not name.startswith('_')]
            color = colors_list[len(self.chart_data) % len(colors_list)]
        self.chart_data.append(
            ft.BarChartGroup(
                x=len(self.chart_data),
                bar_rods=[
                    ft.BarChartRod(from_y=min_value,
                                   to_y=max_value,
                                   width=width,
                                   color=color,
                                   tooltip=tooltip,
                                   border_radius=border_radius,
                                   )
                ]
            )
        )

        return self.chart_data

    def __init_data(self):
        """
        The method is only used to adjust the data into the dataframe used for generating the graph marks.
        The user should inform a DataFrame with the respective columns for X and Y axis.
        If the user wants, they can use as separated vectors, X and Y, that will fit the DataFrame later, into this
        method.
        It is possible to inform only Y vector for the Bar plot, to make it, use the DataFrame or inform X label as None
        """
        if self.chart_data is not None:
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

                # if 'y' not in self.data.columns:
                #    if type(self.y) != str:
                #        raise Exception('The Y parameter should contain the column name for the Y axis.')
                #    self.data['y'] = self.data[self.y]

    def linear(self,
               below_line_bgcolor: bool = False
               ):
        """
        The method is used to iterate every single line into the DataFrame calling and setting up every single mark
        into the graph. The marks should Respect the Cartesian pattern, containing X and Y references.
        :param below_line_bgcolor: Make a colored area below the line till the bottom
        :return: ChartData array containing every graph mark.
        """
        for index, row in self.data.iterrows():
            self.__add_line_data(row['x'], row['y'])

        return self.chart_data

    def bar(self):
        """
        The method is used to iterate every single line into the DataFrame calling and setting up every single mark
        into the graph. The marks should Respect the value of the Bar.
        :return: ChartData array containing every graph mark.
        """
        aux_data = self.data.mean(axis=0, skipna=True)
        bottom_labels = []
        count = 0
        for index, value in aux_data.items():
            if value is not None:
                self.__add_bar_data(max_value=round(float(value), 2),
                                    tooltip=f'{index}: {round(float(value), 2)}',
                                    )
                bottom_labels.append(
                    ft.ChartAxisLabel(value=count, label=ft.Container(ft.Text(index), padding=0))
                )
                count += 1

        self.chart = self.__place_to_chart(aux_data, bottom_labels=bottom_labels)

        return self.chart_data, self.chart

    def __place_to_chart(self, data,
                         bottom_labels: list = None,
                         left_labels: list = None
                         ):
        """
        Method should be used for the final plot of the graph, setting up the configuration of the plot with labels,
        color and grid lines.
        :param data: Data to be inserted into the Chart variable, should be used for plotting the image
        :param bottom_labels: List of ft.ChartAxisLabel for the bottom axis (X), must be formatted in ft.ChartAxisLabel
        style.
        :param left_labels:  List of ft.ChartAxisLabel for the Left Axis (Y), must be formatted in ft.ChartAxisLabel
        style.
        :return: Chart with the image containing the marks and references for the graph
        """
        self.chart = ft.BarChart(
            self.chart_data,
            interactive=True,
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            bottom_axis=ft.ChartAxis(
                labels=bottom_labels
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=data.max(),
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=50
            ),
            expand=True,
        )
        return self.chart
