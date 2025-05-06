import xml.etree.ElementTree as ET
from translate import Translator
import random
import re


class BruteTranslator:
    def __init__(self, dictionary_path):
        NS = {
            'tei': 'http://www.tei-c.org/ns/1.0',
            'xml': 'http://www.w3.org/XML/1998/namespace'
        }
        self.dictionary = {}
        tree = ET.parse(dictionary_path)
        root = tree.getroot()

        for entry in root.findall(".//tei:entry", NS):
            orth = entry.find("tei:form/tei:orth", NS)
            if orth is not None:
                for cit in entry.findall(".//tei:cit[@type='trans'][@xml:lang='pl']", NS):
                    for quote in cit.findall("tei:quote", NS):
                        if quote.text:
                            if orth.text.lower() in self.dictionary:
                                self.dictionary[orth.text.lower()].append(quote.text.strip())
                            else:
                                self.dictionary[orth.text.lower()] = [quote.text.strip()]
        
        self.translator = Translator(to_lang="pl")

    def translate(self, sentence):
        tokens = re.findall(r"\b\w+(?:'\w+)?\b|[^\w\s]", sentence)
    
        result = []
        for token in tokens:
            translated = token
            if re.match(r'\w', token):
                if token.lower() in self.dictionary:
                    translated = (random.choice(self.dictionary[token.lower()]))
                else:
                    translated = self.translator.translate(token.lower())
                    self.dictionary[token.lower()] = [translated]
                
                if token.isupper():
                    translated = translated.capitalize()
            result.append(translated)
 
        result_sentence = ''
        for i in range(len(result)):
            result_sentence += result[i]
            if i + 1 < len(result) and re.match(r'\w', result[i]) and re.match(r'\w', result[i+1]):
                result_sentence += ' '
            elif i + 1 < len(result) and re.match(r'\w', result[i]) and re.match(r'[^\w\s]', result[i+1]):
                continue
            elif i + 1 < len(result) and re.match(r'[^\w\s]', result[i]) and re.match(r'\w', result[i+1]):
                result_sentence += ' '

        return result_sentence