import os
import csv


def create_vocab_file():
    data_folder = os.path.join('', 'data')
    with open(os.path.join(data_folder, 'vocabulaire 18B.csv')) as f:
        reader = csv.reader(f, delimiter=';')
        header_lines = 2
        with open(os.path.join(data_folder, 'vocabulaire.txt'), 'w') as out_file:
            for row in reader:
                if header_lines > 0:
                    header_lines -= 1
                    continue
                for word in row:
                    if word != "":
                        if '(' in word:
                            index = word.index('(')
                            word = word[:index]
                        out_file.write(word.strip())
                        out_file.write('\n')


if __name__ == '__main__':
    create_vocab_file()