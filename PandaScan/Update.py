# ---------------------------------------------- 
import sys
import os
from pathlib import Path
script_directory = Path(os.path.dirname(os.path.realpath(__file__)))

# Liste de chemins à ajouter à sys.path
new_paths = [
    f"{script_directory}/websites/fmteam.fr/update", 
    f"{script_directory}/websites/lelscans.net/update", 
    f"{script_directory}/websites/scantrad-vf/update" ]

for path in new_paths:  # Insérer chaque chemin dans le path
    sys.path.append(path)
# ----------------------------------------------
from Update_fmteam import Update_fmteam
from Update_lelscans import Update_lelscans
from Update_scantrad import Update_scantrad
from Migrate import Migrate_datas
from tkinter import messagebox
from Selenium_config import driver
import json

def Manual_Update(website):
    """Manually Update the mangas chapters.

    Args:
        website (_type_): _description_
    """    
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    print("\n Update : Manual ... \n")                      ##### Track activity
    if config["websites"][website]["enabled"]:  # check config.json to deactivate website update
        if website == "fmteam.fr":
            Update_fmteam()
        elif website == "lelscans.net":
            Update_lelscans()
        elif website == "scantrad-vf":
            Update_scantrad()
        Migrate_datas()
        print("\n Update End \n")                       ##### Track activity
        messagebox.showinfo("Update [ Manual ]", f"{website} 🐼 is up-to-date ✅ ! < read the changelog file for more information >")
    else:
        messagebox.showinfo("Unable to Update ❌", f"Please check {website} state in the \"config.json\" file.") # Si la méthode correspondante au site n'est pas activée  

def Auto_Update():
    """Automatically Update the mangas chapters.
    """    
    print("\n Update : Automatic ... \n")               ##### Track activity
    Update_fmteam()
    Update_lelscans()
    Update_scantrad()
    Migrate_datas()
    print(" Update End !")                              ##### Track activity
    messagebox.showinfo("Update [ Auto ]", "All sites 🐼 are up-to-date ✅ ! < read the changelog file for more information >")
    driver.quit()
