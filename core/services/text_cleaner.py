from core.domaine.document import Document
import re


class TextCleaner:

    def process(self,document:Document)-> Document:
        text=document.raw_text
        print(text)
        text=text.replace("\r\n","\n")
        document.clean_text=text.strip()

        return document