<div align="center">

<img width="800" alt="Developer Charles" src="https://github.com/CAprogs/PandaScan/assets/104645407/developer_charles.png">

#

## Behind PandaScan 🐼 (The Story)

### Table of Contents
- [Introduction](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#introduction)
- [Idea 💡](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#id%C3%A9e-)
- [Challenges ⛔️](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#d%C3%A9fis-%EF%B8%8F)
- [Development 🏗️](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#d%C3%A9veloppement-%EF%B8%8F)
- [Lessons Learned ✍️](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#le%C3%A7ons-tir%C3%A9es-%EF%B8%8F)
- [Acknowledgments](https://github.com/CAprogs/PandaScan/blob/main/docs/FR/LEARN.fr.md#remerciements)

#

## **Introduction**

Hello 👋, I'm Charles, 22 years old, and currently in the final year of engineering school at ECAM-EPMI Cergy in 🇫🇷.

For a few years now, I've been passionate about computers and programming in general! Like any typical student, I had to learn numerous programming languages during my studies, such as HTML, CSS, JavaScript, C, etc.

However, I found a particular affinity for learning Python 🐍, a language known for its simplicity and efficiency. Machine Learning, Automation, Application Development, and more—Python's versatility captivated me. I dove into the world of Python and have been learning new things ever since, through personal projects, courses, and YouTube videos!

In this document, we'll delve into the journey of creating PandaScan 🐼, a project dear to my heart, from its initial idea to its implementation and beyond. The story aims to share my passion, highlight the challenges I faced, and discuss the lessons that shaped this project.

## Idea 💡
It all started with TikTok! Watching videos where users shared pages of scans from my favorite manga got me thinking—how did they do it? Most online manga reading sites don't allow automatic downloading of pages. If I wanted to do the same, manually selecting and downloading each manga chapter page would take an enormous amount of time. The need to create a solution that allows me to automatically download the manga chapters I wanted arose from the fact that these chapters were only accessible online. This limitation was inconvenient when I wanted to access them offline or in remote areas.

## Challenges ⛔️
Like any project and dedicated developer, I faced numerous challenges, requiring days of debugging. The main challenges revolved around the misuse of certain libraries, data retrieval from websites, and creating a simple and user-friendly interface. I spent a lot of time testing, debugging, and exploring.

Knowing where to search and finding the solution to a specific problem is incredibly satisfying!

## Development 🏗️
Before starting my project, I needed to check if the problem had already been solved. To my surprise, there were tools to download manga scans, but they didn't consider the French-speaking aspect. So, I decided to take the plunge.

I knew I needed a way to:
- Visit online manga reading sites
- Retrieve pages ➡️ of a manga chapter ➡️ I wanted
- Store them in a folder on my computer!

On paper, it seemed simple, given my previous experience with web scraping.

1. **The Test**

In this step, I needed to test access to the site and download a page to ensure that retrieving the desired data (in this case, a manga page) was possible. This was achieved using **Requests** and later **Selenium**: I accessed the manga page and sent a request to download the manga. It seemed too simple to be true. However, the site administrators had made it complicated by hiding the image's address on another page. I quickly found a way to bypass this restriction, but the server rejected my requests. So, I decided to find another way to retrieve the image. After a few days of thinking, the idea of simply taking a screenshot of the image came to mind! To my surprise, it was possible with Selenium. The script wasn't perfect, but it worked! I didn't like the dark areas that the screenshot captured, though. I wanted a clean image, the original size, and one that took up little space, as screenshots can be large (an average of 3 MB per capture). So, I searched for a way to "crop" the image after capture. But I faced another problem: the pages were not all the same size and format (some were vertical, and others horizontal). After a few sleepless nights of testing, I managed to create a script that could "crop" the image to the correct size and format!

3. **To Action**

In this step, I needed to automate the process:
- Access the first page of the manga
- Download this page
- Store it in a folder with the "manga name" and the "current downloading chapter name"
- Then, access the next page and add it to the created sub-folder.

This had to be done until the entire chapter was downloaded! The use of loops was essential, and I needed to find a "pattern" that allowed me to access the next pages by incrementing a value. This was quite easy because all sites followed the same structure: "site/manga_name/chapter_number/page." I just had to increment "page," and it worked like a charm. The script worked perfectly! Unfortunately, this victory was short-lived.

4. **Automate Everything**

Even though everything worked perfectly, it was tedious to:
- Enter the manga's address in my script each time
- Find the pattern to download the manga.

I needed a simpler way to access the manga and chapter I wanted. Hence, the need to retrieve data for all chapter numbers and manga names available on the site. This step was cumbersome but crucial for what lay ahead.

5. **The Graphical Interface**

To allow others to use this tool, I had to put my design and development skills to the test. I thank [@ParthJadhav](https://github.com/ParthJadhav) for creating the fantastic tool [tkinter-designer](), which significantly sped up the graphical interface creation process! I also discovered the excellent tool Figma, and the application finally took shape...

6. **The Drama**

My script was originally based on a single website, and my fears came true: **CloudFlare**!

The arch-nemesis of web scrapers, the barrier to task automation had arrived on **Japscan**. I spent a lot of time trying to find a way to bypass this restriction: using **proxies**, changing **User Agent**, **Undetected-chromedriver**, all without success. The simplest solution was to change the site and start the process again.

7. **Survivor**

In my research, I found sites with a good structure, a fairly extensive catalog of manga, and accessible with simple requests: **The Scraper's Holy Grail**.

After spending some sleepless nights developing scraping scripts for these sites, I finally integrated them into my application!

8. **Develop and Improve**

Like any good perfectionist, I couldn't stop there. I absolutely had to make the script available, understandable, and organized. I'll spare you the details; I'm still figuring out how to make the final application available on all platforms and easily installable.

However, the test version is available [here](https://github.com/CAprogs/PandaScan/releases).

9. **A Essential Feature**

To achieve ultimate automation, I needed a way to keep the data up to date and avoid users manually running scripts to update available manga or chapters. 
- So, I managed script execution by creating a JSON configuration file that allows choosing between manual or automatic updates when launching the application. 
- I also set up a system to track every change in site data by saving a .txt file that includes:
  - the update number
  - the date and time of execution
  - the added or removed manga and chapters.

## Lessons Learned ✍️

While developing PandaScan 🐼, I learned a lot about GitHub, even making my first pull request on the [MISST](https://github.com/Frikallo/MISST) project. I also gained a lot of experience in application development and graphical interface design with Python! The errors I encountered, the development process—I learned a lot, and I now know how to start and lead a project like this independently. However, I would have liked to work in a team, even though the feedback from those around me helped a lot. Alone, you go faster, but together, you go further. That's why if you're interested in improving the project, I invite you to check the [CONTRIBUTION]() section to learn how to contribute to PandaScan 🐼!

## Acknowledgments

I want to express my gratitude to all the people, near and far, who contributed to the realization of this project! It would never have come to fruition without Open Source, which is why this project will remain freely accessible to anyone who wants to use it, within the limits of its use, of course.

Thanks again for reading, and I'll see you in even more exciting stories, I hope! 😋

_Charles_

---

*This document aims to provide a detailed account of the creation of PandaScan 🐼, capturing the dedication and passion invested in bringing this project to life.*

</div>
