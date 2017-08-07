from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter


from pdfminer.layout import LAParams
from pdfminer.converter import XMLConverter
from io import BytesIO

from lxml import etree


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

fp.close()
device.close()

xml_parser = etree.XMLParser(remove_blank_text=True)

root = etree.fromstring(retstr.getvalue(), parser=xml_parser)

for element in root.iter("text"):
    print(etree.tostring(element, pretty_print=True))
    #print("%s - %s" % (element.tag, element.text))


retstr.close()