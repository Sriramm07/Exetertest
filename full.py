import pandas as pd
import tqdm
import string 
from collections import Counter

def write_to_file(output_file , line: str):
    with open(output_file, "a", encoding="utf-8") as f:
        f.writelines(line)
        f.close()


def translate(maps: dict,  w: str, counter : dict):
    count = 0
    if w.isupper():
        count = 1
        w = w.lower()
    if w.capitalize() == w:
        count = 2
        w = w.lower()
    if w in maps.keys():
        counter.append(w)
        translation = maps[w]
        if count == 1:
            return translation.upper()
        elif count == 2:
            return translation.capitalize()
        return translation
    else:
        if count == 1:
            return w.upper()
        elif count == 2:
            return w.capitalize()
        else:
            return w


def run_translation(source_file, mapping_csv, output_file):
    # 1. read csv and store it
    translation_dataFrame = pd.read_csv(mapping_csv)
    maps = {}
    for i, j in zip(translation_dataFrame.iloc[:, 0].values, translation_dataFrame.iloc[:, 1].values):
        maps[i] = j
    # print(maps)

    punctuations = string.punctuation
    counter = []
    # read txt file -> for each word lookup for translation in translation_dict
    with open(source_file, "r", encoding="utf-8") as f:
        source_txt = f.readlines()
        with open(output_file, 'w') as file:
            pass
        for l in tqdm.tqdm(source_txt):
            new_line = l
            line = l.split(" ")  # list
            # print(line)
            for w in line:
                if w != "":
                    if w[0] in punctuations:
                        punctuation = w[0]
                        word = w[1:]
                        translation = translate(maps, word, counter)
                        l = l.replace(w, punctuation+translation)
                    elif w[-1] in punctuations:
                        punctuation = w[-1]
                        word = w[0:-1]
                        translation = translate(maps, word, counter)
                        l = l.replace(w, translation+punctuation)
                    else:
                        translation = translate(maps, w, counter)
                        l = l.replace(w, translation)
            write_to_file(output_file, l)
        counts = Counter(counter)
        mapped = [maps[i] for i in counts.keys()]
        df = pd.DataFrame({"English" : counts.keys(), "french" : mapped, "counts" : counts.values()})
        df.to_csv("frequency.csv", index=False)

run_translation("t8.shakespeare.txt", "french_dictionary.csv", "t8.shakespeare.translated.txt")