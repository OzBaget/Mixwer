from datetime import datetime
import tkinter as tk
from tkinter import ttk,filedialog
from PIL import Image, ImageTk

import FunctionalScripts.functionalFiles
import  Main
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
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    array_paths,successFlag = Main.main(file_paths)
    if successFlag:
        current_datetime = datetime.now()
        # Format the datetime as a string
        datetime_string = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

        zip_path = filedialog.asksaveasfilename(initialfile="Mixwer - "+datetime_string+".zip",defaultextension=".zip", filetypes=[("ZIP Files", "*.zip")])

        FunctionalScripts.functionalFiles.zipPdf(array_paths,zip_path)
    #TODO: call AnswerMixer main. at the end ask user where to save the zip
uploadFilesButton.configure(command=UploadFiles_button_click)

window.mainloop()
