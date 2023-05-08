import cv2
from random import shuffle
import editFiles
import os

import exportPng
import listFinds
import editPng
import editBox
import numpy as np

athOfPdf = ""
numOfAnswers = 5
answersId = []
pageCode = True
detailsBetweenQ = False
input_directory = "C:\\Users\\izeik\\Pictures\\אוטומטים לא מעורבל\\"
ouput_directory = 'C:\\Users\\izeik\\Pictures\\Mix\\'


def mixfiles(path, numQ, numA):
    arrayAnswers = []
    for i in range(numQ):
        arrayAnswers.append([])
        for j in range(numA):
            arrayAnswers[i].append(path + "question_{}_answer_{}.png".format(i + 1, j + 1))
        shuffle(arrayAnswers[i])
    shuffleQuestions = []
    for i in range(numQ):
        shuffleQuestions.append(path + "question_{}_prefix.png".format(i + 1))
        for j in range(numA):
            shuffleQuestions.append(arrayAnswers[i][j])
    numQ = 1
    for i in range(0, len(shuffleQuestions), numOfAnswers + 1):
        if shuffleQuestions[i] == path + "question_{}_prefix.png".format(numQ):
            numQ += 1
            for j in range(1, numOfAnswers + 1):
                if i == 30:
                    pass
                editPng.rewriteAnswer(shuffleQuestions[i + j], j,
                                      editBox.rightFirstWordToBox(shuffleQuestions[i + j], answersId))

    return shuffleQuestions



def blendPdf():
    # Conver test .pdf to page.png
    path_originial_pages_png = editFiles.pdf_to_png(path_original_pdf, ouput_directory)

    #TODO dont merge the pages because the ocr is less good, see what to do that it will be splited pages
    # Merge the pages
    pathOfMerge = editFiles.combineFiles(path_originial_pages_png, ouput_directory + 'result')

    # Find how much q and a there are
    global numOfAnswers, answersId
    numOfAnswers, answersId = listFinds.findNumAnswers(pathOfMerge)

    first_words_array = listFinds.find_first_words(pathOfMerge, answersId)
    # make each q to .png
    arrayOfQuestions,numQ = exportPng.export_questions(path_originial_pages_png,answersId,ouput_directory)
    # make each a to .png
    for pathQ in arrayOfQuestions:
        exportPng.export_answers(pathQ,answersId,ouput_directory)
    # crop each a
    editPng.reCrop(numQ, numOfAnswers, ouput_directory, detailsBetweenQ)

    # Mix the order of the answer
    mixAnswers = mixfiles(ouput_directory, numQ, numOfAnswers)

    # Make answers and questions to pages .png
    paths_of_pages = editFiles.combineFilestoPages(mixAnswers, ouput_directory, numOfAnswers)

    # Add answers page
    answer_page_path, path_answers = editPng.createAnswersPage(mixAnswers)
    path_answers = path_answers + answer_page_path
    paths_of_pages = paths_of_pages + answer_page_path
    # Make .png to .pdf
    paths_of_pages_pdf = []
    for current_page in paths_of_pages:
        paths_of_pages_pdf.append(editFiles.png_to_pdf(current_page))

    editFiles.merge_pdf(paths_of_pages_pdf,
                        ouput_directory + path_original_pdf[path_original_pdf.rfind("\\") + 1:-4] + " מעורבל")

    editFiles.delete_files(path_originial_pages_png)
    editFiles.delete_files(paths_of_pages)
    editFiles.delete_files(arrayOfQuestions)
    editFiles.delete_files([ouput_directory + 'result.png'])
    editFiles.delete_files(mixAnswers)


def main():
    '''
    First conver the PDF to PNG files and combine and delete them.
    The answers and questions are exported to PNG files.
    We mix the answers and export to PDF
    '''
    for filename in os.listdir(input_directory):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(input_directory, filename)
            global path_original_pdf
            path_original_pdf = pdf_file_path
            fileNameEnd = path_original_pdf[path_original_pdf.rfind("\\") + 1:-4] + " מעורבל" + path_original_pdf[-4:]
            destPath = ouput_directory + fileNameEnd
            if os.path.isfile(destPath):
                print("EXIST {}".format(destPath))
                continue
            blendPdf()
            print("SUCCESS {}".format(fileNameEnd))


if __name__ == "__main__":
    main()
