# Get started with PandaScan 🐼

## **v1.0.0** | _**23/08/2023**_ released by [**CAprogs**](https://github.com/CAprogs)

`The First following step is required for those who want the Full access to PandaScan 🐼 Features ( Download & Update Features ).`

If you don't want the **Full version** you can rely on the [**lightweight version**](https://github.com/CAprogs/PandaScan/releases/download/v1.0.0/PandaScan.Lite.zip).

---

### **I. First step**
#
Prerequise : Ensure that you have **Google Chrome** installed on your computer. 

- Download [**Chromewebdriver**](https://chromedriver.chromium.org/downloads) ( Select the **right version** for your architecture )
-  Access this **URL** `chrome://version/` & **COPY** the path below ⬇️ 

Photo 1

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

Gif 1

---
**NB:**
The Update changelog File are available in _**PandaScan > datas > "whatever website" > changelog.txt**_ when you launch the Update feature.