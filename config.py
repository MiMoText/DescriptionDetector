import os
# Konfigurations-Datei

# Header
# processed-Header (bei Änderung muss entweder process.py neu ausgeführt oder die Header in den processed-Files angepasst werden)
h_sentence_nr = 'sentence nr'
h_sentence = 'sentence'
h_paragraph_nr = 'paragraph nr'
h_sentence_nr_paragraph = 'sentence nr in paragraph'
h_words = 'words'
h_matches = 'matches'
h_sentence_density = 'sentence density'
h_voc_matches = 'vocabulary words matched'

h_filename = 'filename'
h_sentences = 'sentences'
h_paragraph_density = 'paragraph density'

h_tag = 'Figurenbeschreibung'


def h_density_range(range, same_paragraph):
    return 'density (range=' + str(range) + ',same_paragraph=' + str(same_paragraph) + ')'


def h_paragraph_median(skip_one_sentence_paragraphs):
    if skip_one_sentence_paragraphs:
        return 'paragraph density median (skipped_one_sentece_paragraphs=True)'
    return 'paragraph density median'


def h_paragraph_std(skip_one_sentence_paragraphs):
    if skip_one_sentence_paragraphs:
        return 'paragraph density std (skipped_one_sentece_paragraphs=True)'
    return 'paragraph density std'


# Dateien
fp_vocab_csv = os.path.join('data', 'vocab', 'vocabulaire 18B.csv')
fp_vocab_txt = os.path.join('data', 'vocab', 'vocabulaire.txt')
fp_plain_dir = os.path.join('data', 'plain', 'files')
fp_processed_dir = os.path.join('data', 'processed', 'files')
fp_analysis_dir = os.path.join('data', 'analysis')
fp_analysis_files_dir = os.path.join(fp_analysis_dir, 'files')
fp_analysis_paragraphs_dir = os.path.join(fp_analysis_dir, 'paragraphs')
fp_analysis_sentences_tsv = os.path.join(fp_analysis_dir, 'sentences.tsv')
fp_analysis_paragraphs_tsv = os.path.join(fp_analysis_dir, 'paragraphs.tsv')
fp_analysis_sentences_tagged_tsv = os.path.join(fp_analysis_dir, 'sentences_tagged.tsv')


# Sonstige Konstanten
tag_threshold_low = 'th_low'
tag_threshold_high = 'th_high'
tag_threshold_header = 'th_header'
