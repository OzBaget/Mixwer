import re

import numpy as np
import pytesseract
import cv2

from FunctionalScripts import functionalFiles, editPng

ouput_directory = "Local storage of images\\"


def find_index_correct_ocr(words, target_word):
    if target_word in words:
        return words.index(target_word)
    return -1


def find_index(words, target_word, answersId, num=1, skipBefore=False):
    if target_word == answersId[0]:  # for "שאלה"
        if words.count("שאלה" == 0):
            return -1
        arr = np.array(words)

        x = np.where(arr == target_word)
        return x[0][num - 1]
        # return False
    else:
        '''if words.count(target_word) > 1:
            arr = np.array(words)

            x = np.where(arr == target_word)
            return x[0][-1]
        '''
        if not target_word in words:
            for i, word in enumerate(words):
                if target_word[0] == word:
                    return i
            if answersId.index(target_word) == 1 or skipBefore:
                index_before = -1
            else:
                index_before = find_index(words, answersId[answersId.index(target_word) - 1], answersId)
            try:
                if target_word != answersId[-2]:
                    index_after = find_index(words, answersId[answersId.index(target_word) + 1], answersId,
                                             skipBefore=True)
                    i = index_after
                    while i > 0:
                        if word != '' and target_word[0] in words[i][0]:
                            return i
                        i -= 1
                    if index_after - index_before == 2:
                        return index_before + 1
                else:
                    i = index_before
                    while i < len(words):
                        if word != '' and target_word[0] in words[i][0]:
                            return i
                        i += 1
            except:
                pass
            for i, word in enumerate(words):
                if index_before < i and word in ["-", ".", "--", "\\\\",
                                                 "(\\"]:  # TODO ... and all(word[i] in ["-",...] for i in len(word))
                    return i
            raise Exception("Not find {} in this image".format(target_word))
        return words.index(target_word)


def find_index_answer(words):
    for i, word in enumerate(words):
        if word == "":
            pass
        else:
            return i


def last_occurrence(word, array):
    array_reversed = array[::-1]
    try:
        last_index = len(array) - 1 - array_reversed.index(word)
        return last_index
    except ValueError:
        return -1


def find_first_words(path, answersId=[], fromQ=True, fixOCRAnswers=False):
    image = cv2.imread(path)
    boxes = pytesseract.image_to_data(image, lang='heb', config='--oem 1 --psm 6',
                                      output_type=pytesseract.Output.DICT)
    # Filter only the first word in line
    first_words_boxes = {'text': [], 'left': [], 'top': [], 'width': [], 'height': []}
    line_number = -1
    first_space = False
    for i in range(len(boxes["text"])):
        if boxes["text"][i] == "" and boxes["line_num"][i] != line_number:
            first_space = True
        elif boxes["text"][i] != "" and (first_space or boxes["line_num"][i] != line_number):
            line_number = boxes["line_num"][i]
            if boxes['text'][i] == "שאלה" and boxes['text'][i + 1] == "מספר":
                boxes['text'][i] = "שאלה מספר"
            first_words_boxes['text'].append(boxes['text'][i])  # Extract the bounding boxes for each word
            first_words_boxes['left'].append(boxes['left'][i])  # Extract the bounding boxes for each word
            first_words_boxes['top'].append(boxes['top'][i])  # Extract the bounding boxes for each word
            first_words_boxes['width'].append(boxes['width'][i])  # Extract the bounding boxes for each word
            first_words_boxes['height'].append(boxes['height'][i])  # Extract the bounding boxes for each word
            if first_space:
                first_space = False

    if fromQ:  # intilize the mistakes of ocr
        start_first_words_from_Q(first_words_boxes, answersId)
        for i in range(len(first_words_boxes['text'])):
            for j in range(len(answersId) - 1):
                if answersId[j] in first_words_boxes['text'][i]:
                    first_words_boxes['text'][i] = answersId[j]
                    break
    if fixOCRAnswers:
        try:
            begin = find_index(first_words_boxes['text'], "א.", ["A", "ד.", "ג.", "ב.", "א."])
        except:
            begin = 0
        for i in range(begin,len(first_words_boxes['text'])):
            if first_words_boxes['text'][i][:2] in ["ה.", "ד.", "ג.", "ב.", "א."] \
                    and first_words_boxes['text'][i] not in ["ה.", "ד.", "ג.", "ב.", "א."]:
                first_words_boxes['text'][i] = first_words_boxes['text'][i][:2]
            elif first_words_boxes['text'][i] in ["ה", "ד", "ג", "ב", "א"]:
                first_words_boxes['text'][i] += "."

    return first_words_boxes


