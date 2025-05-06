import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

import streamlit as st
import sacrebleu
from comet import load_from_checkpoint
from nltk.translate.meteor_score import meteor_score

from BruteTranslator import *
from STMTranslator import *


@st.cache_resource
def get_smt_translator():
    return STMTranslator()

@st.cache_resource
def load_comet_model():
    return load_from_checkpoint("models/comet/checkpoints/model.ckpt")

@st.cache_resource
def get_brute_translator():
    return BruteTranslator("dictionary/eng-pol.tei")

def brute_translate(sentence):
    brute_translator = get_brute_translator()
    return brute_translator.translate(sentence)

def smt_translate(sentence):
    smt_translator = get_smt_translator()
    return smt_translator.translate(sentence)

def calculate_bleu(reference, hypothesis):
    return sacrebleu.corpus_bleu([hypothesis], [[reference]])

def calculate_meteor(reference, hypotesis):
    return meteor_score([reference.split()], hypotesis.split())

def calculate_comet(reference, hypotesis, original):
    data = [{
    "src": original,
    "mt": hypotesis,
    "ref": reference
    }]
    comet_model = load_comet_model()
    prediction = comet_model.predict(data, batch_size=8, gpus=0) 
    score = prediction["system_score"]
    return score


st.title("Porównanie tłumaczenia: Brutalne vs Statystyczne")

input_text_original = st.text_area("Wprowadź tekst w języku angielskim:", "I am very hungry.")
input_text_reference = st.text_area("Wprowadź tłumaczenie referencyjne w celu wyliczenia benchmarków:", "Jestem bardzo głodny.")


if st.button("Tłumacz metodą brutalną"):
    brute_result = brute_translate(input_text_original)
    st.subheader("Tłumaczenie brutalne:")
    st.write(brute_result)
    bleu_score = calculate_bleu(input_text_reference, brute_result)
    st.write(f"BLEU Score: {bleu_score.score}")
    meteor_score = calculate_meteor(input_text_reference, brute_result)
    st.write(f"METEOR result: {meteor_score}")
    comet_score = calculate_comet(input_text_reference, brute_result, input_text_original)
    st.write(f"COMET score: {comet_score}")

if st.button("Tłumacz metodą statystyczną (SMT)"):
    smt_result = smt_translate(input_text_original)
    st.subheader("Tłumaczenie statystyczne:")
    st.write(smt_result)
    bleu_score = calculate_bleu(input_text_reference, smt_result)
    st.write(f"BLEU Score: {bleu_score.score}")
    meteor_score = calculate_meteor(input_text_reference, smt_result)
    st.write(f"METEOR result: {meteor_score}")
    comet_score = calculate_comet(input_text_reference, smt_result, input_text_original)
    st.write(f"COMET score: {comet_score}")

