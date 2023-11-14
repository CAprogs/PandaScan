# Get started with PandaScan 🐼

## Version **V2.x.x** | _**13/11/2023**_ released by [**CAprogs**](https://github.com/CAprogs)

A new release will be available soon. Stay tuned !

- Please see Supported OS ( & tested ) versions [here](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/README.en.md#os-compatibility-).
- If you encounter any issue please let me know through the [Chat](https://github.com/CAprogs/PandaScan/discussions/2).

I assume you've already downloaded **PandaScan 🐼**. If not, download the **latest release** below ⬇️.

| Version  | Release |
| :-------- | :-------  |
|  `V2.1.1` | [**BETA**](https://github.com/CAprogs/PandaScan/releases/download/v2.1.1/PandaScan.Beta.zip)  |
|  `V2.0.1`  | [**LITE**](https://github.com/CAprogs/PandaScan/releases/download/v2.0.1/PandaScan.Lite.zip)  |

`BETA` : [First step](https://github.com/CAprogs/PandaScan/blob/main/Installation%20Guide.md#i-first-step) is required for those who want full access to PandaScan 🐼 recent Features.

`LITE` : If you don't want full access to PandaScan 🐼 recent Features, jump to the [Second step](https://github.com/CAprogs/PandaScan/blob/main/Installation%20Guide.md#ii-second-step).

---

### **I. FIRST STEP**
#
- Download and install [**Vscode**](https://code.visualstudio.com/) 
- Download [**Chromewebdriver**](https://googlechromelabs.github.io/chrome-for-testing/#stable) ( Select the **right version** for your architecture as below )

<img width="1493" alt="Capture d’écran 2023-09-28 à 18 14 57" src="https://github.com/CAprogs/PandaScan/assets/104645407/f795b470-cff5-4d63-af52-0a12c2687f96">

---
- **COPY** the path to your `.EXE` file in your chromedriver directory & **Paste** it in the `config.json` file as below ⬇️
  -  On **Windows** your path will look like : `User\Desktop\file_name` | You should redefine it as `User\\Desktop\\file_name`
  
![Installation Guide](https://github.com/CAprogs/PandaScan/assets/104645407/bffd530c-a774-4a56-b875-6a0d2136354d)

**Please Note:** (BETA version only)
- The **`chromedriver.EXE`** file may be blocked by your computer. ( especially for **Mac users** )
- Just follow these steps ⬇️.

![ezgif com-optimize](https://github.com/CAprogs/PandaScan/assets/104645407/e629332b-3ab2-494f-a50e-88d6a9990eb1)

---

### **II. SECOND STEP**
#

## MAC users 

- Download and install [**Python**](https://www.python.org/downloads/) ( **Python 3.12** is recommended )

Avoid using `conda`. It may cause some issues.

- Open your **Terminal**
  - Upgrade **pip** ⬇️
```
pip install --upgrade pip
```
- Enter your **PandaScan file** ⬇️
  - Replace `path/to/PandaScan` with your **PandaScan** file path
```
cd path/to/PandaScan
```
- Create a **python venv** named pandavenv ⬇️
```
python3 -m venv pandavenv
```
- Activate the **venv** ⬇️
```
source pandavenv/bin/activate
```
- Then install **requirements** ⬇️
```
pip install -r requirements.txt
```

- Run **PandaScan** ⬇️
```
python3 App.py
```
## WINDOWS users

You can use a `python venv` or `miniconda` to run PandaScan.

Here's how to use **Miniconda** ⬇️

- Download and install [**miniconda3**](https://docs.conda.io/projects/miniconda/en/latest/)

While downloading and installing Miniconda you should use the **Conda Powershell** to create and install your venv and then launch PandaScan.

- Open your **Terminal**
- Enter your **Miniconda** file with the following command ⬇️
```
cd miniconda3
```
- Create a **Conda Virtual environnement** named **Pandavenv** ⬇️
```
conda create --name pandavenv
```
- Activate the **Venv** ⬇️
```
conda activate Pandavenv
```
- Verify if `pip` is installed in your venv using the following command ⬇️

```
pip --version
```
- If `pip` is not installed in your venv, install it using the following command ⬇️

```
conda install pip
```

- Install the **requirements** using the following command ⬇️
  - Replace `path\to\requirements.txt` with your **requirements.txt** file path
```
pip install -r path\to\requirements.txt
```

- Enter the PandaScan file ⬇️
  - Replace `path\to\PandaScan` with your **PandaScan** file path ⬇️
```
cd path\to\PandaScan
```

- Run **PandaScan** ⬇️
```
conda run python App.py
```
#

### **IV. THIRD STEP ( Optional )**
#

If you don't want to use CLI, you can run **PandaScan** using [**VScode**](https://code.visualstudio.com/) ⬇️

![ezgif com-video-to-gif](https://github.com/CAprogs/PandaScan/assets/104645407/83a7d7db-f17d-4929-b0ff-01a603be0ea9)

---
**Please Note:** (BETA version only)
- The **`changelog`** File is generate in _**PandaScan > changelog > websites > "select a website"**_
- The **`changelog`** File helps you visualize if data have been removed, added or if there's no change at all in a particular Website.
