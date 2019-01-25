import treetaggerwrapper
import glob
import pickle
import os
import argparse


def lemmatize_input_files(source_dir):
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')
    files = [f for f in glob.glob(source_dir + "*.txt")]
    return {os.path.basename(f): treetaggerwrapper.make_tags(tagger.tag_file(f), exclude_nottags=True) for f in files}


def dump_data_to_files(output_dir, file_data_dict):
    for filename, tags in file_data_dict.items():
        file = open(output_dir + filename, "wb")
        pickle.dump(tags, file)
        file.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='attempt to classify the authors of some parsed texts')
    parser.add_argument('source_dir', 
                        help='the directory of text files to process')
    parser.add_argument('output_dir', 
                        help='the directory to store processed files')
    args = parser.parse_args()

    file_data_dict = lemmatize_input_files(args.source_dir)
    dump_data_to_files(args.output_dir, file_data_dict)

