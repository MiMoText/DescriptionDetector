"""
Skript, um die Datei mit den Gesamtergebnissen ("sentences.tsv") zu filtern. 
Durch eine Kombination von Kriterien soll eine Liste von Sätzen gefunden werden, 
die möglichst weitgehend nur true positives, also tatsächliche physische Portraits, sind. 
"""


import pandas as pd
from os.path import join


def read_tsv(datafilepath): 
	with open(datafilepath, "r", encoding="utf8") as datafile: 
		data = pd.read_csv(datafile, sep="\t")
	print(data.head())
	print(data.shape)
	return data

def filter_data(data):
	# Filterschritt: Hier können die Parameter geändert und ergänzt werden.
	filtered = data[(data.matches > 2) & (data.sentence_density > 0.2) & (data.paragraph_density > 0.03)]
	filtered.sort_values(by="sentence_density", ascending=False, inplace=True)
	print(filtered.head())
	print(filtered.shape)
	return filtered


def write_tsv(filtered):
	filtered = filtered.loc[:,["filename", "sentence_nr", "sentence", "matches", "sentence_density", "paragraph_density"]]
	with open("filtered_results.tsv", "w", encoding="utf8") as outfile: 
		filtered.to_csv(outfile, sep="\t")


def main():
	datafilepath = join("data", "analysis", "sentences.tsv")
	data = read_tsv(datafilepath)
	filtered = filter_data(data)
	write_tsv(filtered)

main()

