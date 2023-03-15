import cv2
from random import shuffle
import editFiles
import os
import listFinds
import editPng
import editBox

athOfPdf = ""
numOfAnswers = 5
answersId=[]
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


def export_questions(path, numQ, first_words):
    image = cv2.imread(path)
    numLastQ = numQ
    coordNext = []
    questions_paths = []
    currentQ = 1
    while currentQ < numLastQ + 1:
        if currentQ == 1:
            coordNext = editBox.wordToBox(answersId[0], first_words, answersId, currentQ)
        coordCurrent = coordNext
        # if it is the last answer in the question
        if currentQ != numLastQ:
            coordNext = editBox.wordToBox(answersId[0], first_words,answersId, currentQ + 1)
            cropped_image = image[coordCurrent[1] - 10:coordNext[1] - 10, 0:image.shape[1]]
        else:
            cropped_image = image[coordCurrent[1] - 10:image.shape[0], 0:image.shape[1]]
        try:
            path = ouput_directory + 'question_{}.png'.format(currentQ)
            cv2.imwrite(path, cropped_image)
            questions_paths.append(path)
        except:
            cv2.imwrite(path, image[0:30, 0:image.shape[1]])
            print(fr"ERROR question - {currentQ}")
        currentQ += 1
    return questions_paths


def export_answers(path):
    image = cv2.imread(path)
    first_words = listFinds.find_first_words(path, answersId)
    halfPath = path[path.rfind("\\") + 1:]
    numQ = int(halfPath[9:-4])
    coordNext = []
    for charAns in answersId[1:]:
        if charAns == answersId[1]:
            coordNext = [0, 10, 0, 0]
        coordCurrent = coordNext
        # if it is the last answer in the qestion
        if charAns != answersId[-1]:
            coordNext = editBox.wordToBox(charAns, first_words,answersId, 1)
        else:
            coordNext = [image.shape[1], image.shape[0], image.shape[1], image.shape[0]]
        cropped_image = image[coordCurrent[1] - 10:coordNext[1] - 10, 0:image.shape[1]]
        try:
            if charAns != "א.":
                path = ouput_directory + 'question_{}_answer_{}.png'.format(numQ, answersId.index(charAns) - 1)
                cv2.imwrite(path, cropped_image)
            else:
                path = ouput_directory + 'question_{}_prefix.png'.format(numQ)
                cv2.imwrite(path, cropped_image)
        except:
            cv2.imwrite(path, image[0:30, 0:image.shape[1]])
            print(fr"ERROR question - {numQ} answer - {answersId.index(charAns)}")




def blendPdf():
    pages = editFiles.pdf_to_png(pathOfPdf, ouput_directory)
    pathOfMerge = editFiles.combineFiles(pages, ouput_directory + 'result')
    editFiles.delete_files(pages)
    global numOfAnswers,answersId
    numOfAnswers,answersId = listFinds.findNumAnswers(pathOfMerge)
    first_words_array = listFinds.find_first_words(pathOfMerge, answersId)
    numQ = listFinds.countQuestion(first_words_array)
    arrayOfQuestions = export_questions(pathOfMerge, numQ, first_words_array)
    for pathQ in arrayOfQuestions:
        export_answers(pathQ)
    editFiles.delete_files(arrayOfQuestions)
    editPng.reCrop(numQ, numOfAnswers, ouput_directory, detailsBetweenQ)
    mixAnswers = mixfiles(ouput_directory, numQ, numOfAnswers)
    pathOfMerge = editFiles.combineFilestoPages(mixAnswers, ouput_directory,numOfAnswers)
    editFiles.delete_files(mixAnswers)
    editFiles.png_to_pdf(pathOfMerge, ouput_directory, pathOfPdf)
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
