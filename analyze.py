import os
import pandas as pd
import matplotlib.pyplot as plt

header_words = 'words without punctuation'
header_matches = 'vocabulary matches'
header_sentence_perc = 'vocabulary matches percentage'

example_file = 'Boufflers_Reine'


def create_plot(header, data, filepath=None, dir=None):
    if type(data) == dict:
        for key in data.keys():
            if dir is None:
                create_plot(header, data[key], key)
            else:
                create_plot(header, data[key], os.path.join(dir, key))
    else:
        plt.plot(data[header])
        plt.savefig(filepath)


def create_boxplot(header, data, filepath=None, dir=None):
    if type(data) == dict:
        for key in data.keys():
            if dir is None:
                create_boxplot(header, data[key], key)
            else:
                create_boxplot(header, data[key], os.path.join(dir, key))
    else:
        plt.boxplot(data[header])
        plt.savefig(filepath)


def density_range(dens_range, data, restrict_same_paragraph=False):
    # TODO restrict_same_paragraph (aktuell noch nicht implementiert)
    if dens_range % 2 == 0:
        header = ['density (range=' + str(dens_range) + ',same_paragraph=' + str(restrict_same_paragraph) + ')-',
                  'density (range=' + str(dens_range) + ',same_paragraph=' + str(restrict_same_paragraph) + ')+']
        words_count = data[header_words]
        matches_count = data[header_matches]
        words = []
        matches = []
        words_sum = 0
        matches_sum = 0
        density = []
        compute_density = False
        for i in range(len(words_count)):
            w = words_count[i]
            m = matches_count[i]
            words.append(w)
            matches.append(m)
            words_sum += w
            matches_sum += m
            if len(words) * 2 >= dens_range:
                compute_density = True
            if len(words) > dens_range:
                words_sum -= words[0]
                words = words[1:]
                matches_sum -= matches[0]
                matches = matches[1:]
            if compute_density:
                density.append(matches_sum / words_sum)
        while len(words) > 0:
            words_sum -= words[0]
            words = words[1:]
            matches_sum -= matches[0]
            matches = matches[1:]
            density.append(matches_sum / words_sum)
        data[header[0]] = pd.Series(density[:-1])
        data[header[1]] = pd.Series(density[1:])
    else:
        header = 'density (range=' + str(dens_range) + ',same_paragraph=' + str(restrict_same_paragraph) + ')'
        words_count = data[header_words]
        matches_count = data[header_matches]
        words = []
        matches = []
        words_sum = 0
        matches_sum = 0
        density = []
        compute_density = False
        for i in range(len(words_count)):
            w = words_count[i]
            m = matches_count[i]
            words.append(w)
            matches.append(m)
            words_sum += w
            matches_sum += m
            if len(words) * 2 > dens_range:
                compute_density = True
            if len(words) > dens_range:
                words_sum -= words[0]
                words = words[1:]
                matches_sum -= matches[0]
                matches = matches[1:]
            if compute_density:
                density.append(matches_sum / words_sum)
        while len(words) > 0:
            words_sum -= words[0]
            words = words[1:]
            matches_sum -= matches[0]
            matches = matches[1:]
            density.append(matches_sum / words_sum)
        data[header] = pd.Series(density)


def load_data():
    files_dir = os.path.join('data', 'results', 'files')
    dataframes = {}
    dfs = []
    for filename in os.listdir(files_dir):
        if filename.endswith('tsv'):
            dataframe = pd.read_csv(os.path.join(files_dir, filename), sep='\t')
            dfs.append(dataframe)
            dataframes[filename.replace('.tsv', '')] = dataframe
    df = pd.concat(dfs, axis=0, ignore_index=True)
    df_no_zeros = df[df['vocabulary matches percentage'] != 0]
    return df, df_no_zeros, dataframes


if __name__ == '__main__':
    df, df_no_zeros, dataframes = load_data()
    df_example = dataframes[example_file]
    density_range(9, df_example)
    create_plot('density (range=9,same_paragraph=False)', df_example, 'plot.png')
    print(df_example)