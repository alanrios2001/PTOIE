import pathlib
import random

class Merge:
    def __init__(self, datasets: list, output_name: str):
        self.datasets = datasets
        self.merged = ""

        for i in range(len(datasets)):
            with open(datasets[i], "r", encoding="utf-8") as file:
                data = file.read()
                data = data.split("\n\n")
                random.shuffle(data)
                data = "\n\n".join(data)
                self.merged += data

        path = pathlib.Path("merges")
        path.mkdir(parents=True, exist_ok=True)

        with open(f"merges/{output_name}.txt", "a", encoding="utf-8") as file:
            file.write(self.merged)

        print(f"len {output_name}: ", len(self.merged.split("\n\n")))

datasets_train = ["saida_match/PTOIE_train.txt",
                  "conll2bioes_output/pud_200_train.txt",
                  "conll2bioes_output/pud_100_train.txt",
                  "conll2bioes_output/gamalho_train.txt",
                  "conll2bioes_output/pragmatic_ceten_train.txt",
                  "conll2bioes_output/pragmatic_wiki_train.txt"]

datasets_test = ["saida_match/PTOIE_test.txt",
                 "conll2bioes_output/pud_200_test.txt",
                 "conll2bioes_output/pud_100_test.txt",
                 "conll2bioes_output/gamalho_test.txt",
                 "conll2bioes_output/pragmatic_ceten_test.txt",
                 "conll2bioes_output/pragmatic_wiki_test.txt"]

datasets_dev = ["saida_match/PTOIE_dev.txt",
                 "conll2bioes_output/pud_200_dev.txt",
                 "conll2bioes_output/pud_100_dev.txt",
                 "conll2bioes_output/gamalho_dev.txt",
                 "conll2bioes_output/pragmatic_ceten_dev.txt",
                 "conll2bioes_output/pragmatic_wiki_dev.txt"]

names = ["PTOIE_plus_train", "PTOIE_plus_test", "PTOIE_plus_dev", "merge_train", "merge_test", "merge_dev"]

if len(datasets_dev) == 6:
    Merge(datasets_train, names[0])
    Merge(datasets_test, names[1])
    Merge(datasets_dev, names[2])
else:
    Merge(datasets_train, names[3])
    Merge(datasets_test, names[4])
    Merge(datasets_dev, names[5])