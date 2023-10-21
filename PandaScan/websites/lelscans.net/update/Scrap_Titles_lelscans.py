def Scrap_Titles():
    """Scrap the mangas titles.
    """
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    from Path_to_lelscans import script_repo
     
    links_list = []
    manga_name_list = []

    url = "https://lelscans.net/scan-hunter-x-hunter/400/1" # Just the starting page

    print("\nDébut Scrapping ...\n")
    try:
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
        
            print (len(manga_name_list)," mangas récupérés\n")

            print("Fin Scrapping")

            data_to_add = [{"name": name, "links": links} for name, links in zip(manga_name_list, links_list)]

            datas = pd.DataFrame(data_to_add)

            print(f"\nSauvegarde des datas ...")
            datas.to_csv(f'{script_repo}/datas/mangas.csv', index=False)

            print(f"\nFin.")

        else:
            print("Erreur, aucun manga ajouté")
            
    except:
        print(f"An Error occurred ! Please Debug | {script_repo}")



# Uncomment to debug
#if __name__ == "__main__":
    #Scrap_Titles()