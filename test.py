import pandas as pd

import json


df = pd.read_csv('hdf_list_2021.csv')

df.to_json("tg.json", orient="records")
