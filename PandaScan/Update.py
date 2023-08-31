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
from tkinter import messagebox
import json

def Manual_Update(website):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    print("\n Update : Manual ... \n")                      ##### Track activity
    if config["websites"][website]["enabled"]:  # check config.json to deactive website update
        if website == "fmteam.fr":
            Update_fmteam()
        elif website == "lelscans.net":
            Update_lelscans()
        elif website == "scantrad-vf":
            Update_scantrad()
        print("\n Update End \n")                       ##### Track activity
        messagebox.showinfo("Update [ Manual ]", f"PandaScan 🐼 is up-to-date ✅ ! Check the {website} changelog file ✍️")
    else:
        messagebox.showinfo("Unable to Update ❌", f"Please check {website} state in the \"config.json\" file.") # Si la méthode correspondante au site n'est pas activée  

def Auto_Update():
    print("\n Update : Automatic ... \n")               ##### Track activity
    Update_fmteam()
    Update_lelscans()
    Update_scantrad()
    print(" Update End !")                              ##### Track activity
    messagebox.showinfo("Update [ Auto ]", "PandaScan 🐼 is up-to-date ✅ ! Check the changelogs files ✍️")
    print("\n Update : Automatic ... ( test )\n")
