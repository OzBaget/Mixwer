import cv2
import editBox
import editFiles
import listFinds



def export_questions(array_path, ouput_directory):
    HEIGHT_BEGIN_Q = 140
    coordNext = []
    questions_paths = []
    QueQ = "שאלה"
    general_num_Q = 1
    for img in array_path:
        lastQ = False
        page_num_Q = 1
        open_img = cv2.imread(img)
        first_words = listFinds.find_first_words(img,["שאלה"] ,False,True)
        if first_words['text'].count("שאלה") == 0:
            lastQ = True
        if img == array_path[0] and lastQ:
            continue
        while not lastQ:
            if page_num_Q < first_words['text'].count("שאלה"):
                coordCurrent = editBox.wordToBox(QueQ, first_words, [QueQ], page_num_Q)
                coordNext = editBox.wordToBox(QueQ, first_words, [QueQ], page_num_Q + 1)
                if(coordCurrent[1] > 10):
                    cropped_image = open_img[coordCurrent[1] - 10:coordNext[1] - 10, 0:open_img.shape[1]]
                else:
                    cropped_image = open_img[coordCurrent[1] :coordNext[1] - 10, 0:open_img.shape[1]]
            else: #last q in the page
                coordCurrent = editBox.wordToBox(QueQ, first_words, [QueQ], page_num_Q)
                if coordCurrent[1]>10:
                    cropped_image = open_img[coordCurrent[1] - 10:open_img.shape[0], 0:open_img.shape[1]]
                else:
                    cropped_image = open_img[coordCurrent[1]:open_img.shape[0], 0:open_img.shape[1]]
                lastQ = True
            path = ouput_directory + 'question_{}.png'.format(general_num_Q)
            cv2.imwrite(path, cropped_image)
            questions_paths.append(path)
            general_num_Q += 1
            page_num_Q += 1

        # Check if some answers of the previous page there are in the begining of the page
        if first_words['text'].count("שאלה") != 0 and editBox.wordToBox(QueQ, first_words, [QueQ], 1)[
            1] > HEIGHT_BEGIN_Q and general_num_Q > page_num_Q or first_words['text'].count("שאלה") == 0:
            if first_words['text'].count("שאלה") != 0:
                coordCurrent = editBox.wordToBox(QueQ, first_words, [QueQ], 1)
            else:
                coordCurrent = [0,open_img.shape[0],0,0]
            cropped_image = open_img[0:coordCurrent[1], 0:open_img.shape[1]]
            path = ouput_directory + 'continue_question_{}.png'.format(general_num_Q - page_num_Q)
            cv2.imwrite(path, cropped_image)

            merge_png = [ouput_directory + 'question_{}.png'.format(general_num_Q - page_num_Q)
                , path]
            editFiles.combineFiles(merge_png
                                   , ouput_directory + 'question_{}'.format(general_num_Q - page_num_Q))

    return questions_paths,general_num_Q-1


def export_answers(path, answersId, ouput_directory):
    image = cv2.imread(path)
    first_words = listFinds.find_first_words(path, answersId,False)
    halfPath = path[path.rfind("\\") + 1:]
    numQ = int(halfPath[9:-4])
    if numQ == 9:
        pass
    coordNext = []
    for charAns in answersId[1:]:
        if charAns == answersId[1]:
            coordNext = [0, 10, 0, 0]
        coordCurrent = coordNext
        # if it is the last answer in the qestion
        if charAns != answersId[-1]:
            coordNext = editBox.wordToBox(charAns, first_words, answersId)
        else:
            coordNext = [image.shape[1], image.shape[0], image.shape[1], image.shape[0]]
        cropped_image = image[coordCurrent[1] - 10:coordNext[1] - 10, 0:image.shape[1]]
        try:
            if charAns != answersId[1]:
                path = ouput_directory + 'question_{}_answer_{}.png'.format(numQ, answersId.index(charAns) - 1)
                cv2.imwrite(path, cropped_image)
            else:
                path = ouput_directory + 'question_{}_prefix.png'.format(numQ)
                cv2.imwrite(path, cropped_image)
        except:
            cv2.imwrite(path, image[0:30, 0:image.shape[1]])
            print(fr"ERROR question - {numQ} answer - {answersId.index(charAns)}")
