import copy

import pytesseract
import cv2
import listFinds

def rightFirstWordToBox(path,answersId):
    image = cv2.imread(path)
    boxes = pytesseract.image_to_data(image, lang='eng+heb', config='--oem 2 --psm 6',
                                      output_type=pytesseract.Output.DICT)
    try:
        return wordToBox(answersId[int(path[path.rfind("_")+1:-4])],boxes,answersId,1,True)[2]
    except:
        return 1530


def wordToBox(text, first_word_boxes, answersId,num = 1,answer = False):
    value_first_word = copy.deepcopy(first_word_boxes)
    words = value_first_word['text']
    y = value_first_word['top']
    l = first_word_boxes['left']
    h = value_first_word['height']
    if not answer:
        start_index = listFinds.find_index(words, text, answersId,num)
    else:
        start_index = listFinds.find_index_answer(words)
    x_start, y_start, x_end, y_end = 0, y[start_index], l[start_index], y[start_index] + h[start_index]
    return x_start, y_start, x_end, y_end
