__version__ = '0.0.0'


import fitz
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from tabula import read_pdf
import tabula
import camelot

class Table:
    def __init__(self,address):
        self._address = address


    def extractTableCsv(self):
        try:
            tables = tabula.convert_into(self._address,"extractedCSVAll.csv",pages='all')
            if tables is None:
                print('[!] No table found an empty file created')
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)

    def extractTableJson(self):
        try:
            tables = tabula.convert_into(self._address,"extractedJsonAll.json",pages='all')
            if tables is None:
                print('[!] No table found an empty file created')
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)

    def extractTableHTML(self):
        try:
            tables = camelot.read_pdf(self._address,pages='all')
            if len(tables)<1:
                print("[!] No Table Found")
                return
            tables.export("tablesHTMLAll.html", f="html")
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)

    def extractSpecPageTableHTML(self,page):
        try:
            tables = camelot.read_pdf(self._address,pages=str(page))
            if len(tables)<1:
                print("[!] No Table Found")
                return
            tables.export(f"tablesHTML{page}.html", f="html")
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except IndexError:
            print("[!] Page Not Found")
        except Exception as e:
            print(e)

    def extractSpecPageTableCsv(self,page):
        try:
            tables = tabula.read_pdf(self._address,pages='all')
            if len(tables)<page:
                print('[!] Invalid Page Number')
                return
            tables = tabula.convert_into(self._address, f"OutputCsv{page}.csv", output_format="csv", pages=page)
            if tables is None:
                print('[!] No table found an empty file created')
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)
    def extractSpecPageTableJson(self,page):
        try:
            tables = tabula.read_pdf(self._address,pages='all')
            if len(tables)<page:
                print('[!] Invalid Page Number')
                return
            tables = tabula.convert_into(self._address, f"OutputJson{page}.json", output_format="json", pages=page)
            if tables is None:
                print('[!] No table found an empty file created')
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)

class Image:
    def __init__(self,address):
        self._address = address

    def extractImageAll(self):
        doc = fitz.open(self._address)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                if len(doc.getPageImageList(i))==0:
                    print(f'[!]No Image Found on {i}')
                xref = img[0] 
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5: 
                    pix.writePNG("p%s-%s.png" % (i, xref))
                else: 
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)  
                    pix1.writePNG("p%s-%s.png" % (i, xref))
                    pix1 = None  
                pix = None  
    def extractImageAllJpeg(self):
        doc = fitz.open(self._address)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                if len(doc.getPageImageList(i))==0:
                    print(f'[!]No Image Found on {i}')
                xref = img[0]  
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:  
                    pix.writeJpeg("p%s-%s.jpeg" % (i, xref))
                else:  
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)  
                    pix1.writeJpeg("p%s-%s.jpeg" % (i, xref))
                    pix1 = None  
                pix = None 

    def extractImageSpecPage(self,page):
        doc = fitz.open(self._address)
        if len(doc)<page:
            print("[!]Page Not Found")
            return
        for i in range(len(doc)):
            if i==page:
                if len(doc.getPageImageList(i))==0:
                    print('[!]No Image Found')
                    return
                for img in doc.getPageImageList(i):
                    xref = img[0]  
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5:  
                        pix.writePNG("p%s-%s.png" % (i, xref))
                    else:  
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)  
                        pix1.writePNG("p%s-%s.png" % (i, xref))
                        pix1 = None  
                    pix = None 


class Text:
    def __init__(self,address):
        self._address = address


    def extractTextAll(self):
        try:
            pdf = PdfFileReader(self._address)
        except FileNotFoundError:
            print("[!] No File Found ")
            return
        with open('extractText.txt','w') as f:
            for page_num in range(pdf.numPages):
                pageObj = pdf.getPage(page_num)
                f.write(pageObj.extractText())
            f.close()

    def extractTextSpecPage(self,page):
        try:
            pdf = PdfFileReader(self._address)
        except FileNotFoundError:
            print("[!] No File Found ")
            return
        with open(f'extractTextPage{page}.txt','w') as f:
            pageObj = pdf.getPage(page)
            f.write(pageObj.extractText())
            f.close()