import os
import copy
import pandas as pd
import numpy as np
from bienes_inmuebles.dataset.csv_preprocesamiento import CSV, PATH4


def test_cvs_to_dataframe():
    objeto_csv = CSV(os.path.join(PATH4, "data/csv_barcelona.csv"))
    assert objeto_csv.df.columns[1] == "listing_url"#funcion de comprobacion -> como un if para test

"""test de que plot sale bien, guardar grafico en png, ver que la file existe 

def test_plot():
    csv.plot(save=True)
    assert file_existe? """

csv = CSV(os.path.join(PATH4, "data/csv_barcelona.csv"))
df1 = pd.DataFrame(data={'col1': [1, 1,"hola", np.NaN], 'col2': [2, 2, "hola", np.NaN]})
csv.df = df1

csv2 = copy.deepcopy(csv)
df2 = pd.DataFrame(data={'col1': [1, 1,3, 5], 'col2': [2, 2, 6, 7]})
csv2.df = df2

def test_plot(csv=csv):
    csv.guardar_plot(save=True)
    assert os.path.exists(os.path.join(PATH4, "data/bathrooms.png"))# convierte path relativo en absoluto
"""test funciones nuevas"""

def test_vistazo():
    csv = CSV(os.path.join(PATH4, "data/csv_barcelona.csv"))
    cabecera, final, columnas, faltantes, forma = csv.vistazo()
    assert "neighborhood_overview" in columnas
    assert  "https://www.airbnb.com/rooms/21974"  in cabecera.values[0]

def test_duplicates(csv=csv):
    csv_dup = csv.duplicados()
    assert csv.df.shape != csv_dup.df.shape

def test_dropna(csv=csv):
    csv_dup = csv.dropna(axis=0, number=0)
    assert csv.df.shape != csv_dup.df.shape

def test_int(csv=csv):
    csv_int = csv.ints()
    assert csv.df.shape != csv_int.df.shape

def delete_test_output(output="file.png"):
    try:
        os.remove(output)
    except FileNotFoundError:
        pass

def test_histograma(csv=csv2, output = "file.png"):
    delete_test_output(output)
    csv.plot_histograma(df=csv.df,output=output)
    assert os.path.exists(output)
    delete_test_output(output)

def test_densidad(csv=csv2, output="file.png"):
    delete_test_output(output)
    csv.plot_densidad(df = csv.df,output = output)
    assert os.path.exists(output)
    delete_test_output(output)

def test_bigotes(csv=csv2, output = "file.png"):
    delete_test_output(output)
    csv.plot_bigotes(df=csv.df,output=output)
    assert os.path.exists(output)
    delete_test_output(output)

def test_correlacion(csv=csv2, output = "file.png"):
    delete_test_output(output)
    csv.plot_correlacion(df=csv.df,output=output)
    assert os.path.exists(output)
    delete_test_output(output)
    