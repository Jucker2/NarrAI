import re
from core.domaine.document import Document
from core.domaine.chapter import Chapter

class ChapterDetector:
    PATTERNS=[
        r"chapitre\s+\d+",
        r"chapter\s+\d+",
        r"^\d+\.",
    ]

    def process(self,document:Document)->Document:
        document.chapters=[]
        current_title="Introduction"
        current_content=[]

        for line in document.clean_text.splitlines():
            line=line.strip()
            if not line:
                continue

            is_title=False

            for pattern in self.PATTERNS:
                if re.match(pattern,line,re.IGNORECASE):
                    if current_content:
                        document.chapters.append(Chapter(title=current_title,content="\n".join(current_content)))
                    current_title=line
                    currnet_content=[]
                    break
                    is_title=True
                    break
            if not is_title:
                current_content.append(line)

        if current_content:        
            document.chapters.append(Chapter(
                title=current_title,
                content="\n".join(current_content)
        ) )
            

        return document