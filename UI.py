from datetime import datetime
import tkinter as tk
from tkinter import ttk,filedialog
from PIL import Image, ImageTk

import FunctionalScripts.functionalFiles
import  Main
import  os
window = tk.Tk()
window.title("Mixwer")
window.geometry("500x500")
window.resizable(False, False)  # Disable resizing



#set background image
background_image_path = r'Used Png\UI\background.png'
background_image = Image.open(background_image_path)
background_photo = ImageTk.PhotoImage(background_image)

label = tk.Label(window, image=background_photo)
label.place(x=-2, y=0)

#set uploadFiles button
uploadButton_image_path = r"Used Png\UI\buttonUplodFiles.png"
uploadButton_photo = ImageTk.PhotoImage(file = uploadButton_image_path)

uploadFilesButton = ttk.Button(window,image=uploadButton_photo,  command=lambda: print("Button clicked!"))
uploadFilesButton.place(x=500/2 - 270/2, y=400)

def UploadFiles_button_click():
    # Let the user select PDF files
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if not file_paths:
        return  # User canceled

    # Call the main function to process the PDFs
    array_paths, successFlag = Main.main(file_paths)

    if successFlag:
        print("Processing files")
        # Ensure output folder exists
        final_zip_dir = "Final ZIPs\\"
        os.makedirs(final_zip_dir, exist_ok=True)

        # Generate filename with timestamp
        current_datetime = datetime.now()
        datetime_string = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"Mixwer - {datetime_string}.zip"
        zip_path = os.path.join(final_zip_dir, zip_filename)

        # Create the zip file
        FunctionalScripts.functionalFiles.zipPdf(array_paths, zip_path)

        print(f"ZIP saved to: {zip_path}")


uploadFilesButton.configure(command=UploadFiles_button_click)

window.mainloop()
