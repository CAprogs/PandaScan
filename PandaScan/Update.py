from Update_fmteam import Update_fmteam
from Update_lelscans import Update_lelscans
from Update_scantrad import Update_scantrad
import json

def Update(website):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    
    if config["mode"].lower() == "manual":
        print("\n Update : Manual ... \n")
        if config["websites"][website]["enabled"]:
            if website == "fmteam.fr":
                Update_fmteam()
            elif website == "lelscans.net":
                Update_lelscans()
            elif website == "scantrad-vf":
                Update_scantrad()
            print("\n Update End \n")
        else:
            print("No active method ! Please check the \"config\" file.")
    elif config["mode"].lower() == "auto":
        print("\n Update : Automatic ... \n")
        Update_fmteam()
        Update_lelscans()
        Update_scantrad()
        print(" Update End !")