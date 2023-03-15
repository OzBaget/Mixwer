from PIL import Image
from pdf2image import convert_from_path
import os
from PyPDF2 import PdfReader, PdfWriter


def png_to_pdf(sourcePath, destPath,pathOfPdf):
    png = Image.open(sourcePath)
    im_1 = png.convert('RGB')
    fileName = pathOfPdf[pathOfPdf.rfind("\\") + 1:-4] + " מעורבל" + pathOfPdf[-4:]
    destPath = destPath + fileName
    im_1.save(destPath)
    split_pdf(destPath)

def split_pdf(pathOfPdf):
    pdf_to_png(pathOfPdf,pathOfPdf[pathOfPdf.rfind("\\") + 1])

def pdf_to_png(pathSource, pathDest):
    pages = convert_from_path(pathSource)
    paths = []
    for i, page in enumerate(pages):
        (width, height) = page.size
        crop_box = (0, 0+150, width, height - 200)
        page = page.crop(crop_box)
        paths.append(pathDest + f'page_{i}.png')
        page.save(pathDest + f'page_{i}.png', 'PNG')
    return paths


def delete_files(paths):
    for i in range(len(paths)):
        os.remove(paths[i])

def combineFiles(arrayPath,output_path):
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
    result.save(output_path+'.png')
    return output_path+'.png'





def combineFilestoPages(array_path, output_dir,numA):
    page_num = 1
    total_height = 0
    images_to_combine = []
    total_page_path  = []
    PAGE_HEIGHT = 3308
    PAGE_WIDTH = 1700
    BEGIN_HEIGHT = 200
    for i, path in enumerate(array_path):
        img = Image.open(path)
        if total_height + img.size[1] > PAGE_HEIGHT-BEGIN_HEIGHT:
            # Add white padding to fill the remaining space in the page height
            padding_height = PAGE_HEIGHT-BEGIN_HEIGHT - total_height
            padding = Image.new("RGBA", (PAGE_WIDTH, padding_height), (255, 255, 255, 255))
            images_to_combine.append(padding)



            padding = Image.open(array_path[1][:array_path[1].rfind('\\')+1]+"beginPage.png")
            images_to_combine.insert(0,padding)

            # Combine the images and save to a new file
            result = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color = (255, 255, 255))
            y_offset = 0
            for imgtemp in images_to_combine:
                result.paste(imgtemp, (0, y_offset))
                y_offset += imgtemp.size[1]

            output_path_current = os.path.join(output_dir, f"page_{page_num}.png")
            result.save(output_path_current)

            total_page_path.append(output_path_current)
            # Reset the variables for the next page
            page_num += 1
            total_height = 0
            images_to_combine = []

        # Add the current image to the list of images to be combined
        images_to_combine.append(img)
        total_height += img.size[1]

        # Add white blank after every 6 files
        if (i + 1) % (numA+1) == 0:
            if total_height + 70 < PAGE_HEIGHT - BEGIN_HEIGHT:
                padding = Image.new("RGBA", (PAGE_WIDTH, 70), (255, 255, 255, 255))
                images_to_combine.append(padding)
                total_height += padding.size[1]

    # Check if there are any remaining images to be combined
    if len(images_to_combine) > 0:
        # Add white padding to fill the remaining space in the page height
        padding_height = PAGE_HEIGHT - BEGIN_HEIGHT - total_height
        padding = Image.new("RGBA", (PAGE_WIDTH, padding_height), (255, 255, 255, 255))
        images_to_combine.append(padding)

        padding = Image.open(array_path[1][:array_path[1].rfind('\\') + 1] + "beginPage.png")
        images_to_combine.insert(0, padding)

        # Combine the images and save to a new file
        result = Image.new("RGBA", (PAGE_WIDTH, PAGE_HEIGHT),(255, 255, 255, 255))
        y_offset = 0
        for img in images_to_combine:
            result.paste(img, (0, y_offset))
            y_offset += img.size[1]

        output_path = os.path.join(output_dir, f"page_{page_num}.png")
        result.save(output_path)

        page_num += 1

    return total_page_path
