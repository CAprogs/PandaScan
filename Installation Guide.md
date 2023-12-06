# Get started with PandaScan 🐼

## Version **V3.x.x** | _**05/12/2023**_ released by [**CAprogs**](https://github.com/CAprogs)

- Please see Supported OS ( & tested ) versions [here](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/README.en.md#os-compatibility-).
- PandaScan 🐼 is still in development, so it may contains unexpected bugs.
- If you encountered any issue, open one [here](https://github.com/CAprogs/PandaScan/issues).

I assume you've already downloaded **PandaScan 🐼**. If not, download the **latest release** below ⬇️.

| Version  | Release |
| :-------- | :-------  |
|  `V3.1.1` | [**BETA**](https://github.com/CAprogs/PandaScan/releases/download/v3.1.1/Pandascan_Beta.zip)  |
|  `V3.0.1`  | [**LITE**](https://github.com/CAprogs/PandaScan/releases/download/v3.0.1/Pandascan_Lite.zip)  |

`BETA` : [First step](https://github.com/CAprogs/PandaScan/blob/main/Installation%20Guide.md#i-first-step) is required.

`LITE` : Directly jump to the [Second step](https://github.com/CAprogs/PandaScan/blob/main/Installation%20Guide.md#ii-second-step).

---

### **I. FIRST STEP**
#

- Download and install [**Python**](https://www.python.org/downloads/) ( **Python 3.12** is recommended )

Avoid using `conda`, it may cause some issues.

- Download [**Chromewebdriver**](https://googlechromelabs.github.io/chrome-for-testing/#stable) ( Select the **right version** for your architecture as below )

<img width="1493" alt="Capture d’écran 2023-09-28 à 18 14 57" src="https://github.com/CAprogs/PandaScan/assets/104645407/f795b470-cff5-4d63-af52-0a12c2687f96">

- Try to execute the **`chromedriver.exe`**. You should get a similar message :

[Photo]
- Then kill the process using **`Ctrl + C`** or just manually close the terminal.
- It may not work the first time for **`Mac users`** so follow these steps ⬇️.

![ezgif com-optimize](https://github.com/CAprogs/PandaScan/assets/104645407/e629332b-3ab2-494f-a50e-88d6a9990eb1)

---

### **II. SECOND STEP**
#

## MAC users 

- Open your **Terminal**
  
- Replace `path/to/Pandascan` with the path to your **Pandascan** folder ⬇️
```
cd path/to/PandaScan
```
- Create & Activate a **python venv** named pandavenv ✚ Install the **requirements** & Upgrade **pip** ⬇️
```
python3 -m venv pandavenv && source pandavenv/bin/activate && pip install -r requirements.txt && pip install --upgrade pip
```
- Run **PandaScan** ⬇️
```
python3 App.py
```
- **COPY** & **PASTE** the `chromedriver.exe` path as below ⬇️

[PHOTO]

You can now easily start **PandaScan** whenever you want using the following command ⬇️
- make sure you're in the **PandaScan** folder first ( `cd path/to/Pandascan` )
```
source pandavenv/bin/activate && python3 App.py
```

## WINDOWS users 

- Open your **Command Prompt**
  
- Replace `path\to\Pandascan` with the path to your **Pandascan** folder ⬇️
```
cd path\to\Pandascan
```
- Create & Activate a **python venv** named pandavenv ✚ Install the **requirements** & Upgrade **pip** ⬇️
```
python -m venv pandavenv && .\pandavenv\Scripts\activate && pip install -r requirements.txt && python -m pip install --upgrade pip
```
- Run **Pandascan** ⬇️
```
python App.py
```
- **COPY** & **PASTE** the `chromedriver.exe` path as below ⬇️
    - Don't forget to add the `.exe` extension at the end of your path

[PHOTO]


You can now easily start **PandaScan** whenever you want using the following command ⬇️
- make sure you're in the **PandaScan** folder first ( `cd path\to\Pandascan` )
```
source .\pandavenv\Scripts\activate && python App.py
```

### **IV. THIRD STEP ( Optional )**
#

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
---

### Chromedriver Error 🤖 ( BETA only )

If a `Chromedriver Error` occurs , there could be several reasons :

- You didn't download the right version of **Chromedriver** for your architecture.
- Your **Chromedriver version** doesn't `match` your **Chrome** version.
- **Chromedriver** is `blocked` by your computer. ( make sure you've allowed its execution )
- You didn't `paste` the right path to **Chromedriver**. ( on Windows, don't forget to add the `.exe` extension at the end of your path )

#
 Download speed depends on your internet connection.

### Failed downloads ❌

If a `download fails`, there could be several reasons :
- The website's server is down.
- Your internet connection is monitered by a firewall that blocks the download.
- Your internet connection is too slow.
- The website has changed its data structure.

#### You can always try to :
- Delete the folder chapter's folder created and try again.
- Switch to another connection. (e.g. from WiFi to cellular data)
- Try again later if the website's server is down.
- Switch to another website ( your manga may be available on another website )
#

### Skipped downloads ⏩
If a `download is skipped`, it means that :
- The chapter is already downloaded.
- A chapter with the same name already exists in the manga's folder.

There is an exception for `Fmteam` because they have their own naming convention.

This prevents you from downloading the same chapter twice.
#

### Updates 🔄 ( BETA only )

There's two modes of update :
- **Manual** : this is the default mode. Only the current site's data will be updated.
- **Auto** : this mode will update all websites data when starting app.

Updates `depends on settings` you've chosen :
disabling a website's update will prevent the update from being performed for this specific website.
#

### ChangeLog 📝 ( BETA only )

The `changelog` File helps you visualize if there's **any change** in a particular website's data.

- A `changelog` File is generate in _**src > changelog > websites > "select a website"**_ after each update.

#

### Settings ⚙️ ( BETA only )

Settings are saved in `config.json`.

You can change them manually or using the **Settings** tab.

The only setting that doesn't require to restart app is the `download path` : the new path will be used for the next download.

# 
#

Pandascan will remain **FREE** and **OPEN SOURCE**.

**`Contributions`** are very welcome. 

If you like this project, consider giving it a ⭐️ on Github, it helps me a lot. 🫶