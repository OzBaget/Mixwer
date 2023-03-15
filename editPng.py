import cv2
import numpy as np


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

