import os


for folder in [folder for folder in os.listdir(r"C:\Users\samahalabo\Desktop\5-behavior video CLIPS") if os.path.isdir(os.path.join(r"C:\Users\samahalabo\Desktop\5-behavior video CLIPS",folder))]:
    if folder != "no idea":
        os.makedirs(os.path.join(r"C:\Users\samahalabo\Desktop\6-GENERATED behavior examples pairs",folder),exist_ok=True)