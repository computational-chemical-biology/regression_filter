from matplotlib import pyplot as plt
from matchms.importing import load_from_mgf
from matchms import calculate_scores
from matchms.similarity import ModifiedCosine
import click 

@click.command()
@click.option("--query_spec",
              default='',
              help="pathway to the spectrum that will be compared against your in-house db spectra")
@click.option("--db",
              default='',
              help="pathway to the DB to be compared against the query spectra")
@click.option("--output",
              default='./',
              help="pathway to output directory")

def spectra_comparison(query_spec, db, output):
    """
    Calculates the spectral similarity between the spectrum of interest
    and the user's spectral database, as well as presenting mirrorplots.
    Parameters:
    -------------------
    query_spec: string
      Path to the spectrum to be compared against the user's spectrum db.
    db: string
      Path to the user's spectrum db to be compared against the query spectra
    output: string
      Path to output directory
    -------------------
    Returns:
      Mirror plots of the spectrum of interest against the user's spectral database
      and the similarity score that results from each comparison.
    """
    if output[-1] != '/':
      output += '/'

    query_spec = list(load_from_mgf(query_spec))
    db = list(load_from_mgf(db))

    similarity_measure = ModifiedCosine(tolerance=0.7)

    ## Building the mirrorplots
    for i in range(len(db)):
        for j in range(len(query_spec)):
            spectrums =[db[i], query_spec[j]]
            score_modcosine = calculate_scores(spectrums, spectrums, similarity_measure, is_symmetric=True)
            print(f"Cosine score between user_db("+str(i)+") and query_spectra("+str(j)+")" + f" is {score_modcosine.scores[1][2][0][0]:.2f} with {score_modcosine.scores[1][2][0][1]} matched peaks")
            db[i].plot_against(query_spec[j], grid=False)
            plt.xlim(0, 300)
            text = f'Matched Peaks: {score_modcosine.scores[1][2][0][1]} \nCosine Score: {score_modcosine.scores[1][2][0][0]:.2f}'
            plt.text(2, 0.65, text, fontsize=9)
            plt.savefig(output+"/comparison_user_db("+str(i)+")_query_spectra("+str(j)+").pdf")

if __name__ == '__main__':
    spectra_comparison()
