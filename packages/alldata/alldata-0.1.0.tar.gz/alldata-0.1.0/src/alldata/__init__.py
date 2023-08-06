__version__ = '0.0.2'

import os
import fitz
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from tabula import read_pdf
import tabula
import camelot
import nltk
from nltk.corpus import stopwords
from text_summarizer import generate_summary
from nltk.cluster.util import cosine_distance
import numpy as np
import threading
import networkx as nx

class Table:
    def __init__(self,address):
        self._address = address


    def extractTableCsv(self):
        if 'extractedTablesCsv' in os.listdir():
            pass
        else:
            os.mkdir('extractedTablesCsv')
        try:
            tables = tabula.convert_into(self._address,"extractedTablesCsv/extractedCSVAll.csv",pages='all')
            if tables is None:
                print('[!] No table found an empty file created')
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)

    def extractTableJson(self):
        if 'extractedTablesJson' in os.listdir():
            pass
        else:
            os.mkdir('extractedTablesJson')
        try:
            tables = tabula.convert_into(self._address,"extractedTablesJson/extractedJsonAll.json",pages='all')
            if tables is None:
                print('[!] No table found an empty file created')
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)

    def extractTableHTML(self):
        if 'extractedTablesHTML' in os.listdir():
            pass
        else:
            os.mkdir('extractedTablesHTML')
        try:
            tables = camelot.read_pdf(self._address,pages='all')
            if len(tables)<1:
                print("[!] No Table Found")
                return
            tables.export("extractedTablesHTML/tablesHTMLAll.html", f="html")
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)

    def extractSpecPageTableHTML(self,page):
        if 'extractedTablesHTML' in os.listdir():
            pass        
        else:
            os.mkdir('extractedTablesHTML')
        try:
            tables = camelot.read_pdf(self._address,pages=str(page))
            if len(tables)<1:
                print("[!] No Table Found")
                return
            tables.export(f"extractedTablesHTML/tablesHTML{page}.html", f="html")
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except IndexError:
            print("[!] Page Not Found")
        except Exception as e:
            print(e)

    def extractSpecPageTableCsv(self,page):
        if 'extractedTablesCsv' in os.listdir():
            pass
       
        else:
            os.mkdir('extractedTablesCsv')
        try:
            tables = tabula.read_pdf(self._address,pages='all')
            if len(tables)<page:
                print('[!] Invalid Page Number')
                return
            tables = tabula.convert_into(self._address, f"extractedTablesCsv/OutputCsv{page}.csv", output_format="csv", pages=page)
            if tables is None:
                print('[!] No table found an empty file created')
        except FileNotFoundError:
            print("[!] File not found Invalid address")
        except Exception as e:
            print(e)
    def extractSpecPageTableJson(self,page):
        if 'extractedTablesJson' in os.listdir():
            pass
       
        else:
            os.mkdir('extractedTablesJson')
        try:
            tables = tabula.read_pdf(self._address,pages='all')
            if len(tables)<page:
                print('[!] Invalid Page Number')
                return
            tables = tabula.convert_into(self._address, f"extractedTablesJson/OutputJson{page}.json", output_format="json", pages=page)
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
        if 'extractedImages' in os.listdir():
            pass
        else:
            os.mkdir('extractedImages')
        doc = fitz.open(self._address)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                if len(doc.getPageImageList(i))==0:
                    print(f'[!]No Image Found on {i}')
                xref = img[0] 
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5: 
                    pix.writePNG("extractedImages/p%s-%s.png" % (i, xref))
                else: 
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)  
                    pix1.writePNG("extractedImages/p%s-%s.png" % (i, xref))
                    pix1 = None  
                pix = None  
    def extract_images(pdf, pages):
        threads = []
        for page in pages:
            temp = threading.Thread(target=extract_image, args=(pdf, page, ))
            temp.start()
            print(f"thread launched for page - {page}") 
        extract_images("PDF_Samples/AutoCad_Diagram.pdf", pages=list(range(19)))
    def extractImageSpecPage(self,page):
        if 'extractedImages' in os.listdir():
            pass
        else:
            os.mkdir('extractedImages')
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
                        pix.writePNG("extractedImages/p%s-%s.png" % (i, xref))
                    else:  
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)  
                        pix1.writePNG("extractedImages/p%s-%s.png" % (i, xref))
                        pix1 = None  
                    pix = None 


class Text:
    def __init__(self,address):
        self._address = address


    def extractTextAll(self):
        if 'extractedTextAll' in os.listdir():
            pass
        else:
            os.mkdir('extractedTextAll')
        try:
            pdf = PdfFileReader(self._address)
        except FileNotFoundError:
            print("[!] No File Found ")
            return
        with open('extractedTextAll/extractText.txt','w') as f:
            for page_num in range(pdf.numPages):
                pageObj = pdf.getPage(page_num)
                f.write(pageObj.extractText())
            f.close()

    def extractTextSpecPage(self,page):
        if 'extractedTextAll' in os.listdir():
            pass
        else:
            os.mkdir('extractedTextAll')
        try:
            pdf = PdfFileReader(self._address)
        except FileNotFoundError:
            print("[!] No File Found ")
            return
        with open(f'extractedTextAll/extractTextPage{page}.txt','w') as f:
            pageObj = pdf.getPage(page)
            f.write(pageObj.extractText())
            f.close()

class Summarize:
    def __init__(self,address):
        self._address=address

    def read_article(self):
        file = open(self._address, "r")
        filedata = file.readlines()
        article = filedata[0].split(".")
        sentences = []

        for sentence in article:
            print(sentence)
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop() 
    
        return sentences

    def sentence_similarity(self,sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []

        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]

        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

    # build the vector for the first sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1

        return 1 - cosine_distance(vector1, vector2)
 
    def build_similarity_matrix(self,sentences, stop_words):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2: #ignore if both are same sentences
                    continue 
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix


    def generate_summary(self,file_name, top_n=5):
        nltk.download("stopwords")
        stop_words = stopwords.words('english')
        summarize_text = []

        # Step 1 - Read text anc split it
        sentences =  read_article(file_name)

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
        print("Indexes of top ranked_sentence order are ", ranked_sentence)    

        for i in range(top_n):
            summarize_text.append(" ".join(ranked_sentence[i][1]))

        # Step 5 - Offcourse, output the summarize texr
        print("Summarize Text: \n", ". ".join(summarize_text))
    def summarizer(self):
        f = open("extracted_text.txt", 'w')

        for page in range(19):
            print (page)
        try:
            f.write(extract_text("maviya.pdf", page=page))
            f.write("\n")
        except:
            print ("<no text>")

        f.close()
        generate_summary( "extracted_text.txt", 3)
