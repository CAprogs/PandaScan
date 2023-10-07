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
import time

####################################################   FUNCTIONS   ####################################################

def confirm_update(mode):
    """Demande à l'utilisateur s'il veut vraiment faire la MAJ

    Returns:
        _type_: bool
    """    
    result = messagebox.askquestion(f"Confirmation Check : {mode}", f"Proceed {mode}-Update ❓")
    if not result == "yes":
        return False
    return True

def check_website_settings(website,config):
    """Vérifie si la MAJ du site est activée.

    Args:
        website (str): le site à mettre à jour
        config (Any): les informations du fichier config.json

    Returns:
        _type_: bool
    """    
    if config["websites"][website]["enabled"]:
        print(f"\nUpdating {website} 🔄..")                                                                 ##### Track activity
        return True
    return False

def check_and_migrate(script_directory,i,conn,cursor):
    """Autorise la migration des datas si au moins 1 site est mis à jour.

    Args:
        script_directory (str): le chemin du script
        i (int): variable qui permet de savoir si un site à été mis à jour.
        conn (Any): la connexion à la DB
        cursor (Any): le curseur de la DB

    Returns:
        _type_: bool
    """    
    if i >= 1:
        Migrate_datas(script_directory,conn,cursor)
        print("\nUpdate & Migration completed ✅\n")                                                                    ##### Track activity
        messagebox.showinfo("Update Info ℹ️", f"Update & Migration End ✅ ! Explore the changelog file 🔎")
    else:
        print("Update Canceled ❌, can't migrate datas due to settings.")                                       ##### Track activity
        messagebox.showinfo("Update Info ℹ️", f"Update & Migration End ✅ ! Explore the changelog file 🔎")

def track_update(i,website):
    """Incrémente i si une mise à jour a été effectuée et indique quel site a été mis à jour.

    Args:
        i (int):  variable qui permet de savoir si un site à été mis à jour. 
        website (str): le site à mettre à jour
    
    Returns:
        _type_: int
    """    
    i += 1
    print(f"{website} is Up-to-date ✅")                      ##### Track activity
    return i

def check_and_perform_update(website,config,i):
    """Check if a website can be update and perform the update if it's the case.

    Args:
        website (str): le site à mettre à jour
        config (Any): les informations du fichier config.json
        i (int): variable qui permet de savoir si un site à été mis à jour.
    """    
    if check_website_settings(website,config):  
        if website == "fmteam.fr":
            Update_fmteam()
        elif website == "lelscans.net":
            Update_lelscans()
        elif website == "scantrad-vf":
            Update_scantrad()
        i = track_update(i,website)
        return i
    else:
        print(f"\n{website} can't be updated , check Settings.\n")         ##### Track activity

####################################################    UPDATES METHODS    ####################################################

# ===================================================================   Manual Update

def Manual_Update(script_directory,website,config,conn,cursor):
    """Manually Update a website if his setting is set to "True".

    Args:
        script_directory (str): le chemin du script
        website (str): le site à mettre à jour
        config (Any): les informations du fichier config.json
        conn (Any): la connexion à la DB
        cursor (Any): le curseur de la DB
    """    
    i = 0
    mode = "Manual"
    if confirm_update(mode):
        print(f"\n Searching for Updates {website} 🔄.. \n")                    ##### Track activity

        start_time = time.time()                    # lancer le timer
        i = check_and_perform_update(website,config,i)
        end_time = time.time()                      # lancer le timer
        elapsed_time = end_time - start_time        # calculer le temps écoulé           
        print(f"\n{mode}-Update took: {elapsed_time:.2f} seconds\n")                    ##### Track activity

        check_and_migrate(script_directory,i,conn,cursor)
    else:
        print(f"\n{mode} Update Canceled ❌")
        
# ===================================================================   Auto Update

def Auto_Update(script_directory,config,conn,cursor):
    """Automatically Update a website if his setting is set to "True".

    Args:
        script_directory (str): le chemin du script
        config (Any): les informations du fichier config.json
        conn (Any): la connexion à la DB
        cursor (Any): le curseur de la DB
    """    
    websites = [
    "fmteam.fr",
    "lelscans.net",
    "scantrad-vf"
    ]

    i = 0
    mode = "Auto"
    if confirm_update(mode): 
        print("\n Searching for Updates 🔄.. \n")               ##### Track activity
        for website in websites:

            start_time = time.time()                    # lancer le timer
            i = check_and_perform_update(website,config,i)
            end_time = time.time()                      # lancer le timer
            elapsed_time = end_time - start_time        # calculer le temps écoulé           
            print(f"\n{mode}-Update took: {elapsed_time:.2f} seconds\n")            ##### Track activity

        check_and_migrate(script_directory,i,conn,cursor)
    else:
        print(f"\n{mode} Update Canceled ❌")