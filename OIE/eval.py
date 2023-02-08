import flair
import pathlib
from flair.datasets import DataLoader, ColumnCorpus
from flair.models import SequenceTagger
import typer
import json

app = typer.Typer()


class Eval:
    def __init__(self,
                 model_path: str,
                 out_txt: str,
                 corpus: flair.data.Corpus
                 ):
        self.model_path = model_path
        self.corpus = corpus
        self.oie = SequenceTagger.load(model_path)

        path = pathlib.Path("evaluations")
        path.mkdir(parents=True, exist_ok=True)

        result = self.oie.evaluate(self.corpus.dev,
                                   mini_batch_size=1,
                                   out_path="evaluations/"+out_txt+"_dev"+".txt",
                                   gold_label_type="label")

        print(result.detailed_results)

        js = result.classification_report

        with open("evaluations/"+out_txt+"_result"+".json", "a") as f:
            json.dump(js, f, indent=4)


@app.command()
def run(model_path: str, corpus_dir: str, train: str, test: str, dev: str):

    out_txt = model_path.split("/")[-1]
    corpus = ColumnCorpus(data_folder=corpus_dir,
                          column_format={0: 'text', 8: 'label'},
                          train_file=train,
                          test_file=test,
                          dev_file=dev)

    try:
        #carregando melhor modelo
        SequenceTagger.load(model_path + "/best-model.pt")
        model_path = model_path + "/best-model.pt"
    except:
        print("best-model.pt not found, tryng to use final-model.pt")
        try:
            #carregando modelo final
            SequenceTagger.load(model_path + "/final-model.pt")
            model_path = model_path + "/final-model.pt"
        except:
            print("final-model.pt not found, are you sure you have a model in this folder?")

    Eval(model_path=model_path, out_txt=out_txt, corpus=corpus)


if __name__ == "__main__":
    app()
