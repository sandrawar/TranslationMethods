#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Variables
CORPUS_DIR="./corpus"  # Directory containing source and target files
MODEL_DIR="./model"    # Directory to save the SMT model
LM_FILE="/home/sandra/model/language_model.blm"  # Path to the trained language model
SOURCE_LANG="en"       # Source language code
TARGET_LANG="pl"       # Target language code

MOSES_DIR="/mnt/c/src/github/sandrawar/TranslationMethods/moses-smtnlp/mosesdecoder"  # Corrected Moses path
KENLM_BIN="/home/sandra/kenlm/build/bin"  # Corrected KenLM path

# Create directories
mkdir -p $MODEL_DIR

# Step 1: Preprocessing
echo "Step 1: Tokenizing the corpus..."
perl $MOSES_DIR/scripts/tokenizer/tokenizer.perl -l $SOURCE_LANG < $CORPUS_DIR/train.$SOURCE_LANG > $CORPUS_DIR/train.tok.$SOURCE_LANG
perl $MOSES_DIR/scripts/tokenizer/tokenizer.perl -l $TARGET_LANG < $CORPUS_DIR/train.$TARGET_LANG > $CORPUS_DIR/train.tok.$TARGET_LANG

echo "Step 2: Truecasing the corpus..."
perl $MOSES_DIR/scripts/recaser/train-truecaser.perl --model $CORPUS_DIR/truecase-model.$SOURCE_LANG --corpus $CORPUS_DIR/train.tok.$SOURCE_LANG
perl $MOSES_DIR/scripts/recaser/train-truecaser.perl --model $CORPUS_DIR/truecase-model.$TARGET_LANG --corpus $CORPUS_DIR/train.tok.$TARGET_LANG

perl $MOSES_DIR/scripts/recaser/truecase.perl --model $CORPUS_DIR/truecase-model.$SOURCE_LANG < $CORPUS_DIR/train.tok.$SOURCE_LANG > $CORPUS_DIR/train.true.$SOURCE_LANG
perl $MOSES_DIR/scripts/recaser/truecase.perl --model $CORPUS_DIR/truecase-model.$TARGET_LANG < $CORPUS_DIR/train.tok.$TARGET_LANG > $CORPUS_DIR/train.true.$TARGET_LANG

echo "Step 3: Cleaning the corpus..."
perl $MOSES_DIR/scripts/training/clean-corpus-n.perl $CORPUS_DIR/train.true $SOURCE_LANG $TARGET_LANG $CORPUS_DIR/cleaned_corpus 1 80

# Step 4: Training the Language Model
echo "Step 4: Training the target language model..."
$KENLM_BIN/lmplz -o 3 < $CORPUS_DIR/train.true.$TARGET_LANG > $LM_FILE

echo "Step 5: Training the SMT model..."
perl $MOSES_DIR/scripts/training/train-model.perl \
    --root-dir $MODEL_DIR \
    --corpus $CORPUS_DIR/cleaned_corpus \
    --f $SOURCE_LANG --e $TARGET_LANG \
    --alignment grow-diag-final-and \
    --reordering msd-bidirectional-fe \
    --lm 0:3:$LM_FILE \
    --external-bin-dir ~/mosesdecoder/tools

echo "Training complete! Model saved in $MODEL_DIR."
