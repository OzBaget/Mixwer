import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import editFiles


def reCrop(numQ,numOfAnswers,ouput_directory,detailsBetweenQ):
    for i in range(1,numQ+1):
        for j in range(1,numOfAnswers+1):
            pathImage = ouput_directory + "question_{}_answer_{}.png".format(i, j)
            # Crop the space between char and answer
            cropSpaceAnswerPng(pathImage)
            # Crop the space between char and answer
            cropSpaceEndPng(pathImage)
            #Crop the space between the answer and the nextQuestion
            if detailsBetweenQ: #if there is detailes before qeustion and the next qeustion
                cropSpaceAnswerPng(pathImage, True)

def lastWhiteLineCoordPng(path):
        img = cv2.imread(path)
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Set the threshold for what is considered white
        white_threshold = 255
        # Get the shape of the image
        height, width = gray.shape
        # Calculate the average intensity for each row
        avg_intensity = [sum(row) / width for row in gray]

        # Find the first row where the average intensity is less than the threshold
        for i, intensity in enumerate(avg_intensity[::-1]):
            if intensity < white_threshold:
                return height - i
        return 0


def firstNotWhiteLineCoordPng(path, bigSpace, contiueSearchBigSpace):
    image = cv2.imread(path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Get the shape of the image
    height, width = gray.shape
    # Set the threshold for what is considered white
    white_threshold = 255
    # Calculate the average intensity for each row
    end = min(1000, height)
    avg_intensity = [sum(row) / width for row in gray[20:end]]

    # Find the first row where the average intensity is less than the threshold
    i = 1
    while i < len(avg_intensity):
        isThisEnoughBigSpace = True
        if avg_intensity[i] == white_threshold:
            j = i
            while j < len(avg_intensity) and isThisEnoughBigSpace:
                if j < i + bigSpace and avg_intensity[j] != white_threshold:
                    isThisEnoughBigSpace = False
                    i = j
                    if not contiueSearchBigSpace:
                        break
                if not contiueSearchBigSpace:
                    if j > i+bigSpace and isThisEnoughBigSpace and avg_intensity[j] != white_threshold:
                        return j+20
                else:
                    if j > i + bigSpace and isThisEnoughBigSpace and avg_intensity[j] == white_threshold:
                        return i
                j += 1
            if not isThisEnoughBigSpace and not contiueSearchBigSpace:
                break

        i+=1
    return False



def cropSpaceEndPng(path):
    image = cv2.imread(path)
    height = lastWhiteLineCoordPng(path)
    cropped = image[:height+10, :]
    cv2.imwrite(path, cropped)

def cropSpaceAnswerPng(path, mid = False):
    image = cv2.imread(path)
    height = firstNotWhiteLineCoordPng(path,20,mid)
    if not height:
        return
    if not mid:
        cropped = np.vstack((image[0:30, :], image[height:, :]))
    if mid:
        cropped = image[:height+20, :]
    cv2.imwrite(path, cropped)


def rewriteAnswer(path,i,location):
    text = ".{}".format(i)
    text_height, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    imageQ = cv2.imread(path)
    cv2.rectangle(imageQ, (location, 0),
                  (imageQ.shape[1], imageQ.shape[0]), (255, 255, 255), -1)
    cv2.imwrite(path, imageQ)
    cv2.putText(imageQ, text, (imageQ.shape[1] - 170, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imwrite(path, imageQ)

def createAnswersPage(path_answers):
    PAGE_HEIGHT = 1805
    PAGE_WIDTH = 1700
    image_array =[]
    num_answer = 1
    prefix_path = path_answers[1][:path_answers[1].rfind("\\")+1]
    current_path = ""

    num_q = 0
    for cpath in path_answers:
        if cpath[cpath.rfind("_") + 1:-4] == 'prefix':
            num_answer = 0
        if cpath[cpath.rfind("_") + 1:-4] == '1':
            num_q = cpath[cpath.find("_")+1:cpath.rfind("_")-7]
            blank = Image.new("RGBA", (PAGE_WIDTH, 70), (255, 255, 255, 255))
            text = "{} :{}".format(num_answer
                                  ,num_q)
            font = ImageFont.truetype('arial.ttf', 40)
            draw = ImageDraw.Draw(blank)
            text_width, text_height = draw.textsize(text, font=font)

            text_x = (PAGE_WIDTH - text_width) / 2
            text_y = (70 - text_height) / 2

            # Draw text on the image
            draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
            current_path = prefix_path+fr"answer_{num_q}.png"
            blank.save(current_path)
            image_array.append(current_path)
        num_answer+=1

    return editFiles.combineFilestoPages(image_array,prefix_path,1000,"AnswerPage"),image_array


