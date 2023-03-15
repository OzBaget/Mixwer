import copy

import pytesseract
import cv2
import listFinds

def rightFirstWordToBox(path,answersId):
    image = cv2.imread(path)
    boxes = pytesseract.image_to_data(image, lang='eng+heb', config='--oem 2 --psm 6',
                                      output_type=pytesseract.Output.DICT)
    # 'C:\\Users\\izeik\\Pictures\\Mix\\qustion_1_answer_3_image.png'
    try:
        return wordToBox(answersId[int(path.split('\\')[path.count('\\')].split('_')[3])], boxes)[2]
    except:
        return 1530


def wordToBox(text, first_word_boxes, answersId,num=1,):
    value_first_word = copy.deepcopy(first_word_boxes)
    words = value_first_word['text']
    y = value_first_word['top']
    l = first_word_boxes['left']
    h = value_first_word['height']
    start_index = listFinds.find_index(words, text, num, answersId)
    x_start, y_start, x_end, y_end = 0, y[start_index], l[start_index], y[start_index] + h[start_index]
    return x_start, y_start, x_end, y_end
