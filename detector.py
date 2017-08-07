from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter


from pdfminer.layout import LAParams
from pdfminer.converter import XMLConverter
from io import BytesIO


fp = open('test.pdf', 'rb')

parser = PDFParser(fp)

document = PDFDocument(parser, "pass")

if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

rsrcmgr = PDFResourceManager()
laparams = LAParams()
retstr = BytesIO()

device = XMLConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)

text = retstr.getvalue().decode()
print(text)

fp.close()
device.close()
retstr.close()