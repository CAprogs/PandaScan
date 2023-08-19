from Update_fmteam import Update_fmteam
from Update_lelscans import Update_lelscans
from Update_scantrad import Update_scantrad

def Update(website):
    if website == "fmteam.fr":
        Update_fmteam()
    elif website == "lelscans.net":
        Update_lelscans()
    elif website == "scantrad-vf":
        Update_scantrad()