'''    if disable_consecutive_q:    # If "שאלה" after "שאלה" delete it
        arr = np.array(first_words_boxes['text'])

        x = np.where(arr == answersId[0])

        for i in range(len(x[0]) - 1):
            if x[0][i] + 1 == x[0][i + 1]:
                first_words_boxes['text'][x[0][i + 1]] = '''''


def start_first_words_from_Q(first_word_boxes, answersId):
    index_first_q = find_index(first_word_boxes['text'], answersId[0], answersId)
    first_word_boxes['text'] = first_word_boxes['text'][index_first_q:]  # Extract the bounding boxes for each word
    first_word_boxes['left'] = first_word_boxes['left'][index_first_q:]  # Extract the bounding boxes for each word
    first_word_boxes['top'] = first_word_boxes['top'][index_first_q:]  # Extract the bounding boxes for each word
    first_word_boxes['width'] = first_word_boxes['width'][index_first_q:]  # Extract the bounding boxes for each word
    first_word_boxes['height'] = first_word_boxes['height'][index_first_q:]
    return first_word_boxes


def isCorrectOCR(words):
    if all(word in words for word in ["א.", "ב.", "ג.", "ד."]) and all("\\" not in word for word in words):
        return True
    return False  # TODO check problems


def findNumAnswers(pathOfMerge):
    first_words = find_first_words(pathOfMerge, [], False, True)
    if isCorrectOCR(first_words['text']):
        indexH = find_index_correct_ocr(first_words['text'], "ה.")
        indexD = find_index_correct_ocr(first_words['text'], "ד.")
        if indexH != -1:
            return ["שאלה מספר", "א.", "ב.", "ג.", "ד.", "ה.", "A"]
        elif indexD != -1:
            return ["שאלה מספר", "א.", "ב.", "ג.", "ד.", "A"]
        else:
            return ["שאלה מספר", "א.", "ב.", "A"]

    try:
        indexH = find_index(first_words['text'], "ה.",
                            ["שאלה מספר", "א.", "ב.", "ג.", "ד.", "ה.", "A"])
        indexD = find_index(first_words['text'], "ד.",
                            ["שאלה מספר", "א.", "ב.", "ג.", "ד.", "ה.", "A"])
        indexB = find_index(first_words['text'], "ב.",
                            ["שאלה מספר", "א.", "ב.", "A"])
        if indexH != -1 and indexD < indexH:
            return ["שאלה מספר", "א.", "ב.", "ג.", "ד.", "ה.", "A"]
        if indexB != -1 and indexD == -1 and indexH == -1:
            return ["שאלה מספר", "א.", "ב.", "A"]
    except:
        try:
            indexD = find_index(first_words['text'], "ד.",
                                ["שאלה מספר", "א.", "ב.", "ג.", "ד.", "ה.", "A"])
            indexB = find_index(first_words['text'], "ב.",
                                ["שאלה מספר", "א.", "ב.", "A"])
            if indexB != -1 and indexD == -1:
                return ["שאלה מספר", "א.", "ב.", "A"]
            return ["שאלה מספר", "א.", "ב.", "ג.", "ד.", "A"]
        except:
            return ["שאלה מספר", "א.", "ב.", "A"]


def mixfiles():
    directory_path, file_list = functionalFiles.getFilesPaths()

    # Get a list of all files in the directory

    # Create a list of file paths by joining the directory path with each file name

    arrayAnswers = []
    q = 1
    while "question_{}.png".format(q) in file_list:
        arrayAnswers.append([])
        a = 1
        while "question_{}_answer_{}.png".format(q, a) in file_list:
            arrayAnswers[q - 1].append(directory_path + "question_{}_answer_{}.png".format(q, a))
            a += 1
        np.random.shuffle(arrayAnswers[q - 1])
        q += 1

    shuffleQuestions = []
    q = 0
    while "question_{}.png".format(q + 1) in file_list:
        if "question_{}_prefix.png".format(q + 1) not in file_list:
            q+=1
            continue
        shuffleQuestions.append(directory_path + "question_{}_prefix.png".format(q + 1))
        a = 0
        while "question_{}_answer_{}.png".format(q + 1, a + 1) in file_list:
            shuffleQuestions.append(arrayAnswers[q][a])
            a += 1
        q += 1

    pattern = ouput_directory.replace("\\", "\\\\") + r"question_\d+_prefix.png"
    i = 0
    while i < len(shuffleQuestions):
        isPerfix = re.fullmatch(pattern, shuffleQuestions[i])
        if bool(isPerfix):
            counterA = 1
            i += 1
            isPerfix = False
            while i < len(shuffleQuestions) and not re.fullmatch(pattern, shuffleQuestions[i]):
                if i == 40:
                    pass
                editPng.rewriteAnswer(shuffleQuestions[i], counterA,
                                      editPng.rightmost_non_white_black_pixel(shuffleQuestions[i]))
                counterA += 1
                i += 1
    i += 1
    return shuffleQuestions
