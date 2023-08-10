import requests
from bs4 import BeautifulSoup
import pandas as pd

links_list = []
manga_name_list = []

url = "https://lelscans.net/scan-hunter-x-hunter/400/1"

print("\nDébut Scrapping ...\n")
response = requests.get(url)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")
select_element = soup.select_one('#header-image > h2 > form > select:nth-child(2)')

if select_element and select_element.name == "select":
    for option in select_element.find_all("option"):
        url_manga = option["value"]
        links_list.append(url_manga)

        desired_part = url_manga.split("/")[-1]
        if "lecture-ligne-" in desired_part:
            manga_name = desired_part.replace("lecture-ligne-", "").replace(".php", "")
            manga_name_list.append(manga_name)
        else:
            manga_name = desired_part.replace("lecture-en-ligne-", "").replace(".php", "")
            manga_name_list.append(manga_name)

else:
    print("Erreur, aucun manga ajouté")

print (len(manga_name_list)," mangas récupérés\n")

print("Fin Scrapping")

data_to_add = [{"name": name, "links": links} for name, links in zip(manga_name_list, links_list)]

datas = pd.DataFrame(data_to_add)

print(f"\nSauvegarde des datas ...")
datas.to_csv('/Users/charles-albert/Desktop/PandaScan/PandaScan/datas/lelscans.net/mangas.csv', index=False)

print(f"\nFin.")