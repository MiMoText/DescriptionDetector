import os
import pandas as pd
import matplotlib.pyplot as plt
import config


def load_data():
    dataframes = {}
    for filename in os.listdir(config.fp_processed_dir):
        if filename.endswith('tsv'):
            dataframe = pd.read_csv(os.path.join(config.fp_processed_dir, filename), sep='\t')
            dataframe.insert(0, config.h_filename, filename.replace('.tsv', ''))
            dataframes[filename.replace('.tsv', '')] = dataframe
    df = concat_dataframes(dataframes)
    df_no_zeros = df[df[config.h_sentence_density] != 0]
    return df, df_no_zeros, dataframes


def save_data(data, filepath=None, dir=None):
    if type(data) == dict:
        for key in data.keys():
            if dir is None:
                save_data(data[key], key + '.tsv')
            else:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                save_data(data[key], os.path.join(dir, key + '.tsv'))
    else:
        data.to_csv(filepath, sep='\t', index=False)


def concat_dataframes(data_dict):
    keys = []
    for key in data_dict.keys():
        keys.append(key)
    keys.sort()
    dfs = []
    for key in keys:
        dfs.append(data_dict[key])
    return pd.concat(dfs, axis=0, ignore_index=True)


def create_plot(header, data, filepath=None, dir=None):
    if type(data) == dict:
        for key in data.keys():
            if dir is None:
                create_plot(header, data[key], key + '.png')
            else:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                create_plot(header, data[key], os.path.join(dir, key + '.png'))
    else:
        plt.plot(data[header])
        plt.savefig(filepath)
        plt.close()


def create_boxplot(header, data, filepath=None, dir=None):
    if type(data) == dict:
        for key in data.keys():
            if dir is None:
                create_boxplot(header, data[key], key + '.png')
            else:
                if not os.path.exists(dir):
                    os.makedirs(dir)
                create_plot(header, data[key], os.path.join(dir, key + '.png'))
    else:
        plt.boxplot(data[header])
        plt.savefig(filepath)
        plt.close()


def density_range(dens_range, data, restrict_same_paragraph=False):
    if dens_range % 2 == 0:
        print('Not able to compute the density for range=' + str(dens_range) + '. Only possible for odd ranges.')
    else:
        words_count = data[config.h_words]
        matches_count = data[config.h_matches]
        words = []
        matches = []
        words_sum = 0
        matches_sum = 0
        density = []
        compute_density = False
        for i in range(len(words_count)):
            if restrict_same_paragraph and i > 0 and data[config.h_paragraph_nr][i] != data[config.h_paragraph_nr][i - 1]:
                while len(density) < i:
                    if len(words) > i - len(density) + int(dens_range / 2):
                        words_sum -= words[0]
                        words = words[1:]
                        matches_sum -= matches[0]
                        matches = matches[1:]
                    if words_sum == 0:
                        density.append(0)
                    else:
                        density.append(matches_sum / words_sum)
                words = []
                matches = []
                words_sum = 0
                matches_sum = 0
                compute_density = False
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
                if words_sum == 0:
                    density.append(0)
                else:
                    density.append(matches_sum / words_sum)
        while len(density) < len(data[config.h_words]):
            words_sum -= words[0]
            words = words[1:]
            matches_sum -= matches[0]
            matches = matches[1:]
            if words_sum == 0:
                density.append(0)
            else:
                density.append(matches_sum / words_sum)
        header = config.h_density_range(dens_range, restrict_same_paragraph)
        data[header] = pd.Series(density)


def density_paragraph(data):
    paragraphs = data[config.h_paragraph_nr]
    paragraph_start = 0
    words_count = data[config.h_words]
    matches_count = data[config.h_matches]
    words_sum = words_count[0]
    matches_sum = matches_count[0]
    paragraph_density = []
    for i in range(1, len(paragraphs)):
        if paragraphs[i] != paragraphs[i - 1]:
            for p_index in range(paragraph_start, i):
                if words_sum == 0:
                    paragraph_density.append(0)
                else:
                    paragraph_density.append(matches_sum / words_sum)
            words_sum = words_count[i]
            matches_sum = matches_count[i]
            paragraph_start = i
        else:
            words_sum += words_count[i]
            matches_sum += matches_count[i]
    while len(paragraph_density) < len(paragraphs):
        if words_sum == 0:
            paragraph_density.append(0)
        else:
            paragraph_density.append(matches_sum / words_sum)
    data[config.h_paragraph_density] = pd.Series(paragraph_density)


