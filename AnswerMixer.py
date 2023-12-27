import re


import editFiles

import exportPng
import listFinds
import editPng
import editBox
import numpy as np

successPdf = []
athOfPdf = ""
answersId = []
pageCode = True
detailsBetweenQ = False
# input_directory = "C:\\Users\\izeik\\Pictures\\אוטומטים לא מעורבל\\"
ouput_directory = editFiles.getOutputDirectoryPath()


def mixfiles():
    directory_path, file_list = editFiles.getFilesPaths()

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

    '''numQ = 1
    for i in range(0, len(shuffleQuestions), numOfAnswers + 1):
        if shuffleQuestions[i] == ouput_directory + "question_{}_prefix.png".format(numQ):
            numQ += 1
            for j in range(1, numOfAnswers + 1):
                editPng.rewriteAnswer(shuffleQuestions[i + j], j,
                                      editBox.rightFirstWordToBox(shuffleQuestions[i + j], answersId))
'''


def blendPdf():
    # Convert test .pdf to page.png
    path_originial_pages_png = editFiles.pdf_to_png(path_original_pdf, ouput_directory)

    # TODO dont merge the pages because the ocr is less good, see what to do that it will be splited pages
    # Merge the pages
    pathOfMerge = editFiles.combineFiles(path_originial_pages_png, ouput_directory + 'result')

    # Find how much q and a there are
    # make each q to .png
    arrayOfQuestions, numQ = exportPng.export_questions(path_originial_pages_png, ouput_directory)
    print("Success export Q\n")
    # make each a to .png
    for pathQ in arrayOfQuestions:
        global answersId
        answersId = listFinds.findNumAnswers(pathQ)
        exportPng.export_answers(pathQ, answersId, ouput_directory)
        print("Success export A in Q {}\n".format(pathQ))

    # crop each a
    editPng.reCrop()
    print("Success Croping\n")

    # Mix the order of the answer
    mixAnswers = mixfiles()
    print("Success Mixing\n")
    # Make answers and questions to pages .png
    paths_of_pages = editFiles.combineFilestoPages(mixAnswers, ouput_directory)
    print("Success final pages\n")

    # Add answers page
    answer_page_path, path_answers = editPng.createAnswersPage(mixAnswers)
    paths_of_pages = paths_of_pages + answer_page_path
    print("Success answer page\n")
    # Make .png to .pdf
    paths_of_pages_pdf = []
    for current_page in paths_of_pages:
        paths_of_pages_pdf.append(editFiles.png_to_pdf(current_page))
    print("Success convert pages to.pdf\n")

    ouput_pdf_path = ouput_directory + path_original_pdf[path_original_pdf.rfind("/") + 1:-4] + " מעורבל"
    editFiles.merge_pdf(paths_of_pages_pdf,
                        ouput_pdf_path)
    print("Success merge pages\n")

    editFiles.delete_files(path_originial_pages_png)
    editFiles.delete_files(paths_of_pages)
    editFiles.delete_files(path_answers)
    editFiles.delete_files(arrayOfQuestions)
    editFiles.delete_files(paths_of_pages_pdf)
    editFiles.delete_files([ouput_directory + 'result.png'])
    editFiles.delete_files(mixAnswers)

    return ouput_pdf_path


def main(array_paths):
    '''
    First conver the PDF to PNG files and combine and delete them.
    The answers and questions are exported to PNG files.
    We mix the answers and export to PDF
    '''
    global successPdf
    successPdf = []
    failPdf = []
    for pdf_file_path in array_paths:
        global path_original_pdf
        path_original_pdf = pdf_file_path
        fileNameEnd = path_original_pdf[path_original_pdf.rfind("\\") + 1:-4] + " מעורבל" + path_original_pdf[-4:]
        try:
            # zip all the successPdf
            successPdf.append(blendPdf() + ".pdf")

            print("SUCCESS {}".format(fileNameEnd))

            # TODO:  delete all the rest files that not pdf
        except Exception as e:
            print("NOT  SUCCESS {}".format(fileNameEnd) + " ERROR: ", e)
            failPdf.append(pdf_file_path)
            # TODO send to the UI how many tests rest
    return successPdf != []


def zipPdf(zip_path):
    editFiles.create_zip(successPdf, zip_path)


if __name__ == "__main__":
    main()
