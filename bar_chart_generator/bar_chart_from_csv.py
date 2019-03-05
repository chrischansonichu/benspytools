#!/usr/bin/env python3
#
#
"""
This script will generate a PNG image of a bar chart from a csv file of data, specified by the user in the command line
"""
import csv
import os

from PIL import Image, ImageDraw

__author__ = 'bdhimes@me.com'


def get_csv_location():
    """
    Prompts the user to enter the file path of the csv file that contains the data to be processed. Loops until a valid
    file path is entered or the user exits the program.
    :return:
    """
    csv_location = input('Please enter the full filepath of the csv file you would like to process into a bar chart:\n')
    if not os.path.exists(csv_location):
        print("Sorry, that does not appear to be a valid file path. Please try again.\nIf you would like to exit"
              "the program, please press Ctrl-C.")
        get_csv_location()
    else:
        return csv_location


def add_text_to_image(image, xy_start, text):
    """
    Adds text to an image
    :param image: PIL image to be drawn upon
    :param text: desired text to add
    :param xy_start: (x,y) pixel location for top-left the text to be written
    """
    draw = ImageDraw.Draw(image)
    draw.text(xy_start, text)


def draw_graph_key(image, color_title):
    """
    Draws a key in the top-right corner of the graph
    :param image: image to be drawn upon
    :param color_title: dict containing the color of the bar (in str hex), and the str of what it represents
    """
    top_corner, _ = image.size  # gets the x coordinate of the top-right corner of the image
    key_height = len(color_title) * 30  # determines the height of the key by multiplying the number of entries by 30 px
    draw = ImageDraw.Draw(image)
    # draws an empty box with a white outline
    draw.rectangle([(top_corner-120, 5), (top_corner-10, key_height)], outline='#ffffff')
    for item, d in enumerate(color_title.items(), 1):
        key, value = d
        # draws a short rectangle of the color
        draw.rectangle([(top_corner-110, item * 15), (top_corner-100, item * 15 + 10)], fill=key)
        # labels the color with what it represents
        draw.text((top_corner-95, item * 15), value)


def draw_bar(image, xy_start, px_width, px_height, color):
    """
    Draws a bar on an image
    :param image: PIL image object to draw on
    :param xy_start: tuple giving the x,y coordinates of where to start drawing the bar
    :param px_width: desired width of the bar, in px
    :param px_height: desired height of the bar, in px
    :param color: int color of the bar to be drawn
    """
    draw = ImageDraw.Draw(image)
    w, h = xy_start
    draw.rectangle([xy_start, (w+px_width, h-px_height)], fill=color)


def draw_graph_axis(image, highest_number, lowest_number, x_title='', y_title=''):
    """
    Draws the graph axis on an image
    :param image: PIL image to be drawn upon
    :param highest_number: int highest number that will be used on the x-axis
    :param lowest_number: int highest number that will be used on the x-axis
    :param x_title: str of the title of the x-axis
    :param y_title: str of the title of the y-axis
    :return: tuple containing the 0 y-axis pixel position, highest-, lowest-pixel positions, scale factor
    """
    w, h = image.size
    draw = ImageDraw.Draw(image)
    draw.line([80, 30, 80, h-100], fill=128, width=10)  # draw x-axis
    draw.text([20, 30], str(highest_number))  # label top of x-axis with highest number
    draw.text([20, (30 + (h-100)) // 2], x_title)  # title the x-axis
    draw.line([80, h-100, w-100, h-100], fill=128, width=10)  # draw y-axis
    draw.text([w//2, h-30], str(y_title))  # title y-axis
    # if the lowest number is greater than 0, begins the graph at 0
    if lowest_number >= 0:
        draw.text([20, h-100], '0')
        lowest_number = 0
    x_pixel_height = (h - 100) - 30  # gets the height of the x-axis in pixels
    x_int_height = highest_number - lowest_number  # gets the height of the x-axis in integers
    scale_factor = x_pixel_height / x_int_height  # generates a scale factor of integer increments to drawn pixels
    if lowest_number < 0:
        starting_y = h-110 - (lowest_number * (-1) * scale_factor)
        draw.text([20, starting_y], '0')
        draw.text([20, h-100], str(lowest_number))
    else:
        starting_y = h-110
    return int(starting_y), 30, h-100, scale_factor


def main():
    csv_location = get_csv_location()
    print("Great! Thanks.")
    delimiter_question = input("Is this csv file delimited by anything other than a comma (,)?\n(y/n)\n").lower()
    delimiter = ',' if not delimiter_question.startswith('y') else input('What is the delimiter used?\n')
    with open(csv_location) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        csv_data = list(reader)
    entries = len(csv_data)

    try:
        # makes a flattened list of all of the non-year data
        flat_list = [int(i) for l in map(lambda x: list(x.values())[1:], csv_data) for i in l]
    except ValueError:
        print("It appears your csv includes non-numeric values, and therefore cannot be plotted.")
        raise

    image = Image.new('RGB', ((entries + 1) * 200, 1000))
    starting_y, x_height, x_depth, scale_factor = draw_graph_axis(image,
                                                                  max(flat_list),
                                                                  min(flat_list),
                                                                  '',
                                                                  next(iter(csv_data[0].keys())))

    for entry_number, entry_data in enumerate(csv_data, 1):
        y, p, e = entry_data.values()
        # labels the bar set
        add_text_to_image(image, (int(25 + entry_number * 150), x_depth + 30), y)
        # draws the bars
        draw_bar(image, (int(entry_number * 150), starting_y), 50, int(int(p) * scale_factor), '#ff0000')
        draw_bar(image, (int(50 + entry_number * 150), starting_y), 50, int(int(e) * scale_factor), '#0000ff')
        # on the last loop, draws the graph's key in the top-right corner
        if entry_number == len(csv_data):
            _, a, b = entry_data.keys()
            draw_graph_key(image, {'#ff0000': a, '#0000ff': b})
    # displays the image (saved to /tmp/*.PNG while displaying)
    image.show()


if __name__ == '__main__':
    main()
