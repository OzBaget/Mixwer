import cv2

Qsign = "שאלה מספר"

from Logicalscripts import logicalList
from FunctionalScripts import functionalBox
from FunctionalScripts import functionalFiles


def export_questions(array_path, ouput_directory):
    HEIGHT_BEGIN_Q = 140
    questions_paths = []
    general_num_Q = 1
    first_Q = False
    for img in array_path:
        lastQ = False
        page_num_Q = 1
        open_img = cv2.imread(img)
        first_words = logicalList.find_first_words(img, [Qsign], False)
        if first_words['text'].count(Qsign) == 0:  # If Qsign still doesn't appear, continue to the next page
            if not first_Q:
                continue
            else:
                lastQ = True
        while not lastQ:
            first_Q = True
            coordCurrent = functionalBox.wordToBox(Qsign, first_words, [Qsign], page_num_Q)
            if page_num_Q < first_words['text'].count(Qsign):
                coordNext = functionalBox.wordToBox(Qsign, first_words, [Qsign], page_num_Q + 1)
                cropped_image = open_img[coordCurrent[1]:coordNext[1] - 10, 0:open_img.shape[1]]
            else:
                lastQ = True  # last q in the page
                if coordCurrent[1] > 10:
                    cropped_image = open_img[coordCurrent[1] - 10:open_img.shape[0], 0:open_img.shape[1]]
                else:
                    cropped_image = open_img[coordCurrent[1]:open_img.shape[0], 0:open_img.shape[1]]
            path = ouput_directory + 'question_{}.png'.format(general_num_Q)
            cv2.imwrite(path, cropped_image)
            questions_paths.append(path)
            general_num_Q += 1
            page_num_Q += 1

        ''' Check if some answers of the previous page there are in the begining of the page.
            if: There are something above the first q (probably a continue of the previous q)
                and this is not the last q 
        '''
        if first_words['text'].count(Qsign) != 0 \
                and functionalBox.wordToBox(Qsign, first_words, [Qsign], 1)[1] > HEIGHT_BEGIN_Q \
                and general_num_Q > page_num_Q \
                or first_words['text'].count(Qsign) == 0:
            if first_words['text'].count(Qsign) != 0:
                coordCurrent = functionalBox.wordToBox(Qsign, first_words, [Qsign], 1)
            else:
                coordCurrent = [0, open_img.shape[0], 0, 0]
            cropped_image = open_img[0:coordCurrent[1], 0:open_img.shape[1]]
            path = ouput_directory + 'continue_question_{}.png'.format(general_num_Q - page_num_Q)
            cv2.imwrite(path, cropped_image)

            merge_png = [ouput_directory + 'question_{}.png'.format(general_num_Q - page_num_Q)
                , path]
            functionalFiles.combineFiles(merge_png
                                         , ouput_directory + 'question_{}'.format(general_num_Q - page_num_Q))

    return questions_paths, general_num_Q - 1


def export_answers(pathRoot, answersId, ouput_directory):
    image = cv2.imread(pathRoot)
    first_words = logicalList.find_first_words(pathRoot, answersId, False,True)
    halfPath = pathRoot[pathRoot.rfind("\\") + 1:]
    numQ = int(halfPath[9:-4])
    if numQ == 10:
        pass
    coordNext = []
    try:
        for charAns in answersId[1:]:
            if charAns == answersId[1]:
                coordNext = [0, 10, 0, 0]
            coordCurrent = coordNext
            # If it is the last answer in the qestion
            if charAns != answersId[-1]:
                try:
                    coordNext = functionalBox.wordToBox(charAns, first_words, answersId)
                except:
                    # Crop the image from the begin of the last A, in order to make OCR read better
                    cropped_image = image[coordCurrent[1] - 10:image.shape[0], 0:image.shape[1]]

                    cv2.imwrite(pathRoot, cropped_image)
                    image = cv2.imread(pathRoot)
                    first_words = logicalList.find_first_words(pathRoot, answersId, False)

                    coordNext = functionalBox.wordToBox(charAns, first_words, answersId)
            else:
                coordNext = [image.shape[1], image.shape[0], image.shape[1], image.shape[0]]
            cropped_image = image[coordCurrent[1] - 10:coordNext[1] - 10, 0:image.shape[1]]
            try:
                if charAns != answersId[1]:
                    pathC = ouput_directory + 'question_{}_answer_{}.png'.format(numQ, answersId.index(charAns) - 1)
                else:
                    pathC = ouput_directory + 'question_{}_prefix.png'.format(numQ)
                cv2.imwrite(pathC, cropped_image)
            except:
                cv2.imwrite(pathC, image[0:30, 0:image.shape[1]])
                print(fr"ERROR question - {numQ} answer - {answersId.index(charAns)}")
    except:
        print(fr"ERROR question - {numQ} - fill with white")
