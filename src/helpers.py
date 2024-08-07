# helpers.py
import plotly.express as px


def get_bar_plot(display_data, color_col_name, title):
    """
    Generate a bar plot using Plotly.

    Args:
        display_data (pd.DataFrame): The data to be plotted.
        color_col_name (str): The column name to be used for coloring the bars.
        title (str): The title of the plot.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly Figure object representing the bar plot.
    """
    fig = px.bar(display_data, x='launch_year', y='launch_count', color=color_col_name,
                 title=title, labels={'launch_year': 'Year',
                                      'launch_count': 'Number of Launches'},
                 color_discrete_sequence=['#2c57c9', '#8d50d0', '#c95574', '#0b786c', '#ab7310', '#ca78cc'], opacity=0.8)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      font=dict(family="Courier New, monospace", size=18), legend_title=None, template='plotly_dark')
    return fig


def get_line_plot(display_data, x_col, y_col, labels, color_sequence, title, color_col=None):
    """
    Generate a line plot using Plotly.

    Args:
        display_data (pd.DataFrame): The data to be plotted.
        x_col (str): The column name to be used for the x-axis.
        y_col (str): The column name to be used for the y-axis.
        labels (dict): A dictionary mapping column names to axis labels.
        color_sequence (list of str): A list of colors to be used for the lines.
        title (str): The title of the plot.
        color_col (str, optional): The column name to be used for coloring the lines. Default is None.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly Figure object representing the line plot.
    """
    fig = px.line(display_data, x=x_col, y=y_col, labels=labels, title=title,
                  color=color_col, color_discrete_sequence=color_sequence)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      font=dict(family="Courier New, monospace", size=18), legend_title=None, template='plotly_dark')
    fig.update_traces(line={'width': 3})
    return fig


def display_plot(fig, png_path=None, html_path=None):
    """
    Display and optionally save a Plotly figure.

    Args:
        fig (plotly.graph_objs._figure.Figure): The Plotly figure to be displayed and saved.
        png_path (str, optional): The file path to save the plot as a PNG image. Default is None.
        html_path (str, optional): The file path to save the plot as an HTML file. Default is None.

    Returns:
        None
    """
    fig.show()
    if png_path:
        fig.write_image(png_path, engine="kaleido", width=1080, height=720)
    if html_path:
        fig.write_html(html_path, full_html='False', include_plotlyjs='cdn')
