from app.tools.jsonPlus import JsonPlus
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(base_dir, 'data/obs.json')
texte = ''

with open(file_name, "r") as f:
    lignes = f.readlines()
    for aligne in lignes:
        texte += str(aligne)

    my_json = JsonPlus().loads(texte)
    print(my_json['meteor'])
