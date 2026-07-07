
from Logicalscripts import *
from FunctionalScripts import *
import os

successPdf = []
answersId = []

output_directory = "Local storage of images\\"
output_final_directory = "Final PDFs\\"



def blendPdf():
    # Convert test .pdf to page.png
    path_originial_pages_png = functionalFiles.pdf_to_png(path_original_pdf, output_directory)

    # TODO dont merge the pages because the ocr is less good, see what to do that it will be splited pages
    # Merge the pages
    pathOfMerge = functionalFiles.combineFiles(path_originial_pages_png, output_directory + 'result')

    # Find how much q and a there are
    # make each q to .png
    arrayOfQuestions, numQ = exportPng.export_questions(path_originial_pages_png, output_directory)
    print("Success export Q\n")
    # make each a to .png
    for pathQ in arrayOfQuestions:
        global answersId
        answersId = logicalList.findNumAnswers(pathQ)
        exportPng.export_answers(pathQ, answersId, output_directory)
        print("Success export A in Q {}\n".format(pathQ))

    # crop each a
    logicalPng.cropAnswers()
    print("Success Croping\n")

    # Mix the order of the answer
    mixAnswers = logicalList.mixfiles()
    print("Success Mixing\n")
    # Make answers and questions to pages .png
    paths_of_pages = logicalPng.combineFilestoPages(mixAnswers, output_directory)
    print("Success final pages\n")

    # Add answers page
    answer_page_path, path_answers = logicalPng.createAnswersPage(mixAnswers)
    paths_of_pages = paths_of_pages + answer_page_path
    print("Success answer page\n")
    # Make .png to .pdf
    paths_of_pages_pdf = []
    for current_page in paths_of_pages:
        paths_of_pages_pdf.append(functionalFiles.png_to_pdf(current_page))
    print("Success convert pages to.pdf\n")

    ouput_pdf_path = output_final_directory + path_original_pdf[path_original_pdf.rfind("/") + 1:-4] + " מעורבל"
    functionalFiles.merge_pdf(paths_of_pages_pdf,
                        ouput_pdf_path)
    print("Success merge pages\n")

    functionalFiles.delete_files(tuple(functionalFiles.getFilesPaths()[0]+B for B in functionalFiles.getFilesPaths()[1]))

    return ouput_pdf_path


def main(array_paths):
    '''
    First conver the PDF to PNG files and combine and delete them.
    The answers and questions are exported to PNG files.
    We mix the answers and export to PDF
    '''
    # Ensure output directories exist
    os.makedirs(output_directory, exist_ok = True)
    os.makedirs(output_final_directory, exist_ok = True)
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
        except Exception as e:
            print("NOT  SUCCESS {}".format(fileNameEnd) + " ERROR: ", e)
            failPdf.append(pdf_file_path)
    return successPdf,successPdf != []


if __name__ == "__main__":
    main()


def get_ouput_directory():
    return output_directory