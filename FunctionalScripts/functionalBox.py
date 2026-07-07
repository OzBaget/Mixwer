import copy

import pytesseract
import cv2

from Logicalscripts import logicalList

def rightFirstWordToBox(path, answersId):
    image = cv2.imread(path)
    boxes = pytesseract.image_to_data(image, lang='eng+heb', config='--oem 1 --psm 6',
                                      output_type=pytesseract.Output.DICT)
    try:
        return wordToBox(answersId[int(path[path.rfind("_") + 1:-4])], boxes, answersId, 1, True)[2]#TODO: go over and find the righest not white pixel
    except:
        return 1530


def wordToBox(text, first_word_boxes, answersId, num=1, answer=False):
    """

    :param text: the word
    :param first_word_boxes: The array
    :param answersId: The
    :param num: the num appearance of the word
    :param answer: the array of optoinal array
    :return: The coord of word[0(right),top,left,bottom]
    """
    value_first_word = copy.deepcopy(first_word_boxes)
    words = value_first_word['text']
    y = value_first_word['top']
    l = first_word_boxes['left']
    h = value_first_word['height']
    if not answer:
        start_index = logicalList.find_index(words, text, answersId, num)
    else:
        start_index = logicalList.find_index_answer(words)
    return 0, y[start_index], l[start_index], y[start_index] + h[start_index]
