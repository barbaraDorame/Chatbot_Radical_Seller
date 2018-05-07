import pandas as pd

doc = pd.read_csv("meanAndStdev.csv", ",")

fileneg = open('Negativas.txt', 'w')
filepos = open('Positivas.txt', 'w')

for i, palabra in doc[["Palabra", "Agrado"]].iterrows():
    plbr = palabra["Palabra"]
    plbr = plbr.replace('_R', '')
    plbr = plbr.replace('_V', '')
    plbr = plbr.replace('_A', '')
    plbr = plbr.replace('_N', '')
    plbr = plbr.replace('_S', '')
    plbr = plbr.replace('á', 'a')
    plbr = plbr.replace('é', 'e')
    plbr = plbr.replace('í', 'i')
    plbr = plbr.replace('ó', 'o')
    plbr = plbr.replace('ú', 'u')
    plbr = plbr.replace('ü', 'u')

    if palabra["Agrado"] < 2:
        fileneg.write(plbr + '\n')
    elif palabra["Agrado"] > 2:
        filepos.write(plbr + '\n')

fileneg.close()
filepos.close()
