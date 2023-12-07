# Get started with Pandascan_BETA 🐼

<div align="center">

![latest](https://img.shields.io/github/v/release/CAprogs/PandaScan?label=latest%20release)
![total_downloads](https://img.shields.io/github/downloads/CAprogs/PandaScan/total?color=purple)
</div>

- Please see Supported OS ( & tested ) versions [here](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/README.en.md#compatibility-).
- Pandascan 🐼 is still in development, so it may contains unexpected bugs.
- If you encountered any issue, open one [here](https://github.com/CAprogs/PandaScan/issues).
- See all releases [here](https://github.com/CAprogs/PandaScan/releases)

### Summary

- [I. Chromedriver 🤖](#i-chromedriver-🤖)
- [II. Installation ↧](#ii-installation-↧)
    - [MAC 💻](#mac-💻)
    - [WINDOWS 💻](#windows-💻)
- [III. Vscode ( Optional )](#iii-vscode--optional)
- [Good To Know 📝](#good-to-know-📝)
    - [Chromedriver Error 🤖](#chromedriver-error-🤖)
    - [Failed downloads ❌](#failed-downloads-❌)
    - [Skipped downloads ⏩](#skipped-downloads-⏩)
    - [Updates 🔄](#updates-🔄)
    - [ChangeLog 📝](#changelog-📝)
    - [Settings ⚙️](#settings-⚙️)


If you like this project, consider giving it a ⭐️ on Github, it helps me a lot. 🫶

---

### **I. Chromedriver 🤖**
#

- Download [**Chromewebdriver**](https://googlechromelabs.github.io/chrome-for-testing/#stable) ( Select the **right version** for your architecture as below )

<img width="1493" alt="chromedriver" src="https://github.com/CAprogs/PandaScan/assets/104645407/f795b470-cff5-4d63-af52-0a12c2687f96">

- Try to execute the **`chromedriver.exe`**. You should get a similar message :

<img width="900" alt="chromedriver_success_exe" src="https://github.com/CAprogs/PandaScan/assets/104645407/a0feb85c-b555-41ec-897a-f3b44b547373">

- Then kill the process using **`Ctrl + C`** or just manually close the terminal.
- It may not work the first time for **`Mac users`** so follow these steps ⬇️.

![ezgif com-optimize](https://github.com/CAprogs/PandaScan/assets/104645407/e629332b-3ab2-494f-a50e-88d6a9990eb1)

---

## **II. Installation ↧**

### MAC 💻
---

- Download and install [**Python**](https://www.python.org/downloads/) ( **Python 3.12** is recommended )

- Open your **Terminal**
  
- Replace `path/to/Pandascan` with the path to your **Pandascan** folder ⬇️
```
cd path/to/PandaScan
```
- Copy and Paste ⬇️
```
python3 -m venv pandavenv && source pandavenv/bin/activate && pip install -r requirements.txt && pip install --upgrade pip && python3 App.py
```
- **COPY** & **PASTE** your `chromedriver.exe` path as below ⬇️

<img width="700" alt="mac" src="https://github.com/CAprogs/PandaScan/assets/104645407/9c460df1-16df-453b-b3ca-a5c2a4f744fa">

To easily run **PandaScan** on **Mac** :
- make sure you're in the **PandaScan** folder first ( `cd path/to/Pandascan` ) and execute  ⬇️
```
source pandavenv/bin/activate && python3 App.py
```

### WINDOWS 💻 
---
On windows, installation is a bit more complicated but don't worry, just follow these steps ⬇️.

- Install [**miniconda3**](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe) (64-bit version)
- Install **Powershell** ( via the Windows store )

Make sure to **Deactivate your antivirus** before running any commands.

- Open **Anaconda prompt** and Paste :
```
conda init powershell
```
- Close **Anaconda prompt** and Open **Powershell**
- Copy & replace `path\to\Pandascan_Beta` with the right path ⬇️
```
conda create --name pandavenv -y && conda activate pandavenv && cd path\to\Pandascan_Beta && conda install pip -y && pip install -r requirements.txt && python App.py
```

- **COPY** & **PASTE** your `chromedriver.exe` path as below ⬇️
    - Don't forget to add the `.exe` extension

<img width="700" alt="windows" src="https://github.com/CAprogs/PandaScan/assets/104645407/445652ff-8091-4c37-afd2-fe52610c035a">

To easily run **PandaScan** on **Windows** :
- Create a **.txt** file with the following content ⬇️
     - replace `path\to\Pandascan_Beta` with the right path
```
@echo off
cd path\to\Pandascan_Lite
CALL conda.bat activate pandavenv
python App.py
```
- Save the **.txt** file as `panda.bat`

Now every time you want to run **Pandascan_Lite**, just execute the **.bat** file with Powershell by entering the path to `panda.bat`.
```
path\to\panda.bat
```

## **III. Vscode ( Optional )**


If you don't want to use CLI, you can run **PandaScan** using [**VScode**](https://code.visualstudio.com/) ⬇️

- Download and install [**Vscode**](https://code.visualstudio.com/)
- Open **Vscode**
- Click on **File** > **Open Folder**
- Select your **PandaScan** folder
- Select the **App.py** file
- Select your **venv** ( **pandavenv** ) as interpreter
- Click on **Run** > **Run without debugging**

![ezgif com-video-to-gif](https://github.com/CAprogs/PandaScan/assets/104645407/83a7d7db-f17d-4929-b0ff-01a603be0ea9)


## Good To Know 📝

### Chromedriver Error 🤖
---

If a `Chromedriver Error` occurs , there could be several reasons :

- You didn't download the right version of **Chromedriver** for your architecture.
- Your **Chromedriver version** doesn't `match` your **Chrome** version.
- **Chromedriver** is `blocked` by your computer. ( make sure you've allowed its execution )
- You didn't `paste` the right path to **Chromedriver**. ( on Windows, don't forget to add the `.exe` extension at the end of your path )

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

### Updates 🔄
---

There's two modes of update :
- **Manual** : this is the default mode. Only the current site's data will be updated.
- **Auto** : this mode will update all websites data when starting app.

Updates `depends on settings` you've chosen :
disabling a website's update will prevent the update from being performed for this specific website.

### ChangeLog 📝
---

The `changelog` File helps you visualize if there's **any change** in a particular website's data.

- A `changelog` File is generate in _**src > changelog > websites > "select a website"**_ after each update.

### Settings ⚙️
---
Settings are saved in `config.json`.

You can change them manually or using the **Settings** tab.

Settings that doesn't require to restart app are `download path` and `website's updates`
