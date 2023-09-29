# Get started with PandaScan 🐼

## **v1.1.0** | _**28/09/2023**_ released by [**CAprogs**](https://github.com/CAprogs)

- The [First step](https://github.com/CAprogs/PandaScan/blob/main/Installation%20Guide.md#i-first-step) is required for those who want full access to PandaScan 🐼 Features.

- If you don't want the [**Full version**](https://github.com/CAprogs/PandaScan/releases/download/v2.1.0/PandaScan.Beta.zip) you can rely on the [**lightweight version**](https://github.com/CAprogs/PandaScan/releases/download/v2.0.0/PandaScan.Lite.zip) and jump to the [Second step](https://github.com/CAprogs/PandaScan/blob/main/Installation%20Guide.md#ii-second-step).

---

### **I. FIRST STEP**
#

- Download [**Chromewebdriver**](https://googlechromelabs.github.io/chrome-for-testing/#stable) ( Select the **right version** for your architecture as in the table below )

<img width="1493" alt="Capture d’écran 2023-09-28 à 18 14 57" src="https://github.com/CAprogs/PandaScan/assets/104645407/f795b470-cff5-4d63-af52-0a12c2687f96">

-  **COPY** the path to your `.EXE` file in your chromedriver directory & **Paste** it in the `config.json` file as below ⬇️

![Installation Guide](https://github.com/CAprogs/PandaScan/assets/104645407/bffd530c-a774-4a56-b875-6a0d2136354d)

**Please Note:** (BETA version only)
- The **`chromedriver.EXE`** file may be blocked by your computer. ( especially for **Mac users** )
- Just follow these steps ⬇️.

![ezgif com-optimize](https://github.com/CAprogs/PandaScan/assets/104645407/e629332b-3ab2-494f-a50e-88d6a9990eb1)

---

### **II. SECOND STEP**
#
I recommend using `conda` for this part. If you don't have **conda** you can install it using this [**link**](https://docs.conda.io/en/latest/miniconda.html). 

Why ? : _I'm currently using `miniconda3` with a `MacBook pro M1` chip. I downloaded the `.pkg` file from the latest release with `Python 3.10`. 
**Miniconda** is just a **lightweight distribution of Anaconda**._

For **Windows Users**, pleaser consider downloading a [`Cygwin`](https://www.cygwin.com/install.html) or an equivalent.

- Open your **Terminal**
- Enter your **Miniconda** / **Anaconda** file with the following command ⬇️
```
cd miniconda3
```
- Create a **Conda Virtual environnement** named **Pandavenv** ⬇️
```
conda create --name Pandavenv
```
- Activate the **Venv** ⬇️
```
conda activate Pandavenv
```

I assume you've already downloaded the **PandaScan file**. If not, download the **latest release** below ⬇️.

| Version  | Release |
| :-------- | :-------       |
|  `V2.1.0` | [**BÊTA**](https://github.com/CAprogs/PandaScan/releases/download/v2.1.0/PandaScan.Beta.zip)  |
|  `V2.0.0`  | [**LITE**](https://github.com/CAprogs/PandaScan/releases/download/v2.0.0/PandaScan.Lite.zip)  |

- Install `pip` in your `conda venv` using the following command ⬇️
```
conda install pip
```

- Install the **requirements** using the following command ⬇️
  - _Replace `path/to/requirements.txt` with your **requirements.txt** file path_
```
pip install -r path/to/requirements.txt
```

#
### **III. THIRD STEP**
#
- **Launch** the **PandaScan** app

Replace `path/to/App.py` with your **App.py** file path ⬇️
```
conda run -n Pandavenv python path/to/App.py
```
#

### **IV. FOURTH STEP ( Optional )**
#

If you don't like the Terminal, you can launch **PandaScan** using [**VScode**](https://code.visualstudio.com/) ⬇️

![ezgif com-video-to-gif](https://github.com/CAprogs/PandaScan/assets/104645407/83a7d7db-f17d-4929-b0ff-01a603be0ea9)

---
**Please Note:** (BETA version only)
- The **`changelog`** File is generate in _**PandaScan > websites > "whatever website" > changelog > changelog.txt**_
- The **`changelog`** File helps you visualize if data have been removed, added or if there's no change at all in a particular Website.
