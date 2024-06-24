import plotly.express as px


def display_bar_plot(display_data, color_col_name: str, title: str, png_path: str = None, html_path: str = None):
    """
    Displays and optionally saves a bar plot of the annual number of satellite launches.

    This function generates a bar plot using the Plotly library to visualize the annual number of satellite launches,
    with the bars colored according to a specified column. The plot can be displayed in a web browser and optionally saved
    as a PNG image and/or an HTML file.

    Args:
        display_data (pd.DataFrame): The DataFrame containing the data to be displayed, including 'launch_year' and 'launch_count' columns.
        color_col_name (str): The name of the column used to color the bars.
        title (str): The title of the plot.
        png_path (str, optional): The file path to save the plot as a PNG image. If None, the plot is not saved as a PNG.
        html_path (str, optional): The file path to save the plot as an HTML file. If None, the plot is not saved as an HTML file.

    Returns:
        None
    """
    fig = px.bar(display_data, x='launch_year', y='launch_count', color=color_col_name,
                 title=title,
                 labels={'launch_year': 'Year',
                         'launch_count': 'Number of Launches'},
                 color_discrete_sequence=['#2c57c9', '#8d50d0', '#c95574', '#0b786c', '#ab7310', '#ca78cc'], opacity=0.8)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ), legend_title=None, template='plotly_dark')
    # Show the plot
    fig.show()
    # Save as PNG
    if png_path:
        fig.write_image(png_path, engine="kaleido")
    # Save as HTML
    if html_path:
        fig.write_html(html_path)


def display_line_plot(display_data, x_col: str, y_col: str, labels: dict, color_sequence: list[str], title: str, color_col: str = None, png_path: str = None, html_path: str = None):
    """
    Displays and optionally saves a line plot.

    This function generates a line plot using the Plotly library to visualize data over a specified x-axis and y-axis.
    The plot can be colored based on a specified column, and it can be displayed in a web browser. Additionally, it can
    be optionally saved as a PNG image and/or an HTML file.

    Args:
        display_data (pd.DataFrame): The DataFrame containing the data to be displayed.
        x_col (str): The column name to be used for the x-axis.
        y_col (str): The column name to be used for the y-axis.
        labels (dict): A dictionary for labeling the axes.
        color_sequence (list[str]): A list of colors to be used for the lines.
        title (str): The title of the plot.
        color_col (str, optional): The column name used to color the lines. If None, lines are not colored by any specific column.
        png_path (str, optional): The file path to save the plot as a PNG image. If None, the plot is not saved as a PNG.
        html_path (str, optional): The file path to save the plot as an HTML file. If None, the plot is not saved as an HTML file.

    Returns:
        None
    """
    fig = px.line(
        display_data,
        x=x_col,
        y=y_col,
        labels=labels,
        title=title,
        color=color_col,
        color_discrete_sequence=color_sequence)

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ), legend_title=None, template='plotly_dark'
    )
    fig.update_traces(line={'width': 3})

    # Show the plot
    fig.show()

    # Save as PNG
    if png_path:
        fig.write_image(png_path, engine="kaleido")

    # Save as HTML
    if html_path:
        fig.write_html(html_path)
