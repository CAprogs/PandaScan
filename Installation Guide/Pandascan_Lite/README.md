# Get started with Pandascan_LITE 🐼

<div align="center">

![latest_release](https://img.shields.io/github/v/release/CAprogs/PandaScan?label=latest%20release)
![total_downloads](https://img.shields.io/github/downloads/CAprogs/PandaScan/total?color=purple)

</div>

- Please see Supported OS ( & tested ) versions [here](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/README.en.md#compatibility-).
- Pandascan 🐼 is still in development, so it may contains unexpected bugs.
- If you encountered any issue, open one [here](https://github.com/CAprogs/PandaScan/issues).
- See all releases [here](https://github.com/CAprogs/PandaScan/releases)


### Summary

- [I. Installation ↧](#i-installation-↧)
    - [MAC 💻](#mac-💻)
    - [WINDOWS 💻](#windows-💻)
- [II. VScode ( Optional )](#ii-vscode--optional)
- [Good To Know 📝](#good-to-know-📝)
    - [Failed downloads ❌](#failed-downloads-❌)
    - [Skipped downloads ⏩](#skipped-downloads-⏩)


If you like this project, consider giving it a ⭐️ on Github, it helps me a lot. 🫶

---

## **I. Installation ↧**

### MAC 💻
---

- Download and install [**Python**](https://www.python.org/downloads/) ( **Python 3.12** is recommended )

- Open your **Terminal**
  
- Replace `path/to/Pandascan_Lite` with the path to your **Pandascan_Lite** folder ⬇️
```
cd path/to/Pandascan_Lite
```
- Copy and Paste ⬇️
```
python3 -m venv pandavenv && source pandavenv/bin/activate && pip install -r requirements.txt && pip install --upgrade pip && python3 App.py
```

To easily run **Pandascan_Lite** on **Mac** :
- make sure you're in the **Pandascan_Lite** folder first ( `cd path/to/Pandascan_Lite` ) and execute  ⬇️
```
source pandavenv/bin/activate && python3 App.py
```

### WINDOWS 💻
---
On windows, installation is a bit more complicated but don't worry, just follow these steps ⬇️.

- Install [**miniconda3**](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe) (64-bit version)
- Install and open **Powershell** ( via the Windows store )

Make sure to **Deactivate your antivirus** before running any commands.

- Copy & replace :
    - `path\to\miniconda3` with the path to your **miniconda3** folder
        - if you followed the default installation, it should look like `C:\Users\your_username\miniconda3`
    - `path\to\requirements.txt` with the path to **requirements.txt** (add the `.txt` extension)
    - `path\to\App.py` with the path to **App.py** (add the `.py` extension)
```
cd path\to\miniconda3 && conda create --name pandavenv -y && conda activate pandavenv && conda install pip -y && pip install -r path\to\requirements.txt && python path\to\App.py
```

To easily run **Pandascan_Lite** on **Windows** :
- Create a **.txt** file with the following content ⬇️
     - replace `path/to/miniconda3` and `path/to/App.py` with their respective paths
```
@echo off
cd path\to\miniconda3
call conda activate pandavenv
python path\to\App.py
```
- Save the file as **Pandascan_Lite.bat** ( make sure to change the extension from **.txt** to **.bat** )

Now every time you want to run **Pandascan_Lite**, just execute the **.bat** file with powershell.

## **II. Vscode ( Optional )**

If you don't want to use CLI, you can run **Pandascan_Lite** using [**VScode**](https://code.visualstudio.com/) ⬇️

- Download and install [**Vscode**](https://code.visualstudio.com/)
- Open **Vscode**
- Click on **File** > **Open Folder**
- Select your **Pandascan_Lite** folder
- Select the **App.py** file
- Select your **venv** ( **pandavenv** ) as interpreter
- Click on **Run** > **Run without debugging**

![ezgif com-video-to-gif](https://github.com/CAprogs/Pandascan_Lite/assets/104645407/83a7d7db-f17d-4929-b0ff-01a603be0ea9)


## Good To Know 📝

### Failed downloads ❌
---
If a `download fails`, there could be several reasons :
- The website's server is down.
- Your internet connection is monitered by a firewall that blocks the download.
- Your internet connection is too slow.
- The website has changed its data structure.

#### Try to :
- Delete the folder chapter's folder created and try again.
- Switch to another connection. (e.g. from WiFi to cellular data)
- Try again later if the website's server is down.
- Switch to another website ( your manga may be available on another website )

### Skipped downloads ⏩
---
If a `download is skipped`, it means that :
- The chapter is already downloaded.
- A chapter with the same name already exists in the manga's folder.

There is an exception for `Fmteam` because it has its own naming convention.

This prevents you from downloading the same chapter twice.
