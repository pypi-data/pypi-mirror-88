import os
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from pathlib import Path

"""CONSTANTES (en mayuscula)"""
path = Path(__file__)  # PATH A LA FILE EN CUALQUIER ORDENADOR
path2 = Path(path.parent)  # Un directorio hacia atras
path3 = Path(path2.parent)
PATH4 = str(Path(path3.parent))

class CSVPlot():
    def __init__(self, df):
        self.df = df

    def plot(self, grafico=2, columnas=[]):
        if columnas:
            df = self.df[columnas]
        else:
            df = self.df
        if grafico == 0:
            self.plot_histograma(df)
        elif grafico == 1:
            self.plot_densidad(df)
        elif grafico == 2:
            self.plot_bigotes(df)
        elif grafico == 3:
            self.plot_correlacion(df)
        elif grafico == 4:
            self.plot_dispersion(df)
        else:
            pass

    def plot_histograma(self, df, output=False):
        df.hist()
        if not output:
            plt.show()
        else:
            plt.savefig(output)

    def plot_densidad(self, df, output=False):
        df.plot(subplots=True, layout=(10, 4), sharex = False)  # kind="density" ¿No funciona?
        if not output:
            plt.show()
        else:
            plt.savefig(output)

    def plot_bigotes(self, df, output=False):
        df.plot(kind='box', subplots=True, layout=(10, 4), sharex=False, sharey=False)
        if not output:
            plt.show()
        else:
            plt.savefig(output)

    def plot_correlacion(self, df, output=False):
        correlaciones = df.corr()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(correlaciones, vmin=-1, vmax=1)
        fig.colorbar(cax)
        if not output:
            plt.show()
        else:
            plt.savefig(output)

    def plot_dispersion(self, df):
        scatter_matrix(df)
        plt.show()

    def guardar_plot(self, save=True):  # Opcion a guardar el plot
        columns = self.df.columns.values
        for column in columns:
            try:
                self.df.hist(column=column)
                if save:
                    my_file = f'data/{column}.png'
                    plt.savefig(os.path.join(PATH4, my_file))
                else:
                    pass
            except ValueError:
                pass

    """Opcion a eliminar el plot"""

if __name__ == "__main__":
    df = pd.read_csv("../../data/csv_barcelona.csv")
    plot = CSVPlot(df)
    plot.plot()
