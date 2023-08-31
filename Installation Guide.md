# Get started with PandaScan 🐼

## **v1.0.0** | _**30/08/2023**_ released by [**CAprogs**](https://github.com/CAprogs)

The [First step](https://github.com/CAprogs/PandaScan/blob/main/Installation%20Guide.md#i-first-step) is required for those who want the Full access to PandaScan 🐼 Features ( Download & Update Features ).

If you don't want the **Full version** you can rely on the [**lightweight version**](https://github.com/CAprogs/PandaScan/releases/download/v1.0.0/PandaScan.Lite.zip) and directly go to the [Second step](https://github.com/CAprogs/PandaScan/blob/main/Installation%20Guide.md#ii-second-step).

---

### **I. First step**
#
Prerequise : Ensure that you have **Google Chrome** installed on your computer. 

- Download [**Chromewebdriver**](https://chromedriver.chromium.org/downloads) ( Select the **right version** for your architecture in the table below )

<img width="1488" alt="Capture d’écran 2023-08-26 à 01 01 00" src="https://github.com/CAprogs/PandaScan/assets/104645407/26ab6c15-9f8c-4bde-9c31-134a56f40273">

-  **COPY** the path to your `.EXE` file in your chromedriver directory & **Paste** it in the `config.json` file as below ⬇️

![Installation Guide](https://github.com/CAprogs/PandaScan/assets/104645407/bffd530c-a774-4a56-b875-6a0d2136354d)

---

### **II. Second step**
#
I recommend using `conda` for this part. If you don't have **conda** you can install it using this [**link**](https://docs.conda.io/en/latest/miniconda.html). 

**N.B:** _I'm currently using `miniconda3` with a `MacBook pro M1` chip. I downloaded the `.pkg` file from the latest release with `Python 3.10`. 
**Miniconda** is just a **lightweight distribution of Anaconda**._

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

I assume you've already downloaded the **PandaScan file**. If not, **Download** the file [**here**](https://github.com/CAprogs/PandaScan/archive/refs/tags/v1.0.0.zip) and **Unzip** it.

- Install the **requirements** 

Replace `path/to/requirements.txt` with your **requirements.txt** file path ⬇️
```
conda install --file path/to/requirements.txt
```
#
If you encounter any issue installing the requirements, please consider installing `pip` in your `conda venv` using the following command ⬇️
```
conda install pip
```
Now you can install **manually** the dependencies using the following command ⬇️
```
pip install -r path/to/requirements.txt
```
#
### **III. Third step**
#
- **Launch** the **PandaScan** app

Replace `path/to/App.py` with your **App.py** file path ⬇️
```
conda run -n Pandavenv python path/to/App.py
```
#

### **IV. Fourth step ( Optional )**
#

If you don't like the Terminal, you can **launch** the **PandaScan** app using **VScode** ⬇️

GIF 2

---
**NB:**
The Update changelog File are available in _**PandaScan > datas > "whatever website" > changelog.txt**_ when you launch the Update feature.
