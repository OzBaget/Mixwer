# Mixwer
Belender answers of tests in JCT.
## Usage
run UI.py and upload your PDFs.

The Project work with PDF that the answers in AlephBet template like - 

![alt tag](https://github.com/OzBaget/Mixwer/blob/main/Screenshots/GoodQ.png)

but not like

![alt tag](https://github.com/OzBaget/Mixwer/blob/main/Screenshots/BadQ1.png)

or

![alt tag](https://github.com/OzBaget/Mixwer/blob/main/Screenshots/BadQ2.png)


## Setup

Clone the project: git clone [https://github.com/OzBaget/Mixwer](https://github.com/OzBaget/Mixwer)

Navigate to the project directory: cd /path/to/TestsShuffler

Install dependencies: Activate the setup.py file and install all the necessary packages: pip install .

Install Tesseract OCR:

Download and install Tesseract OCR from here.
After installation, navigate to C:\Program Files\Tesseract-OCR\tessdata.
Remove the heb.traineddata file and replace it with the provided heb.traineddata file from the project.
Configure Blender Paths:
Navigate to blender/paths directory in the project.
Update Blender paths in the path file if necessary. Default paths might suffice.
Install Poppler:
Download Poppler from here.
Extract the zip file to a location you can remember.
Update the path file to include the location of Poppler:
poppler_path=r"C:\Program Files (x86)\poppler-23.11.0\Library\bin"
Run the server: python server/server.py
Ensure you follow each step carefully to set up the project correctly.
