import argparse
import pickle
import glob
import os
import re
from collections import Counter
from itertools import groupby
import matplotlib.pyplot as plt


bestiaire = ["abeille", "aigle", "âne", "animal", "araignée", "boeuf", 
             "canard", "cerf", "chat", "cheval", "chèvre", "chien", 
             "chouette", "cochon", "coq", "cygne", "dragon", "écureuil",
             "éléphant", "fourmi", "gibier", "insecte", "lapin", "lièvre",
             "loup", "moineau", "mouche", "mouton", "oie", "oiseau", "ours", 
             "papillon", "perroquet", "pigeon", "poisson", "poule", "poulet",
             "rat", "renard", "rossignol", "serpent", "singe", "souris", 
             "tigre", "truite", "vache", "veau"]


def load_preprocessed_data(source_dir):
    print('loading data...', end='')
    file_paths = [f for f in glob.glob(source_dir + "*.txt")]
    input_data_dict = {}
    for path in file_paths:
        file = open(path , "rb")
        input_data_dict[os.path.basename(path)] = pickle.load(file)
        file.close()
        print('.', end='')
    print('done loading data.')
    return input_data_dict


def get_author_name_from_path_regex(file_path):
    return re.search('(?<=-)(.+)(?=-)', file_path).group()


def compute_bestiaire_counts(book_data_dict):
    book_bestiaire_count_dict = {}
    for book_file_path, tag_sequence in book_data_dict.items():
        sorted_tags = sorted(tag_sequence, key=lambda tag: tag.lemma)
        counts = [(i, len(list(c))) for i, c  in groupby(sorted_tags, key=lambda tag: tag.lemma)]
        bestiaire_counts = {i: c for i, c in counts if i in bestiaire}
        book_bestiaire_count_dict[book_file_path] = bestiaire_counts
        print(book_file_path + ' bestiaire count complete')
    return book_bestiaire_count_dict


def merge_author_counts(book_bestiaire_count_dict):
    author_bestiaire_count_dict = {get_author_name_from_path_regex(key): {}
                                   for key in book_bestiaire_count_dict.keys()}
    for book_path, count_dict in book_bestiaire_count_dict.items():
        author = get_author_name_from_path_regex(book_path)
        author_bestiaire_count_dict[author] = Counter(author_bestiaire_count_dict[author]) + Counter(count_dict)
    return author_bestiaire_count_dict



def bar_plot(names, values):
    plt.bar(range(len(values)),values,tick_label=list(names))
    plt.xticks(rotation=90)
    plt.savefig('bar.png')
    plt.show()


if __name__ == "__main__":

    plot_choices = ['choice']
    parser = argparse.ArgumentParser(description='generate specified plot from supplied data')
    parser.add_argument('source_dir', help='input data directory')
    parser.add_argument('--plot', choices=plot_choices, default='choice',
                        help='the plot you wish to create')
    args = parser.parse_args()
    
    book_data_dict = load_preprocessed_data(args.source_dir)
    book_bestiaire_count_dict = compute_bestiaire_counts(book_data_dict)
    author_bestiaire_count_dict = merge_author_counts(book_bestiaire_count_dict)
    bar_plot(author_bestiaire_count_dict['Colette'].keys(), author_bestiaire_count_dict['Colette'].values())
