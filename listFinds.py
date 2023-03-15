import pytesseract
import cv2

def find_word_n_times(words, target_word, num,answersId):
    if target_word == answersId[0] and num == 1:
        if target_word in words:
            return words.index(target_word)
        # return False
    if answersId[0] not in words[1:]:  # for the last Que
        if not target_word in words:
            for i, word in enumerate(words):
                if target_word[0] == word:
                    return i
            for i, word in enumerate(words):
                if word != '' and target_word[0] in word[0]:
                    return i
            beforeOne = find_word_n_times(words, answersId[answersId.index(target_word) - 1], num,answersId)
            if beforeOne:
                return beforeOne + 1
            return beforeOne
        return words.index(target_word)
    if num == 1 and target_word != answersId[0]:  # the last iterative
        index = words.index(target_word)
        afterQ = find_word_n_times(words, answersId[0], num + 1,answersId)
        if index < afterQ:
            return index
        for i, word in enumerate(words):
            if i < afterQ and target_word[0] == word:
                return i
        for i, word in enumerate(words):
            if i < afterQ and target_word[0] in word[0]:
                return i
        if target_word != answersId[-1]:
            return find_word_n_times(words, answersId[answersId.index(target_word) + 1], num,answersId) - 1
        else:
            return find_word_n_times(words, answersId[answersId.index(target_word) - 1], num,answersId) + 1
    index_this_Q = find_word_n_times(words[1:], answersId[0], 1,answersId)
    return 1 + index_this_Q + find_word_n_times(words[index_this_Q + 1:], target_word, num - 1,answersId)


def last_occurrence(word, array):
    array_reversed = array[::-1]
    try:
        last_index = len(array) - 1 - array_reversed.index(word)
        return last_index
    except ValueError:
        return -1


def countQuestion(first_words):
    return first_words['text'].count("שאלה")


def find_index(words, target_word, num,answersId):
    if target_word == answersId[-1]:
        return find_word_n_times(words, answersId[0], num + 1,answersId)
    return find_word_n_times(words, target_word, num,answersId)


def find_first_words(path, answersId, fromQ=True):
    image = cv2.imread(path)
    boxes = pytesseract.image_to_data(image, lang='heb', config='--oem 2 --psm 6',
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
            first_words_boxes['text'].append(boxes['text'][i])  # Extract the bounding boxes for each word
            first_words_boxes['left'].append(boxes['left'][i])  # Extract the bounding boxes for each word
            first_words_boxes['top'].append(boxes['top'][i])  # Extract the bounding boxes for each word
            first_words_boxes['width'].append(boxes['width'][i])  # Extract the bounding boxes for each word
            first_words_boxes['height'].append(boxes['height'][i])  # Extract the bounding boxes for each word
            if first_space:
                first_space = False

    if fromQ:#intilize the mistakes of ocr
        first_words_from_Q(first_words_boxes,answersId)
        for i in range(len(first_words_boxes['text'])):
            for j in range(len(answersId) - 1):
                if answersId[j] in first_words_boxes['text'][i]:
                    first_words_boxes['text'][i] = answersId[j]
                    break

    return first_words_boxes


def first_words_from_Q(first_word_boxes,answersId):
    index_first_q = find_index(first_word_boxes['text'], answersId[0], 1,answersId)
    first_word_boxes['text'] = first_word_boxes['text'][index_first_q:]  # Extract the bounding boxes for each word
    first_word_boxes['left'] = first_word_boxes['left'][index_first_q:]  # Extract the bounding boxes for each word
    first_word_boxes['top'] = first_word_boxes['top'][index_first_q:]  # Extract the bounding boxes for each word
    first_word_boxes['width'] = first_word_boxes['width'][index_first_q:]  # Extract the bounding boxes for each word
    first_word_boxes['height'] = first_word_boxes['height'][index_first_q:]
    return first_word_boxes

def findNumAnswers(pathOfMerge):
    first_words = find_first_words(pathOfMerge, [], False)
    try:
            if find_index(first_words['text'][first_words['text'].index("שאלה"):],"ה.",1,["שאלה", "א.", "ב.", "ג.", "ד.", "ה.", "A"]) != -1:
                return 5,["שאלה", "א.", "ב.", "ג.", "ד.", "ה.", "A"]
    except:
        return 4,["שאלה", "א.", "ב.", "ג.", "ד.", "A"]