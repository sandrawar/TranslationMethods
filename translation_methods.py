import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

import streamlit as st
from translate import Translator
import argostranslate.package
import argostranslate.translate
import sacrebleu
from nltk.tokenize import word_tokenize


# Funkcja do brutalnego tłumaczenia (słownikowego)
#def brute_translate(sentence):
#   translator = Translator(to_lang="pl")
#   words = word_tokenize(sentence)
#   translated = [translator.translate(w) for w in words]
#   return ' '.join(translated)

def brute_translate(sentence):
    translator = Translator(to_lang="pl")
    words = sentence.split()
    translated = [translator.translate(w) for w in words]
    return ' '.join(translated)

def smt_translate(sentence):
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next(filter(lambda x: x.code == "en", installed_languages))
    to_lang = next(filter(lambda x: x.code == "pl", installed_languages))
    translation = from_lang.get_translation(to_lang)
    return translation.translate(sentence)

def calculate_bleu(reference, hypothesis):
    return sacrebleu.corpus_bleu([hypothesis], [reference])

st.title("Porównanie tłumaczenia: Brutalne vs Statystyczne")

input_text = st.text_area("Wprowadź tekst w języku angielskim", "I am very hungry")

if st.button("Tłumacz metodą brutalną"):
    brute_result = brute_translate(input_text)
    st.subheader("Tłumaczenie brutalne:")
    st.write(brute_result)
    bleu_score = calculate_bleu(["Jestem bardzo głodny."], brute_result)
    st.write(f"BLEU Score: {bleu_score.score}")

if st.button("Tłumacz metodą statystyczną (SMT)"):
    smt_result = smt_translate(input_text)
    st.subheader("Tłumaczenie statystyczne:")
    st.write(smt_result)
    bleu_score = calculate_bleu(["Jestem bardzo głodny."], smt_result)
    st.write(f"BLEU Score: {bleu_score.score}")

