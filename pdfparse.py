#encoding:utf-8

"""
parse pdf file with python
get data from table

"""
import sys
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def parse():
    fp=open('20150623043633273.pdf','rb')
    praser=PDFParser(fp)
    doc=PDFDocument()
    praser.set_document(doc)
    
    doc.set_parser(praser)
    doc.initialize()

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr=PDFResourceManager()
        laparams=LAParams()
        device=PDFPageAggregator(rsrcmgr,laparams=laparams)
        interpreter=PDFPageInterpreter(rsrcmgr,device)
        
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout=device.get_result()

            for x in layout:
                if(isinstance(x,LTTextBoxHorizontal)):
                    with open(r'2015g.txt')as f:
                        results=x.get_text()
                        print(results)
                        f.write(results+'\n')

if __name__=='__main__':
    parse()
    
