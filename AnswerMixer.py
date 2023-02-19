import copy
import pytesseract
import cv2
from random import shuffle
import editFiles
import os
import listFinds
import editPng

athOfPdf = ""
numOfAnswers = 4
pageCode = True
detailsBetweenQ = False
input_directory = "C:\\Users\\izeik\\Pictures\\אוטומטים לא מעורבל\\"
ouput_directory = 'C:\\Users\\izeik\\Pictures\\Mix\\'

if numOfAnswers == 5:
    answersId = ["שאלה", "א.", "ב.", "ג.", "ד.", "ה.", "A"]
else:
    answersId = ["שאלה", "א.", "ב.", "ג.", "ד.", "A"]


def mixfiles(path, numQ, numA):
    arrayAnswers = []
    for i in range(numQ):
        arrayAnswers.append([])
        for j in range(numA):
            arrayAnswers[i].append(path + "qustion_{}_answer_{}_image.png".format(i + 1, j + 1))
        shuffle(arrayAnswers[i])
    shuffleQuestions = []
    for i in range(numQ):
        shuffleQuestions.append(path + "qustion_{}_image.png".format(i + 1))
        for j in range(numA):
            shuffleQuestions.append(arrayAnswers[i][j])
    numQ = 1
    for i in range(0, len(shuffleQuestions), numOfAnswers + 1):
        if shuffleQuestions[i] == path + "qustion_{}_image.png".format(numQ):
            numQ += 1
            for j in range(1, numOfAnswers + 1):
                if i == 30:
                    pass
                editPng.rewriteAnswer(shuffleQuestions[i + j], j, rightFirstWordToBox(shuffleQuestions[i + j]))

    return shuffleQuestions


def rightFirstWordToBox(path):
    image = cv2.imread(path)
    boxes = pytesseract.image_to_data(image, lang='eng+heb', config='--oem 2 --psm 6',
                                      output_type=pytesseract.Output.DICT)
    # 'C:\\Users\\izeik\\Pictures\\Mix\\qustion_1_answer_3_image.png'
    try:
        return wordToBox(answersId[int(path.split('\\')[path.count('\\')].split('_')[3])], boxes)[2]
    except:
        return 1530


def wordToBox(text, first_word_boxes, num=1):
    value_first_word = copy.deepcopy(first_word_boxes)
    words = value_first_word['text']
    y = value_first_word['top']
    l = first_word_boxes['left']
    h = value_first_word['height']

    start_index = listFinds.find_index(words, text, num, answersId)
    x_start, y_start, x_end, y_end = 0, y[start_index], l[start_index], y[start_index] + h[start_index]
    return x_start, y_start, x_end, y_end


def export_elements(path, numQ, first_words):
    image = cv2.imread(path)
    numAppear = 1
    numLastQ = numQ + 1
    coordNext = []
    height = 0
    for numQ in range(1, numLastQ):
        for charAns in answersId[1:]:
            if numQ == 19:
                pass
            if charAns == answersId[1]:
                coordNext = wordToBox(answersId[0], first_words, numAppear)
            coordCurrent = coordNext
            # if it is the last answer in the qestion
            if charAns == answersId[-1]:
                if numQ != numLastQ - 1:
                    coordNext = wordToBox(answersId[0], first_words, numAppear + 1)
                else:
                    coordNext = [image.shape[1], image.shape[0], image.shape[1], image.shape[0]]
            else:
                coordNext = wordToBox(charAns, first_words, numAppear)
            cropped_image = image[coordCurrent[1] - 10:coordNext[1] - 10, 0:image.shape[1]]
            try:
                if charAns != "א.":
                    path = ouput_directory + 'qustion_{}_answer_{}_image.png'.format(numQ, answersId.index(charAns) - 1)
                    cv2.imwrite(path, cropped_image)
                else:
                    path = ouput_directory + 'qustion_{}_image.png'.format(numQ)
                    cv2.imwrite(path, cropped_image)
            except:
                cv2.imwrite(path, image[0:30, 0:image.shape[1]])
                print(fr"ERROR question - {numQ} answer -{answersId.index(charAns)}")
        numAppear += 1


def blendPdf():
    pages = editFiles.pdf_to_png(pathOfPdf, ouput_directory)
    pathOfImage = editFiles.combineFiles(pages, ouput_directory + 'result')
    editFiles.delete_files(pages)
    first_words_array = listFinds.first_words(pathOfImage, answersId)
    numQ = listFinds.countQuestion(first_words_array)
    export_elements(pathOfImage, numQ, first_words_array)
    editPng.reCrop(numQ, numOfAnswers, ouput_directory, detailsBetweenQ)
    mixAnswers = mixfiles(ouput_directory, numQ, numOfAnswers)
    pathOfImage = editFiles.combineFiles(mixAnswers, ouput_directory + 'result')
    editFiles.delete_files(mixAnswers)
    editFiles.png_to_pdf(pathOfImage, ouput_directory, pathOfPdf)
    editFiles.delete_files([ouput_directory + 'result.png'])


def main():
    '''
    First conver the PDF to PNG files and combine and delete them.
    The answers and questions are exported to PNG files.
    We mix the answers and export to PDF
    '''
    for filename in os.listdir(input_directory):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(input_directory, filename)
            global pathOfPdf
            pathOfPdf = pdf_file_path
            fileNameEnd = pathOfPdf[pathOfPdf.rfind("\\") + 1:-4] + " מעורבל" + pathOfPdf[-4:]
            destPath = ouput_directory + fileNameEnd
            # if os.path.isfile(destPath):
            #   print("EXIST {}".format(destPath))
            #  continue

            blendPdf()
            print("SUCCESS {}".format(fileNameEnd))


if __name__ == "__main__":
    main()
