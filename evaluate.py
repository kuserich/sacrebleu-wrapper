import sys
import os
import argparse
import sacrebleu
from mosestokenizer import *

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def de_preprocess(references, language):
    clean_references = []
    for item in references:
        item = item.replace("@@ ", "")
        item = item.replace("@@@", "")
        item = item.replace("@@@@", "")
        item = item.replace("<eos>", "")
        item = item.replace("@str", "")

        item = item.replace("\n", "")
        with MosesDetokenizer(language) as detokenize:
            item_clean = detokenize(item.split(" "))
            clean_references.append(item_clean)
    return clean_references

def get_source_references(source_file_path, preprocessed=False, language=''):
    if preprocessed and not language:
        print("[Error] Please provide a language for de-preprocessing")
        sys.exit()

    source_file_handler = open(source_file_path, 'r')
    source_references = source_file_handler.readlines()

    if preprocessed:
        return de_preprocess(source_references, language)

    return source_references


parser = argparse.ArgumentParser(description="Compute BLEU score")
parser.add_argument("--src", type=str, help="location of the source translation (i.e. output of your model")
parser.add_argument("--trg", type=str, help="location of the target translation")
parser.add_argument("--language", type=str, nargs="?", help="Language of the source translation (needed for de-preprocessing)")
parser.add_argument("--preprocessed", type=str2bool, nargs="?", const=True, default=False, help="Revert pre-processing")
parser.add_argument("--save", type=str2bool, nargs="?", const=True, default=True, help="Store a file with the results")

args = parser.parse_args()

target_file_handler = open(args.trg, 'r')
target_references = target_file_handler.readlines()
source_file_path = args.src

files_to_process = []

if os.path.isdir(source_file_path):
    files_to_process = [os.path.join(source_file_path, file) for file in os.listdir(source_file_path) if os.path.isfile(os.path.join(source_file_path, file))]
else:
    files_to_process = [args.src]

for file in files_to_process:
    source_references = get_source_references(file, preprocessed=args.preprocessed, language=args.language)
    try:
        bleu = str(sacrebleu.corpus_bleu(source_references, [target_references]))
        print(file, bleu)

        if args.save:
            f = open(file + ".bleu", "a")
            f.write(bleu)
    except:
        print("An error occurred.")
        print("Skipped file: "+file)