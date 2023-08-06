import os
import pandas as pd
from bienes_inmuebles.dataset.csv_preprocesamiento import CSV, PATH4  # Importa clase csv y variable (CONSTANTE) PATH4

"""FUNCIONES --> API"""


def main():
    csv = CSV(os.path.join(PATH4, "data/csv_barcelona.csv"))
    # pd.set_option('max_rows', None)
    # pd.reset_option("max_rows")
    # csv.vistazo()
    # csv.estadistica()
    # csv.plot()
    csv_dup = csv.duplicados()
    csv_dup.vistazo()  # porque pone a show=1 #¿para mostrar cabecera?
    csv_na = csv_dup.dropna(number=1000, axis=1)
    # print(csv_na.vistazo())
    csv_na2 = csv_dup.dropna(number=10, axis=0)
    # print(csv_na2.df.shape)
    csv_int = csv_na2.ints()
    # print(csv_int.df.dtypes)
    print("AQUIIII")
    csv_int.vistazo(show=True)
    print(csv_int.df.isnull().sum())
    csv_mvs = csv_int.mvs()
    print(csv_mvs.df.isnull().sum())
    csv_outliers = csv_mvs.outliers()
    print(csv_outliers)
    # csv.guardar_plot()
    pd.set_option('max_rows', None)
    # set_printoptions(precision=3)
    csv_binar = csv_outliers.normalizada()
    print(csv_binar.df[0:5, 0:5])
    binar1 = csv_outliers.estandarizar()
    print(binar1.df[0:5, 0:5])
    ##DF


""" COMMAND LINE / EJECUTAS LA FILE DIRECTO"""
if __name__ == "__main__":
    main()

"""
csv = CSV("datos.csv")
csv_dupl = csv.duplicados()
csv_na = csv_dupl.dropna()

ml = ML(csv_na.df)
"""
