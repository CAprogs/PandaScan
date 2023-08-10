from bs4 import BeautifulSoup
import requests
import pandas as pd
import yaml

print("\n Importation et Creation des données ... \n")
# Ouvrir le fichier csv : mangas
datas = pd.read_csv('/Users/charles-albert/Desktop/PandaScan/PandaScan/datas/lelscans.net/mangas.csv') # Accès mangas et liens
manga_chapters_dict = {} # création du dictionnaire qui contiendra les chapitres respectifs de chaque manga

print("\nDebut Scrapping ... ")
for index, manga_name in enumerate(datas['name']):
    url = datas['links'][index]
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    select_element = soup.select_one('#header-image > h2 > form > select:nth-child(1)')
    
    print(f"\nManga : {manga_name}") # Indique dans quel manga nous sommes pour le scrapping des chapitres
    manga_chapters_dict[manga_name]=[] # Crée une clé de dictionnaire vide , avec le nom du manga qu'on explore.

    if select_element and select_element.name == "select":
        for option in select_element.find_all("option"):
            desired_part = option["value"].split("/")[-1]  # on récupère uniquement le numéro de chapitre
            chapter = "chapitre " + desired_part
            manga_chapters_dict[manga_name].append(chapter) # Ajouter le chapitre à 'manga_chapters_dict' avec sa clé correspondante
            print(f"{chapter} récupéré ")
    else:
        print(f"Erreur, aucun chapitre trouvé | {manga_name}")

# Convertir le dictionnaire en document YAML
yml_data = yaml.dump(manga_chapters_dict)

print(f"\nSauvegarde des datas ...")
# Sauvegarde des datas

with open('/Users/charles-albert/Desktop/PandaScan/PandaScan/datas/lelscans.net/mangas_chapters.yml', 'w') as file:
    file.write(yml_data)

print(f"\nFin Scrapping.")