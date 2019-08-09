import os
import fitz
from docx import Document
import cv2

def check_file(f_path):
    if f_path.endswith(".jpg") or f_path.endswith(".png") or f_path.endswith(".jpeg"):
        return 0
    if f_path.endswith(".pdf"):
        return 1
    if f_path.endswith(".docx"):
        return 2

    return -1

def pdf2text(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += (page.getText().replace("\n", " "))
    print(text.split(' '))

def doc2text(path):
    fileExtension=path.split(".")[-1]
    if fileExtension =="docx":
        docxFilename = path
        document = Document(docxFilename)
        for para in document.paragraphs:
            print(para.text)

def resize_image(img, scale_width, scale_height):
    # scale_percent = 60  # percent of original size

    width = int(img.shape[1] * scale_width)
    height = int(img.shape[0] * scale_height)
    dim = (width,
           height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    print('Resized Dimensions : ', resized.shape)
    return resized

if __name__ == "__main__":
    text = pdf2text("D:\Coding\OcrImage\\file\\NguyenQuocBinhCV.pdf")
    doc2text("D:\Coding\OcrImage\doc\\Bao+cao+CSDLDPT.docx")