def median_density_per_paragraph(data, skip_one_sentence_paragraphs=False):
    paragraphs = data[config.h_paragraph_nr]
    paragraph_start = 0
    sentence_density = data[config.h_sentence_density]
    sentence_densities = [sentence_density[0]]
    paragraph_median = []
    paragraph_std = []
    medians = []
    for i in range(1, len(paragraphs)):
        if paragraphs[i] != paragraphs[i - 1]:
            if skip_one_sentence_paragraphs and i - paragraph_start < 2:
                median = 0
                std = 0
            else:
                median = pd.Series(sentence_densities).median()
                medians.append(median)
                std = pd.Series(sentence_densities).std()
            for p_index in range(paragraph_start, i):
                paragraph_median.append(median)
                paragraph_std.append(std)
            sentence_densities = []
            paragraph_start = i
        sentence_densities.append(sentence_density[i])
    if skip_one_sentence_paragraphs and len(paragraphs) - paragraph_start < 2:
        median = 0
        std = 0
    else:
        median = pd.Series(sentence_densities).median()
        medians.append(median)
        std = pd.Series(sentence_densities).std()
    while len(paragraph_median) < len(paragraphs):
        paragraph_median.append(median)
        paragraph_std.append(std)
    data[config.h_paragraph_median(skip_one_sentence_paragraphs)] = pd.Series(paragraph_median)
    data[config.h_paragraph_std(skip_one_sentence_paragraphs)] = pd.Series(paragraph_std).fillna(0)
    return pd.Series(medians).median()


def paragraph_dataframe(data):
    paragraphs_nr = data[config.h_paragraph_nr]
    if config.h_paragraph_median(False) not in data.columns:
        median_density_per_paragraph(data)
    filenames = []
    paragraphs = []
    sentences = []
    words = []
    matches = []
    densities = []
    medians = []
    stds = []
    for i in range(paragraphs_nr[len(paragraphs_nr)-1] + 1):
        filenames.append(data[config.h_filename][0])
        paragraphs.append(i)
        sentences.append(max(data[config.h_sentence_nr_paragraph][data[config.h_paragraph_nr] == i]) + 1)
        w = sum(data[config.h_words][data[config.h_paragraph_nr] == i])
        words.append(w)
        m = sum(data[config.h_matches][data[config.h_paragraph_nr] == i])
        matches.append(m)
        densities.append(m / w)
        medians.append(max(data[config.h_paragraph_median(False)][data[config.h_paragraph_nr] == i]))
        stds.append(max(data[config.h_paragraph_std(False)][data[config.h_paragraph_nr] == i]))
    df = pd.DataFrame()
    df[config.h_filename] = filenames
    df[config.h_paragraph_nr] = paragraphs
    df[config.h_sentences] = sentences
    df[config.h_words] = words
    df[config.h_matches] = matches
    df[config.h_paragraph_density] = densities
    df[config.h_paragraph_median(False)] = medians
    df[config.h_paragraph_std(False)] = stds
    return df


if __name__ == '__main__':
    df, df_no_zeros, dataframes = load_data()

    paragraphs_dfs = {}
    for key in dataframes.keys():
        dataframe = dataframes[key]
        density_range(3, dataframe, restrict_same_paragraph=True)
        density_range(3, dataframe, restrict_same_paragraph=False)
        density_paragraph(dataframe)
        paragraphs_dfs[key] = paragraph_dataframe(dataframe)

    save_data(dataframes, dir=config.fp_analysis_files_dir)
    save_data(paragraphs_dfs, dir=config.fp_analysis_paragraphs_dir)

    df_all_sentences = concat_dataframes(dataframes)
    df_all_paragraphs = concat_dataframes(paragraphs_dfs)
    save_data(df_all_sentences, filepath=config.fp_analysis_sentences_tsv)
    save_data(df_all_paragraphs, filepath=config.fp_analysis_paragraphs_tsv)

    create_boxplot(config.h_paragraph_median(False), df_all_paragraphs,
                os.path.join(config.fp_analysis_dir, 'paragraphs_median_boxplot.png'))
    create_plot(config.h_paragraph_median(False), df_all_paragraphs,
                   os.path.join(config.fp_analysis_dir, 'paragraphs_median_plot.png'))
    create_boxplot(config.h_paragraph_density, df_all_paragraphs,
                os.path.join(config.fp_analysis_dir, 'paragraphs_density_boxplot.png'))
    create_plot(config.h_paragraph_density, df_all_paragraphs,
                   os.path.join(config.fp_analysis_dir, 'paragraphs_density_plot.png'))

    # Auswahl bestimmter Datei
    example_file = 'Abbes_Voyage'
    df_example = dataframes[example_file]
    p_df_example = paragraphs_dfs[example_file]

    # Erstellen und Speichern von Boxplots und Plots
    create_boxplot(config.h_density_range(3, True), df_example,
                   os.path.join('examples', example_file + '_densityRange3SameParagraph_boxplot.png'))
    create_plot(config.h_density_range(3, True), df_example,
                os.path.join('examples', example_file + '_densityRange3SameParagraph_plot.png'))

    create_boxplot(config.h_paragraph_median(False), p_df_example,
                   os.path.join('examples', example_file + '_paragraph_medianDensity_boxplot.png'))
    create_plot(config.h_paragraph_median(False), p_df_example,
                   os.path.join('examples', example_file + '_paragraph_medianDensity_plot.png'))

    # Abspeichern der Dataframes
    save_data(df_example, os.path.join('examples', example_file + '_df.tsv'))
    save_data(p_df_example, os.path.join('examples', example_file + '_paragraphs_df.tsv'))