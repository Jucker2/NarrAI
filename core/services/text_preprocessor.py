import re

from core.domaine.document import Document

class TextPreprocessor:
    def process(self,document:Document)->Document:
        
        text=document.clean_text

        #remplacer les espaces multiples
        text=re.sub(r"[ \t]+"," ",text)

        #corriger les lignes vides multiples
        text=re.sub(r"\n{3,}", "\n\n",text)

        #reunir les mots coupés par un retour à la ligne
        text=re.sub(r"-\n","",text)

        document.clean_text=text.strip()
        return document
    
   