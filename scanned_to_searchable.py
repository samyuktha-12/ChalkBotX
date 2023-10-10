import os
import pdf2image
import pytesseract
import cv2
import pypdf

pytesseract.pytesseract.tesseract_cmd="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
TESSDATA_PREFIX="C:\\Program Files\\Tesseract-OCR"
tessdata_dir_config='--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'


def image_conversion(inpath):
  OUTPUT_FOLDER=None
  FIRST_PAGE=None
  LAST_PAGE=None
  FORMAT='jpg'
  USERPWD=None
  USE_CROPBOX=None
  STRICT=False
  pil_images=pdf2image.convert_from_path(inpath,output_folder=OUTPUT_FOLDER,first_page=FIRST_PAGE,last_page=LAST_PAGE,fmt=FORMAT,userpw=USERPWD,use_cropbox=USE_CROPBOX,strict=STRICT)
  i=0
  for image in pil_images:
    image.save("images_path/converted_image"+str(i)+".jpg")
    i+=1
  print("ALL PAGES CONVERTED TO IMAGE")

def pdf_conversion(folder_dir):
  i=0
  for images in os.listdir(folder_dir):
    img=cv2.imread("images_path/"+images,1)
    result=pytesseract.image_to_pdf_or_hocr(img,lang="eng",config=tessdata_dir_config)
    f=open("pages/searchablepdf"+str(i)+".pdf","w+b")
    f.write(bytearray(result))
    f.close()
    i+=1
  print("ALL IMAGES CONVERTED TO PDF")

def merge_pdf(pdf_folder,filename):
  merger = pypdf.PdfMerger()
  for pdf in os.listdir(pdf_folder):
    merger.append(pdf_folder+'/'+pdf)
  merger.write('result/'+filename+".pdf")
  merger.close()
  print("PDF MERGED")

def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")



