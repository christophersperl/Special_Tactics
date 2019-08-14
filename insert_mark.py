# Arbeiten mit html als Basis
# 
# 06.08.2019 SC V 1.0.0
###

import re
import os
import spacy
from bs4 import BeautifulSoup, Tag

html_file_path = 'Beispielkunde.html'

# Das html welches mit pdf2htmlEx aus einem pdf erstellt wurde laden.
html_doc = open(html_file_path, 'r', encoding = 'utf-8').read()
soup = BeautifulSoup(html_doc, 'html.parser')
html_doc = soup.prettify()
print(html_doc[:15])

# Den Textinhalt des html extrahieren.
text_from_html_document = u''
for x in soup.findAll('body'): 
       text_from_html_document += x.text

# Importieren der Mustererkennung.
from spacy.matcher import Matcher

# Das Sprachmodell in das NLP Objekt laden.
nlp = spacy.load('en_core_web_md')

# Die Mustererkennung initialisieren.
matcher = Matcher(nlp.vocab)

# Die zu suchenden Muster hinzufügen.

pattern = [{'LIKE_NUM': True}]
matcher.add('SimpleNumeric_PATTERN', None, pattern)

# Dokument Verarbeiten.
doc = nlp(text_from_html_document)

# Das Dokument auf treffer untersuchen.
matches = matcher(doc) 


# Erstellen eines Index über den Body der HTML    
matches_container = []
html_body_index = {}
html_body = '' 
html_body += str(soup.body)

switcher = False
i = 0

for character in range(len(html_body)):
    if html_body[character] == '>':
        switcher = True
        html_body_index['X'+str(character)] = html_body[character]
        continue
    if html_body[character] == '<':
        switcher = False
        html_body_index['X'+str(character)] = html_body[character]
        continue

    if switcher:
        html_body_index[i] = html_body[character]
        i += 1
    else:
        html_body_index['X'+str(character)] = html_body[character]







# Ausgabe der Treffer pro Dokument.
for match_id, start, end in matches:
    matched_span = doc[start:end]
    beginning = matched_span.start_char
    ending = matched_span.end_char
    matches_container.append((matched_span.start_char, matched_span.end_char))

    html_body_index[beginning] = '<mark>'+ html_body_index[beginning]
    html_body_index[ending] = html_body_index[ending] + '</mark>'

new_body = ''
for x  in html_body_index:
    new_body += html_body_index[x]


out = re.sub(r'<body>[\s\S]*</body>',str(new_body),str(soup))

with open('Beispiel_out.html', 'w', encoding='utf-8') as file:
    file.write(str(out))
    file.close()
