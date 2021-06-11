import config
import pandas as pd
import numpy as np
from analyze import save_data


def read_sentence_tsv():
    with open(config.fp_analysis_sentences_tsv) as file:
        df = pd.read_csv(file, sep='\t')
    return df


def create_threshold(low_value, high_value, header):
    return {config.tag_threshold_low: low_value,
            config.tag_threshold_high: high_value,
            config.tag_threshold_header: header}


def tag(df):
    # Thresholds
    # In dem Array können bel. viele Thresholds mit Hilfe der Funktion 'create_threshold' hinzugefügt werden.
    # Die Thresholds bestehen aus einer unteren und oberen Grenze.
    # Außerdem muss der Header der Spalte angegeben werden (dafür config.py verwenden!)
    # Liegt ein Satz über allen oberen Grenzen, erhält dieser Satz den Tag = 1,
    # liegt dieser unter allen unteren Grenzen, erhält dieser den Tag = 0,
    # 0.5 sonst.
    thresholds = [create_threshold(1, 3, config.h_matches),
                  create_threshold(0.1, 0.2, config.h_sentence_density),
                  create_threshold(0.1, 0.2, config.h_paragraph_density)]

    h_high = 'tmp_high_header'
    h_low = 'tmp_low_header'
    df[h_high] = True
    df[h_low] = True
    for threshold in thresholds:
        df[h_high] = df[h_high] & (df[threshold[config.tag_threshold_header]] > threshold[config.tag_threshold_high])
        df[h_low] = df[h_low] & (df[threshold[config.tag_threshold_header]] < threshold[config.tag_threshold_low])
    df[config.h_tag] = np.where(df[h_high], 1, np.where(df[h_low], 0, 0.5))
    df.drop(labels=[h_high, h_low], axis=1, inplace=True)


if __name__ == '__main__':
    data = read_sentence_tsv()
    tag(data)
    save_data(data, config.fp_analysis_sentences_tagged_tsv)
