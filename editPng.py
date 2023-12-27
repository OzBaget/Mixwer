import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import editFiles


def is_image_all_white(image_path):
    try:
        # Open the image
        image = Image.open(image_path)

        # Get the image dimensions
        width, height = image.size

        # Define the white color in RGB format
        white_color = (255, 255, 255)

        # Iterate through each pixel in the image
        for x in range(width):
            for y in range(height):
                pixel_color = image.getpixel((x, y))
                if pixel_color != white_color:
                    return False  # Found a non-white pixel

        # If all pixels are white, return True
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False  # Handle any exceptions by returning False


def reCrop():
    ouput_directory,list_files = editFiles.getFilesPaths()
    for pathC in enumerate(list_files):
        if "answer" in pathC[1] or "prefix" in pathC[1]:
            cropSpaceEndPng(editFiles.getOutputDirectoryPath()+pathC[1])#TODO pathC[1]

def lastWhiteLineCoordPng(path):
    img = cv2.imread(path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Set the threshold for what is considered white
    white_threshold = 255
    # Get the shape of the image
    height, width = gray.shape
    # Calculate the average intensity for each row
    avg_intensity = [sum(row) / width for row in gray]

    # Find the first row where the average intensity is less than the threshold
    for i, intensity in enumerate(avg_intensity[::-1]):
        if intensity < white_threshold:
            return height - i
    return 0


def firstNotWhiteLineCoordPng(path, bigSpace, contiueSearchBigSpace):
    image = cv2.imread(path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Get the shape of the image
    height, width = gray.shape
    # Set the threshold for what is considered white
    white_threshold = 255
    # Calculate the average intensity for each row
    end = min(1000, height)
    avg_intensity = [sum(row) / width for row in gray[20:end]]

    # Find the first row where the average intensity is less than the threshold
    i = 1
    while i < len(avg_intensity):
        isThisEnoughBigSpace = True
        if avg_intensity[i] == white_threshold:
            j = i
            while j < len(avg_intensity) and isThisEnoughBigSpace:
                if j < i + bigSpace and avg_intensity[j] != white_threshold:
                    isThisEnoughBigSpace = False
                    i = j
                    if not contiueSearchBigSpace:
                        break
                if not contiueSearchBigSpace:
                    if j > i + bigSpace and isThisEnoughBigSpace and avg_intensity[j] != white_threshold:
                        return j + 20
                else:
                    if j > i + bigSpace and isThisEnoughBigSpace and avg_intensity[j] == white_threshold:
                        return i
                j += 1
            if not isThisEnoughBigSpace and not contiueSearchBigSpace:
                break

        i += 1
    return False


def cropSpaceEndPng(path):
    image = cv2.imread(path)
    height = lastWhiteLineCoordPng(path)
    cropped = image[:height + 10, :]
    cv2.imwrite(path, cropped)


def cropSpaceAnswerPng(path, mid=False):
    image = cv2.imread(path)
    height = firstNotWhiteLineCoordPng(path, 20, mid)
    if not height:
        return
    if not mid:
        cropped = np.vstack((image[0:30, :], image[height:, :]))
    if mid:
        cropped = image[:height + 20, :]
    cv2.imwrite(path, cropped)


# Add the number of Answer to Png
def rewriteAnswer(path, i, location):
    text = ".{}".format(i)
    text_height, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    imageQ = cv2.imread(path)
    cv2.rectangle(imageQ, (location, 0),
                  (imageQ.shape[1], imageQ.shape[0]), (255, 255, 255), -1)
    cv2.imwrite(path, imageQ)
    cv2.putText(imageQ, text, (1530, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imwrite(path, imageQ)


def createAnswersPage(path_answers):
    PAGE_HEIGHT = 1805
    PAGE_WIDTH = 1700
    image_array = []
    num_answer = 1
    prefix_path = path_answers[1][:path_answers[1].rfind("\\") + 1]
    current_path = ""

    num_q = 0
    for cpath in path_answers:
        pathEnd = cpath[cpath.rfind("_") + 1:-4]
        if pathEnd == 'prefix':
            num_answer = 1
        elif pathEnd == '1':
            num_q = cpath[cpath.find("_") + 1:cpath.rfind("_") - 7]
            blank = Image.new("RGBA", (PAGE_WIDTH, 70), (255, 255, 255, 255))
            text = "Question {} : Answer {}".format(num_q
                                   , num_answer)
            font = ImageFont.truetype('arial.ttf', 40)
            draw = ImageDraw.Draw(blank)
            text_width, text_height = draw.textsize(text, font=font)

            text_x = (PAGE_WIDTH - text_width) / 2
            text_y = (70 - text_height) / 2

            # Draw text on the image
            draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
            current_path = prefix_path + fr"answer_{num_q}.png"
            blank.save(current_path)
            image_array.append(current_path)
        try:
            int(pathEnd)
            num_answer += 1
        except:
            pass

    return editFiles.combineFilestoPages(image_array, prefix_path, "AnswerPage"), image_array

#if the Q is more than a page we need to split it
def crop_png_middle(path_to_png, start_coord,search_height=70,noWhite=False):
    img = Image.open(path_to_png)
    width, height = img.size

    if noWhite:
        split_y = start_coord
    else:
        # Define the starting point and height for the search
        start_y = start_coord


        # Iterate through the image and find the white lines
        white_lines = []
        try:
            for y in range(start_y, height):
                line = img.crop((0, y, width, y + 1))
                avg_color = tuple(map(int, line.resize((1, 1)).getpixel((0, 0))))
                if avg_color == (255, 255, 255):
                    white_lines.append(y)
                else:
                    white_lines.clear()
                if len(white_lines) == search_height:
                    break
        except:
            return False

        # If no white lines were found, return the original image
        if not len(white_lines) == search_height:
            return False

        if not white_lines[0] + 10 < height:
            return False

        # Otherwise, split the image at the first white line found
        split_y = white_lines[0]

    top_img = img.crop((0, 0, width, split_y+10))
    bottom_img = img.crop((0, split_y+10, width, height))

    # Save the cropped images to disk
    top_img.save(path_to_png[:path_to_png.rfind(".")]+"_top.png" )
    bottom_img.save(path_to_png[:path_to_png.rfind(".")]+"_bottom.png")
    return [path_to_png[:path_to_png.rfind(".")]+"_top.png",path_to_png[:path_to_png.rfind(".")]+"_bottom.png"]


def rightmost_non_white_black_pixel(path):
    # Open the image
    image = Image.open(path)

    # Get image width and height
    width, height = image.size
    flagA,flagB,flagC =False,False,False
    # Start from the rightmost column and move towards the left
    for x in range(width - 1, -1, -1):
        col_sum = [0, 0, 0]
        for y in range(height):
            pixel_value = image.getpixel((x, y))
            col_sum[0] += pixel_value[0]  # Red channel
            col_sum[1] += pixel_value[1]  # Green channel
            col_sum[2] += pixel_value[2]  # Blue channel

        # Calculate the average for each color channel
        avg_r = col_sum[0] / height
        avg_g = col_sum[1] / height
        avg_b = col_sum[2] / height

        # Check if the average of the column is not purely white (255, 255, 255)
        if avg_r < 255 or avg_g < 255 or avg_b < 255:
            flagA = True
        if flagA and avg_r == 255 and avg_g == 255 and avg_b == 255:
            flagB = True
        if flagA and flagB and (avg_r < 255 or avg_g < 255 or avg_b < 255):
            flagC = True
        if flagA and flagB and flagC and avg_r == 255 and avg_g == 255 and avg_b == 255:
            return x

            # Find the rightmost non-white black pixel in the column
