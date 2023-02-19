from PIL import Image
from pdf2image import convert_from_path
import os

def png_to_pdf(sourcePath, destPath,pathOfPdf):
    png = Image.open(sourcePath)
    im_1 = png.convert('RGB')
    fileName = pathOfPdf[pathOfPdf.rfind("\\") + 1:-4] + " מעורבל" + pathOfPdf[-4:]
    destPath = destPath + fileName
    im_1.save(destPath)
    split_pdf(pathOfPdf,destPath)

def split_pdf(file_path, save_folder):
    # Open the PDF file
    image = Image.open(file_path)

    # Get the number of pages in the PDF
    pages = len(image.sequence)

    # Iterate over each page
    for i in range(pages):
        # Get the current page
        page = image.sequence[i]

        # Save the current page as a separate image
        page_image = Image.new("RGB", image.size)
        page_image.putpalette(image.palette)
        page_image.paste(page)
        page_image.save(os.path.join(save_folder, f"page_{i}.png"), "PNG")


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
