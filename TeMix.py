import copy
import pytesseract
import cv2
from random import shuffle
from PIL import Image
from pdf2image import convert_from_path
import os



pathOfPdf = 'C:\\Users\\izeik\\Pictures\\Tesy.pdf'
pathOfAnswers = 'C:\\Users\\izeik\\PycharmProjects\\pythonProject1\\'
def delete_files(paths):
    for i in range(len(paths)):
        os.remove(paths[i])

def png_to_pdf(path):
    png = Image.open(path)
    im_1 = png.convert('RGB')
    im_1.save(pathOfPdf[:-4] + " מעורבל" + pathOfPdf[-4:])

def pdf_to_png(pathSource,pathDest):
    pages = convert_from_path(pathSource)
    paths = []
    for i, page in enumerate(pages):
        paths.append(pathDest + f'page_{i}.png')
        page.save(pathDest + f'page_{i}.png', 'PNG')
    return paths

def combineFiles(arrayPath):
    # Load the images
    images = [Image.open(path) for path in arrayPath]
    # Determine the total size of the combined image
    total_width = max(img.size[0] for img in images)
    total_height = sum(img.size[1] for img in images)

    # Create a new image to store the combined images
    result = Image.new("RGBA", (total_width, total_height))

    # Paste each image into the result
    y_offset = 0
    for img in images:
        result.paste(img, (0, y_offset))
        y_offset += img.size[1]

    # Save the result
    result.save("result.png")
    return "result.png"

def mixfiles(path, numQ, numA = 5):
    arrayAnswers = []
    for i in range(numQ):
        arrayAnswers.append([])
        for j in range(numA):
            arrayAnswers[i].append(path + "qustion_{}_answer_{}_image.png".format(i+1, j+1))
        shuffle(arrayAnswers[i])
    shuffleAnsers = []
    for i in range(numQ):
        shuffleAnsers.append(path + "qustion_{}_image.png".format(i + 1))
        for j in range(numA):
            shuffleAnsers.append(arrayAnswers[i][j])
    return shuffleAnsers


def first_word(path):
    image = cv2.imread(path)
    boxes = pytesseract.image_to_data(image, lang='eng+heb', config='--oem 2 --psm 6',
                                      output_type=pytesseract.Output.DICT)
    # Filter only the first word in line
    first_word_boxes = {'text': [], 'left': [], 'top': [], 'width': [], 'height': []}
    line_number = -1
    first_space = False
    for i in range(len(boxes["text"])):
        if boxes["text"][i] == "" and boxes["line_num"][i] != line_number:
            first_space = True
        elif boxes["text"][i] != "" and (first_space or boxes["line_num"][i] != line_number):
            line_number = boxes["line_num"][i]
            first_word_boxes['text'].append(boxes['text'][i])  # Extract the bounding boxes for each word
            first_word_boxes['left'].append(boxes['left'][i])  # Extract the bounding boxes for each word
            first_word_boxes['top'].append(boxes['top'][i])  # Extract the bounding boxes for each word
            first_word_boxes['width'].append(boxes['width'][i])  # Extract the bounding boxes for each word
            first_word_boxes['height'].append(boxes['height'][i])  # Extract the bounding boxes for each word
            if first_space:
                first_space = False

    return first_word_boxes

def stupid_find_index(words, target_word, arrayText, num):
    before = find_index(words, [(
        arrayText[
            arrayText.index(target_word) - 1])], arrayText, num)
    for i, word in enumerate(words):
        if i > before and target_word[0] in word[0]:
            return i

def find_index(words, target_word, arrayText, num):
    copy_words = copy.deepcopy(words)
    for numInline in range(num - 1):
        copy_words[find_index(copy_words, target_word, arrayText, 1)] = ''
    if target_word == 'שאלה':
        return copy_words.index(target_word)
    elif target_word == arrayText[-1]:
        return find_index(copy_words, arrayText[0], arrayText, num + 1)
    if target_word in words:
        after = find_index(copy_words, 'שאלה', arrayText, num + 1)
        index = copy_words.index(target_word)
        if index < after:
            return index
    return stupid_find_index(copy_words, target_word, arrayText, num)


def pngToLine(path, text, first_word_boxes,arrayText, num=1):
    image = cv2.imread(path)
    value_first_word = copy.deepcopy(first_word_boxes)
    words = value_first_word['text']
    x = value_first_word['left']
    y = value_first_word['top']
    w = value_first_word['width']
    h = value_first_word['height']
    target_string = text
    start_index = find_index(words,target_string,arrayText,num)
    end_index = start_index + len(target_string) - 3
    x_start, y_start, x_end, y_end = 0, y[end_index], image.shape[1], y[start_index] + h[start_index]
    return x_start, y_start, x_end, y_end


def export_elements(path,numQ):
    image = cv2.imread(path)
    numAppear = 1
    first_words = first_word(path)
    numLastQ = numQ+1
    coordNext = []
    for numQ in range(1, numLastQ):
        for charAns in answersId[1:]:
            if(numQ == 8):
                pass
            if (charAns == answersId[1]):
                coordNext = pngToLine(path, answersId[0], first_words, answersId,numAppear)
            coordCurrent = coordNext
            try:
                if numQ == numLastQ - 1 and charAns == answersId[-1]:
                    coordNext = pngToLine(path, "עמוד", first_words,answersId, numAppear+1)
                    coordNext = [coordNext[0], coordNext[1], coordNext[2] , coordNext[3]- 300]
                elif numQ != numLastQ - 1 and charAns == answersId[-1]:
                    charAns = answersId[0]
                    coordNext = pngToLine(path, charAns, first_words,answersId, numAppear+1)
                    charAns = answersId[-1]
                else:
                    coordNext = pngToLine(path, charAns, first_words,answersId, numAppear)
            except:
                continue
            cropped_image = image[coordCurrent[1]-10:coordNext[3], coordCurrent[0]:coordNext[2]]
            if charAns == "א.":
                cv2.imwrite('qustion_{}_image.png'.format(numQ), cropped_image)
                continue
            try:
                cv2.imwrite('qustion_{}_answer_{}_image.png'.format(numQ, answersId.index(charAns) - 1), cropped_image)
            except:
                continue
        numAppear += 1

def countQuestion(path):
    first_words = first_word(path)
    return first_words['text'].count("שאלה")

pages = pdf_to_png(pathOfPdf,pathOfAnswers)
pathOfImage = combineFiles(pages)
delete_files(pages)
numQ = countQuestion(pathOfImage)
export_elements(pathOfImage,numQ)
mixAnswers = mixfiles(pathOfAnswers, numQ, 5)
pathOfFile = combineFiles(mixAnswers)
delete_files(mixAnswers)
png_to_pdf(pathOfFile)


