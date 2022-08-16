"""
File: babygraphics.py
Name: Chin
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 500
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    year = YEARS
    margin = GRAPH_MARGIN_SIZE

    year_count = len(year)
    x_coordinate = margin + year_index * (width - 2 * margin) / year_count

    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #
    w = CANVAS_WIDTH
    h = CANVAS_HEIGHT
    margin = GRAPH_MARGIN_SIZE

    # Draw margin line
    canvas.create_line(margin, margin, w-margin, margin, width=1, fill='gray')
    canvas.create_line(margin, h-margin, w-margin, h-margin, width=1, fill='gray')

    # Draw vertical line
    for i in range(len(YEARS)):
        x_cord = get_x_coordinate(w, i)
        canvas.create_line(x_cord, 0, x_cord, h, width=1, fill='gray')
        canvas.create_text(x_cord, h-margin, text=YEARS[i], anchor='nw')


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #

    w = CANVAS_WIDTH
    h = CANVAS_HEIGHT
    margin = GRAPH_MARGIN_SIZE
    years = YEARS
    color = COLORS

    for name in lookup_names:
        x = []
        y = []
        rank_text = []

        for i in range(len(years)):
            if str(years[i]) not in name_data[name]:                         # 處理排名
                rank = 1000
                rank_text.append('*')
            else:
                rank = int(name_data[name][str(years[i])])                   # 新增排名文字
                rank_text.append(rank)

            y_coordinate = int(((rank * (h - 2 * margin)) / 1000) + margin)  # 處理 y 座標 (等分)
            x.append(get_x_coordinate(w, i))                                 # Add x coord. in list by years.
            y.append(y_coordinate)                                           # Add y coord. in list by years.

        for i in range(len(years)):             # 這邊應該可改成 python comprehension (吧?)
            if i == len(years)-1:
                canvas.create_line(x[i], y[i], x[i], y[i], width=1, fill=color[lookup_names.index(name) % 4])
            else:
                canvas.create_line(x[i], y[i], x[i+1], y[i+1], width=1, fill=color[lookup_names.index(name) % 4])
            canvas.create_text(x[i], y[i], text=f"{name} {rank_text[i]}", fill=color[lookup_names.index(name) % 4], anchor='sw')

# main() code is provided, feel free to read through it but DO NOT MODIFY


def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
