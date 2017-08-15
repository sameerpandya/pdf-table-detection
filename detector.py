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



def get_text_groups(file):
    parser = PDFParser(file)

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

    file.close()
    device.close()

    xml_parser = etree.XMLParser(remove_blank_text=True)

    root = etree.fromstring(retstr.getvalue(), parser=xml_parser)

    n = 0

    for element in root.iterdescendants():
        if element.tag in ['textgroup']:
            n += 1
            print(element.tag + " " + str(n))
            children = element.getchildren()
            for child in children:
                if child.tag in ['textbox']:
                    print('\t' + child.tag)
                    break

    retstr.close()

    return

def main():
    fp = open('test.pdf', 'rb')
    text_groups = get_text_groups(fp)

if __name__ == '__main__':
    main()