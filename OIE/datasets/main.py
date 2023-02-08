from create_txt_csv import Convert
from OIE.datasets.match import OIE_Match
import typer

app = typer.Typer()


@app.command()
def criar_conll(out_name: str,
                test_size: float,
                dev_size: float,
                json_dir: str,
                input_path: str,
                PTOIE: bool = False):

    if "PTOIE" in input_path:
        PTOIE = True

    if PTOIE:
        # convertendo arquivo PTOIE_ para json
        Convert(input_path, out_name)

    # selecionar e anotar sentenças validas
    oie_match = OIE_Match(out_name, json_dir)
    oie_match.run(test_size, dev_size)

if __name__ == "__main__":
    app()
