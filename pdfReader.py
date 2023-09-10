import PyPDF2
from gtts import gTTS


# function to read pdf
def read_pdf(name, start_page=0, end_page=None):
    path = open(name, 'rb')

    pdfReader = PyPDF2.PdfReader(path)

    # initialize text variable
    text = ''

    # get the end page
    if end_page is None:
        end_page = len(pdfReader.pages)
    else:
        end_page = min(end_page, len(pdfReader.pages))

    # loop through specified pages
    for page_num in range(start_page, end_page):
        page = pdfReader.pages[page_num]
        text += page.extract_text()

    # reading the text
    tts = gTTS(text=text, lang='en')
    
    # save output with pdf name
    output_name = name.replace(".pdf", ".mp3")
    tts.save(output_name)

# main function
def main():
    name = input("Enter Name of PDF: ")
    start_page = input("Enter start page (leave blank for first page): ")
    end_page = input("Enter end page (leave blank for last page): ")

    if start_page:
        start_page = int(start_page) - 1
    else:
        start_page = 0

    if end_page:
        end_page = int(end_page)
    else:
        end_page = None

    read_pdf(name, start_page, end_page)


main()
