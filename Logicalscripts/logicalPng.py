import os

from PIL import Image, ImageFont, ImageDraw

from FunctionalScripts import functionalFiles
from FunctionalScripts import editPng
def createAnswersPage(path_answers):
    PAGE_HEIGHT = 1805
    PAGE_WIDTH = 1700
    image_array = []
    num_answer = 1
    prefix_path = path_answers[1][:path_answers[1].rfind("\\") + 1]
    current_path = ""

    num_q = 0
    for cpath in path_answers:
        pathEnd = cpath[cpath.rfind("_") + 1:-4]
        if pathEnd == 'prefix':
            num_answer = 1
        elif pathEnd == '1':
            num_q = cpath[cpath.find("_") + 1:cpath.rfind("_") - 7]
            blank = Image.new("RGBA", (PAGE_WIDTH, 70), (255, 255, 255, 255))
            text = "Question {} : Answer {}".format(num_q
                                   , num_answer)
            font = ImageFont.truetype('arial.ttf', 40)
            draw = ImageDraw.Draw(blank)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]


            text_x = (PAGE_WIDTH - text_width) / 2
            text_y = (70 - text_height) / 2

            # Draw text on the image
            draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
            current_path = prefix_path + fr"answer_{num_q}.png"
            blank.save(current_path)
            image_array.append(current_path)
        try:
            int(pathEnd)
            num_answer += 1
        except:
            pass

    return combineFilestoPages(image_array, prefix_path, "AnswerPage"), image_array


def cropAnswers():
    ouput_directory,list_files = functionalFiles.getFilesPaths()
    for pathC in enumerate(list_files):
        if "answer" in pathC[1] or "prefix" in pathC[1]:
            editPng.cropSpaceEndPng(functionalFiles.getOutputDirectoryPath()+pathC[1])


def combineFilestoPages(array_path, output_dir,prefixFile = "final_page"):
    page_num = 1
    total_height = 0
    images_to_combine = []
    total_page_path  = []
    topAndBottonArray  = []
    PAGE_HEIGHT = 1805
    PAGE_WIDTH = 1700
    BEGIN_HEIGHT = 200
    for i, path in enumerate(array_path):
        img = Image.open(path)
        # Add white blank after every Q files
        if path[path.rfind("_")+1:-4] == "prefix" and page_num != 1:
            if total_height + 70 < PAGE_HEIGHT - BEGIN_HEIGHT:
                padding = Image.new("RGBA", (PAGE_WIDTH, 70), (255, 255, 255, 255))
                images_to_combine.append(padding)
                total_height += padding.size[1]
        #If the Q is bigger than page, we have to split it
        if  img.size[1] > PAGE_HEIGHT-BEGIN_HEIGHT:
            rest_page = PAGE_HEIGHT- total_height - BEGIN_HEIGHT
            topAndBotton = editPng.crop_png_middle(path, int(rest_page / 2))
            if not topAndBotton:
                topAndBotton = editPng.crop_png_middle(path, int(rest_page / 2), 25)
            if not topAndBotton:
                topAndBotton = editPng.crop_png_middle(path, int(rest_page / 2), 10)
            if not topAndBotton:
                topAndBotton = editPng.crop_png_middle(path, int(rest_page / 2), 0, True)
            array_path.insert(i+1,topAndBotton[0])
            array_path.insert(i+2,topAndBotton[1])
            topAndBottonArray.insert(0,topAndBotton[0])
            topAndBottonArray.insert(0,topAndBotton[1])

            continue
        if total_height + img.size[1] > PAGE_HEIGHT-BEGIN_HEIGHT:
            # Add white padding to fill the remaining space in the page height
            padding_height = PAGE_HEIGHT-BEGIN_HEIGHT - total_height
            padding = Image.new("RGBA", (PAGE_WIDTH, padding_height), (255, 255, 255, 255))
            images_to_combine.append(padding)
            if page_num != 1:
                padding = Image.open(r"Used Png/Final Pages Png/beginPage.png")
                images_to_combine.insert(0,padding)
            else:
                padding = Image.open(r"Used Png/Final Pages Png/FirstbeginPage.png")
                images_to_combine.insert(0,padding)

            # Combine the images and save to a new file
            result = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color = (255, 255, 255))
            y_offset = 0
            for imgtemp in images_to_combine:
                result.paste(imgtemp, (0, y_offset))
                y_offset += imgtemp.size[1]

            output_path_current = os.path.join(output_dir, f"{prefixFile}_{page_num}.png")
            result.save(output_path_current)

            total_page_path.append(output_path_current)
            # Reset the variables for the next page
            page_num += 1
            total_height = 0
            images_to_combine = []

        # Add the current image to the list of images to be combined
        images_to_combine.append(img)
        total_height += img.size[1]



    # Check if there are any remaining images to be combined
    if len(images_to_combine) > 0:
        # Add white padding to fill the remaining space in the page height
        padding_height = PAGE_HEIGHT - BEGIN_HEIGHT - total_height
        padding = Image.new("RGBA", (PAGE_WIDTH, padding_height), (255, 255, 255, 255))
        images_to_combine.append(padding)

        padding = Image.open(r"Used Png/Final Pages Png/beginPage.png")
        images_to_combine.insert(0, padding)

        # Combine the images and save to a new file
        result = Image.new("RGBA", (PAGE_WIDTH, PAGE_HEIGHT),(255, 255, 255, 255))
        y_offset = 0
        for img in images_to_combine:
            result.paste(img, (0, y_offset))
            y_offset += img.size[1]

        output_path_current = os.path.join(output_dir, f"{prefixFile}_{page_num}.png")
        result.save(output_path_current)
        total_page_path.append(output_path_current)
        page_num += 1
    return total_page_path
