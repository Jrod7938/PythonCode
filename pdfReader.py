import PyPDF2
from gtts import gTTS


# function to read pdf
def pdfReader(name):
    path = open(name, 'rb')

    pdfReader = PyPDF2.PdfReader(path)

    # initialize text variable
    text = ''

    # loop through all pages
    for page_num in range(len(pdfReader.pages)):
        page = pdfReader.pages[page_num]
        text += page.extract_text()

    # reading the text
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")

# main function
def main():
    name = input("Enter Name of PDF: ")

    pdfReader(name)
    

main()

