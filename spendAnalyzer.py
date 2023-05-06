import os
import sys
import PyPDF4
from datetime import datetime

if len(sys.argv) < 3:
    print("Erreur : spécifiez un mot clé à rechercher et le chemin vers le dossier des fichiers PDF")
    sys.exit(1)

# Chemin d'accès au dossier contenant les fichiers PDF à rechercher
# folderPath = "/Users/regis/Documents/00-administration/64-ccp/2022"

folderPath = sys.argv[2]

# Mot-clé à rechercher dans les fichiers PDF

keyword = sys.argv[1]

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
                  pos = text.find(keyword)
                  occurences = []
                  while pos != -1:
                      occurences.append(pos)
                      pos = text.find (keyword, pos+1)  

                  if occurences:
                    for pos in occurences:  
                        item = {}
                        start = pos-8
                        end = pos + len(keyword) + 8
                        pos0 = pos + len(keyword)
                        text0 = text[start:start+5]
                        item["date"] = text0
                        item["value"] = text[pos0:end]
                        item["value"] = item["value"].replace(",",".")
                        item["keyword"] = keyword
                        items.append(item)

sorted_items = sorted (items, key=lambda x: datetime.strptime(x["date"], '%d/%m' ))

for item in sorted_items:
    print ("{}\t{}\t{}".format( item["date"], item["keyword"], item["value"]))
