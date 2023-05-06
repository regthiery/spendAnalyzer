import os
import sys
import PyPDF4
from datetime import datetime

if len(sys.argv) < 4:
    print("Erreur : spécifiez un mot clé à rechercher et le chemin vers le dossier des fichiers PDF")
    sys.exit(1)


folderPath = sys.argv[3]

# Mot-clé à rechercher dans les fichiers PDF

keywordToSearch = sys.argv[1]

keywordToWrite = sys.argv[2]

# Parcours de tous les fichiers du dossier

items = []
for filename in os.listdir(folderPath):
    if filename.endswith('.pdf'):
        # Ouverture du fichier PDF
        
        with open(os.path.join(folderPath, filename), 'rb') as pdf_file:
        
            # Lecture du contenu du fichier PDF
            pdf_reader = PyPDF4.PdfFileReader(pdf_file)
        
            for page in range(pdf_reader.getNumPages()):
                page_obj = pdf_reader.getPage(page)
                text0 = page_obj.extractText()
                text = text0.replace("\n", "")

                for line in text.splitlines():
                  pos = text.find(keywordToSearch)
                  occurences = []
                  while pos != -1:
                      occurences.append(pos)
                      pos = text.find (keywordToSearch, pos+1)  

                  if occurences:
                    for pos in occurences:  
                        item = {}
                        start = pos-8
                        end = pos + len(keywordToSearch) + 8
                        pos0 = pos + len(keywordToSearch)
                        text0 = text[start:start+5]
                        item["date"] = text0
                        item["value"] = text[pos0:end]
                        item["value"] = item["value"].replace(",",".")
                        item["keyword"] = keywordToWrite
                        items.append(item)

sorted_items = sorted (items, key=lambda x: datetime.strptime(x["date"], '%d/%m' ))

for item in sorted_items:
    print ("{}\t{}\t{}".format( item["date"], item["keyword"], item["value"]))
