"""
File: stanCodoshop.py
Name: 
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
"""

import os
import sys
from simpleimage import SimpleImage
from time import time


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """

    # Average pixel return is a list, not pixel type in SimpleImage.
    # So use position to cal. , given pixel = [R,G,B] (dtype = list).

    dist = ((red - pixel.red)**2 + (green - pixel.green)**2 + (blue - pixel.blue)**2)**(1/2)
    return dist


def get_average(pixels):
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """

    # Set rgb
    rgb = [0, 0, 0]     # [Red, Green, Blue].

    for j in pixels:
        color = [j.red, j.green, j.blue]
        rgb[0] += color[0]
        rgb[1] += color[1]
        rgb[2] += color[2]

    # Sum value by RGB
    # for j in pixels:
    #     # for each pixels
    #     color = [j.red, j.green, j.blue]
    #     for i in range(3):
    #         rgb[i] += color[i]

    # Average / Division
    for i in range(3):
        rgb[i] = int(rgb[i] / len(pixels))

    return rgb

 # ---------------------------------------------------------------------------------------
    # list 不能使用 temp_red = temp_blue = temp_green = [] 的寫法，會被Python視為是同一個list。
    # 在 Append 的時候 會一直往後疊加:
    # Example:
    #    temp_red = temp_blue = []
    #    temp_red.append = j.red
    #    temp_blue.append = j.blue
    #    print(temp_red) = [255,255]
    #    print(temp_blue) = [255,255]   ← 這樣是錯的
    # ---------------------------------------------------------------------------------------

def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest "color distance", which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """

    pixels_avg = get_average(pixels)
    best_pixel = pixels[0]
    dist = float('Inf')
    for img in pixels:
        new_dist = get_pixel_dist(img, pixels_avg[0], pixels_avg[1], pixels_avg[2])
        if new_dist < dist:
            dist = new_dist
            best_pixel = img
    return best_pixel


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """

    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)

    # Time test
    time_list = []
    start = time()

    # ----- YOUR CODE STARTS HERE ----- #

    # Ver.1 - 先把所有的圖的點都抓出來，變成一張大表，再執行。(跑 monster 平均時間約 13秒)
    # print(hex(id(pixel_list))) -> 都在同一個記憶體位置，調用比較快 (ex. 0x1ce51239300)
    pixel_list = [[[]]]  # To Create a three-layer nested list, representing x, y,img_list
    for x in range(result.width):
        pixel_list.append([])
        for y in range(result.height):
            pixel_list[x].append([])
            pixel_list[x][y].append(SimpleImage.get_pixel(images[0], x, y))
            pixel_list[x][y].append(SimpleImage.get_pixel(images[1], x, y))
            pixel_list[x][y].append(SimpleImage.get_pixel(images[2], x, y))

    for x in range(result.width):
        for y in range(result.height):
            SimpleImage.set_pixel(result, x, y, get_best_pixel(pixel_list[x][y]))


    # Ver.2 -  用 3 個 for迴圈去執行，跑 monster 平均時間約 25秒
    # print(hex(id(pixel_list))) -> 每個 list 都在不同的記憶體位置，所以比較慢 (ex.0x1b449053f80,0x1b4490592c0,...)

    # for x in range(width):
    #     for y in range(height):
    #         pixel_list = []                 # Important! 如果沒有reset list 的話，list會變得超大，所以會跑超級慢
    #         for img in images:
    #             pixel_list.append(img.get_pixel(x, y))
    #         result.set_pixel(x, y, get_best_pixel(pixel_list))

    # ----- YOUR CODE ENDS HERE ----- #

    # Time test
    end = time()
    time_list.append(round(end-start, 5))
    print('Execution time: ', sum(time_list)/len(time_list))

    # Display img
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):                       # 如果 filename 的結尾是.jpg
            filenames.append(os.path.join(dir, filename))   # filenames = 路徑 + 圖檔名
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
