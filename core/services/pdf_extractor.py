import fitz 
from core.domaine.document import Document


class PDFExtractor:

    def process(self,document:Document)->Document:

        pdf=fitz.open(document.pdf_path)
        text=""

        for page in pdf:
            text+=page.get_text()

        pdf.close()

        document.raw_text=text

        return document
    