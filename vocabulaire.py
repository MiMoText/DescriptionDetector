import csv
import config


def create_vocab_file():
    words_to_delete = ['c..', 'un']

    words = []
    with open(config.fp_vocab_csv) as f:
        reader = csv.reader(f, delimiter=';')
        header_lines = 2
        for row in reader:
            if header_lines > 0:
                header_lines -= 1
                continue
            for word in row:
                if word != "":
                    if '(' in word:
                        index = word.index('(')
                        word = word[:index].strip()
                        words.append(word)
    words = list(set(words))
    words.sort()
    for w in words_to_delete:
        words.remove(w)
    with open(config.fp_vocab_txt, 'w') as out_f:
        for word in words:
            out_f.write(word)
            out_f.write('\n')


if __name__ == '__main__':
    create_vocab_file()