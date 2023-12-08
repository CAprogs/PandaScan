# Get started with Pandascan_LITE 🐼

<div align="center">

![latest_release](https://img.shields.io/github/v/release/CAprogs/PandaScan?label=latest%20release)
![total_downloads](https://img.shields.io/github/downloads/CAprogs/PandaScan/total?color=purple)

</div>

- Please see Supported OS ( & tested ) versions [here](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/README.en.md#compatibility-)
- Pandascan 🐼 is still in development, so it may contains unexpected bugs.
- If you encountered any issue, open one [here](https://github.com/CAprogs/PandaScan/issues)
- See all releases [here](https://github.com/CAprogs/PandaScan/releases)


### Summary

- [I. Installation ↧](#i-installation-↧)
    - [MAC 🖥️](#mac-🖥️)
        - [Create your own executable (.sh)](#how-to-create-your-own-executable-sh)
    - [WINDOWS 💻](#windows-💻)
        - [Create your own executable (.bat)](#how-to-create-your-own-executable-bat)
- [II. VScode ( Optional )](#ii-vscode--optional)
- [Good To Know 📝](#good-to-know-📝)
    - [Failed downloads ❌](#failed-downloads-❌)
    - [Skipped downloads ⏩](#skipped-downloads-⏩)

#

<div align="center">
Download the cheatsheet for your OS below ⬇️


| <div align="center">MAC</div>  | <div align="center">Windows</div>
| :-------- | :-------
cheatsheet | cheatsheet
</div>

## **I. Installation ↧**

### MAC 🖥️
---

- Download and install [**Python**](https://www.python.org/downloads/) ( **Python 3.12** is recommended )

- Open your **Terminal**
  
- Replace `path/to/Pandascan_Lite` with the right path ⬇️
```
cd path/to/Pandascan_Lite
```
- Copy and Paste ⬇️
```
python3 -m venv pandavenv && source pandavenv/bin/activate && pip install -r requirements.txt && pip install --upgrade pip && python3 App.py
```

### How to create your own executable (.sh)
---

- Create a `panda.txt` file inside Pandascan_Lite's folder
- Copy and Paste inside `panda.txt` ⬇️
    - replace `path/to/Pandascan_Lite` with the right path
```
cd path/to/Pandascan_Lite && source pandavenv/bin/activate && python3 App.py
```
- Save the file as `panda.sh`
- Open your terminal and run ⬇️
    - replace `path/to/Pandascan_Lite` with the right path

```
chmod +x panda.sh
```

Now you can run Pandascan_Lite whenever you want with your Terminal

The easiest way is to Drag and drop `panda.sh` to the Terminal.

- You can also run Pandascan with the terminal using ⬇️
    - replace `path/to/panda.sh` with the right path
```
path/to/panda.sh
```

### WINDOWS 💻
---
On windows, installation is a bit more complicated but don't worry, just follow these steps ⬇️.

- Install [**miniconda3**](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe) (64-bit version)
- Install **Powershell**( via the Windows store )

Make sure to **Deactivate your antivirus** before running any commands.

- Open **Anaconda prompt** and Paste :
```
conda init powershell
```
- Close **Anaconda prompt** and Open **Powershell**
    - Copy & replace `path\to\Pandascan_Lite` with the right path ⬇️
```
conda create --name pandavenv -y && conda activate pandavenv && cd path\to\Pandascan_Lite && conda install pip -y && pip install -r requirements.txt && python App.py
```

### How to create your own executable (.bat)
---

- Create a `panda.txt` file with the following content ⬇️
     - replace `path\to\Pandascan_Lite` with the right path
```
@echo off
cd path\to\Pandascan_Lite
CALL conda.bat activate pandavenv
python App.py
```
- Rename the file as `panda.bat`

Now you can run Pandascan_Lite whenever you want with **Powershell**.

The easiest way is to Drag and drop `panda.bat` to **Powershell**.

- You can also run Pandascan with **Powershell** using ⬇️
    - replace `path\to\panda.bat` with the right path
```
path\to\panda.bat
```

## **II. Vscode ( Optional )**

If you don't want to use CLI, you can run **Pandascan_Lite** using [**VScode**](https://code.visualstudio.com/) ⬇️

- Download and install [**Vscode**](https://code.visualstudio.com/)
- Open **Pandascan_Lite** folder with VScode
- Select the **App.py** file
- Select your **venv** ( **pandavenv** ) as interpreter
- Click on **Run** > **Run without debugging**

![ezgif com-video-to-gif](https://github.com/CAprogs/PandaScan/assets/104645407/83a7d7db-f17d-4929-b0ff-01a603be0ea9)

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


#
<div align=center>
If you like this project, consider giving it a ⭐️ on Github, it helps me a lot. 🫶
</div>