#       efficiency: $ python -m spacy download fr_core_news_sm
# OR    accuracy:   $ python -m spacy download fr_dep_news_trf

import spacy
import os
import re
import string
import csv


def split_sentences_and_lemmatize_text(text):
    nlp = spacy.load("fr_core_news_sm")

    punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation))

    doc = nlp(text)
    processed_sentences = []
    sentences = []
    for sent in doc.sents:
        sentence = sent.text.strip()
        sentences.append(sentence)
        sent_doc = nlp(sentence)
        processed_sentence = [token.lemma_.lower() for token in sent_doc]
        for word in processed_sentence:
            if punctuation_regex.sub('', word) == '':
                processed_sentence.remove(word)
        processed_sentences.append(processed_sentence)
    return sentences, processed_sentences


def read_vocab():
    filepath = os.path.join('data', 'vocabulaire.txt')
    with open(filepath) as f:
        vocab = f.read().split('\n')
    vocab = list(set(vocab))
    vocab.remove('')
    return vocab


def read_lemmatized_vocab():
    vocab = read_vocab()
    nlp = spacy.load("fr_core_news_sm")
    lemmatized_vocab = []
    for v in vocab:
        doc = nlp(v)
        lemmatized = [token.lemma_.lower() for token in doc]
        if not lemmatized in lemmatized_vocab:
            lemmatized_vocab.append(lemmatized)
    return lemmatized_vocab


def count_vocab_words_in_text(vocab, sentence):
    count = 0
    found_vocabs = []
    for w_index in range(len(sentence)):
        for vocab_sequence in vocab:
            if w_index + len(vocab_sequence) < len(sentence):
                index = w_index
                match = True
                for vocab_word in vocab_sequence:
                    if vocab_word != sentence[index]:
                        match = False
                        break
                    index += 1
                if match:
                    found_vocabs.append(vocab_sequence)
                    count += 1
    return count, found_vocabs


def compute_density(vocab, text):
    results = []
    results_header = ['sentence nr', 'sentence', 'paragraph nr', 'sentence nr in paragraph', 'words',
                      'vocabulary matches', 'vocabulary matches percentage', 'vocabulary words found']
    paragraphs = text.split('\n')
    total_sentence_count = 0
    for p_index in range(len(paragraphs)):
        print('\r', (p_index+1), '/', len(paragraphs), end='')
        paragraph = paragraphs[p_index].strip()
        sentences, processed_sentences = split_sentences_and_lemmatize_text(paragraph)
        if len(sentences) != len(processed_sentences):
            print('ERROR: sentence-len')
        for s_index in range(len(sentences)):
            sentence = sentences[s_index]
            processed_sentence = processed_sentences[s_index]

            sentence_result = {}
            sentence_result['sentence nr'] = total_sentence_count
            sentence_result['sentence'] = sentence
            sentence_result['paragraph nr'] = p_index
            sentence_result['sentence nr in paragraph'] = s_index
            sentence_result['words'] = len(processed_sentence)

            matches, found_vocabs = count_vocab_words_in_text(vocab, processed_sentence)
            sentence_result['vocabulary matches'] = matches
            if len(processed_sentence) == 0:
                sentence_result['vocabulary matches percentage'] = 0
            else:
                sentence_result['vocabulary matches percentage'] = matches / len(processed_sentence)
            sentence_result['vocabulary words found'] = found_vocabs

            results.append(sentence_result)
            total_sentence_count += 1
    return results_header, results


if __name__ == '__main__':
    RE_ANALYZE = True

    vocab = read_lemmatized_vocab()

    text_dir = os.path.join('data', 'plain', 'files')
    results_dir = os.path.join('data', 'results', 'files')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    for filename in os.listdir(text_dir):
        if filename.endswith('.txt'):
            results_filename = os.path.join(results_dir, filename.replace('.txt', '.tsv'))
            if not RE_ANALYZE and os.path.exists(results_filename):
                continue
            print('\n' + filename)
            with open(os.path.join(text_dir, filename)) as file:
                text = file.read()
            results_header, results = compute_density(vocab, text)
            with open(results_filename, 'w') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(results_header)
                for result in results:
                    row = []
                    for header in results_header:
                        row.append(result[header])
                    writer.writerow(row)