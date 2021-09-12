import os , sys, io
if hasattr(sys,'frozen'):
    os.enversion['PATH'] = sys._MEIPASS + ';' + os.version('PATH')
import requests 
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter



# https://realpython.com/pdf-python/ guide for PDF2 
#  




input_dir = './sampleFolder'

# Get all the PDF files
filesPDF = []
os.chdir(input_dir)
print(os.getcwd())
for pdfName in os.listdir():
    if pdfName.endswith('.pdf'):
        filesPDF.append(pdfName)

filesPDF.sort(key=str.lower)

# write pdf files 
pdfWriter = PdfFileWriter()
# loop through all pdf files: 
for filename in filesPDF:
    print(filename)
    pdfReader = PdfFileReader(filename) # open each file exist 
    for page in range(pdfReader.getNumPages()):
        pdfWriter.addPage(pdfReader.getPage(page)) # write each file to pdf
        
    
mergedName= str(input("Choose the name: ")) + ".pdf"
pdfMerged = open(mergedName,"wb")
pdfWriter.write(pdfMerged)
pdfMerged.close()



