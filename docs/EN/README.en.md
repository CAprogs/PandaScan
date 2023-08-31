# Behind PandaScan 🐼 (The Story)

## Table of Contents
- [Introduction](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/LEARN.en.md#introduction)
- [Idea 💡](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/LEARN.en.md#idea-)
- [Challenges ⛔️](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/LEARN.en.md#challenges-%EF%B8%8F)
- [Development 🏗️](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/LEARN.en.md#development-%EF%B8%8F)
- [Lessons Learned ✍️](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/LEARN.en.md#lessons-learned-%EF%B8%8F)
- [Acknowledgments](https://github.com/CAprogs/PandaScan/blob/main/docs/EN/LEARN.en.md#acknowledgments)

#

## **Introduction**

Hello 👋, my name is Charles, I'm 22 years old, and I'm in my final year of engineering school at ECAM-EPMI Cergy in 🇫🇷

For a few years now, I've been passionate about computers and programming in general! Like any typical student, I had to learn numerous programming languages during my studies, such as HTML, CSS, JavaScript, C, etc.

However, I found a greater interest in learning Python 🐍, a language known for its simplicity and efficiency. Machine Learning, Automation, App Development, etc... The possibilities with this language are vast and diverse. So, I jumped into it, and for the past few years, I've been continuously learning new things, whether through personal projects, courses, or YouTube videos!

In this document, we will delve into the journey of creating PandaScan 🐼, a project that means a lot to me, from its initial idea to its implementation and beyond. The upcoming story aims to convey my passion, acquaint you with the challenges I faced, and share the lessons that shaped this project.

## Idea 💡
The idea came to me while watching Tiktok videos! Accounts were sharing pages of scans from my favorite manga, and I wondered how they did it, as most, if not all, online manga reading sites don't allow us to download these pages automatically. I realized that if I wanted to do the same thing, I would waste a tremendous amount of time selecting each chapter page to download. The need to create a solution that would allow me to automatically download the manga chapters I wanted also arose from the fact that these chapters are only accessible through an internet connection, which is unfortunate when we want to access them offline or in remote areas, far from everything.

## Challenges ⛔️
Like any respectable project and developer, I certainly faced numerous problems, requiring many days of debugging. The main challenges I encountered were mainly related to outdated syntax of certain libraries, data retrieval from websites, and creating a user-friendly interface. I spent a lot of time testing, debugging, and researching. Knowing where to search and finding the solution to a specific problem brings a great deal of satisfaction!

## Development 🏗️
Before starting my project, I needed to verify that the problem hadn't already been solved. To my great surprise, there were indeed tools to do this, but they didn't take the Francophone aspect into account! So, I decided to embark on this adventure. I knew I needed a way to **access online manga reading sites**, **retrieve the pages => of the chapter => of a manga** that I wanted, and **store it in a folder** on my computer! On paper, it seemed simple to do, given that I had already dealt with web scraping before.

1. **Testing**

In this step, I needed to test accessing the site and downloading a page to ensure the project was feasible. Access was possible with either Request or Selenium, but I needed to see what happened when my script ran. Therefore, I opted for the combination of Selenium + Request. I accessed the page of my manga and sent a request to download the manga, and it worked. Too simple! The site's developers had complicated things and hidden the address containing the image on another page. I was able to quickly bypass this restriction, but the server was rejecting my requests. So, I decided to find another way to retrieve the image. After a few days of reflection, the idea of simply taking a screenshot of the image came to mind! To my surprise, this was possible with Selenium. The script wasn't perfect, but it worked! Additionally, I didn't like the dark areas that the screenshot captured, I wanted the image alone, clean, at the original size, and taking up less space because, yes, screenshots take up space (an average of 3 MB per capture). So, I looked for a way to "crop" the image after capture, but I encountered another problem: the pages are not all the same size and not all in the same format (some were vertical and others horizontal). After a few nights of testing, I managed to create the script that allowed me to "crop" the image to the correct size and format!

3. **Taking Action**

In this step, I needed to automate the process: access the first page of the manga, download this page, and store it in a folder named after the manga, which would contain the "name of the chapter being downloaded." Then, I needed to access the next page and add it to the created sub-folder. This had to be done until the entire chapter was downloaded! The use of loops was essential. I needed to find a "pattern" that allowed me to access the following pages by incrementing a value. This was quite easy since all the sites followed the same architecture: "site/manga_name/chapter_number/page." I just had to increment "page," and it was done. The script worked wonderfully! Unfortunately, this wasn't enough...

4. **Full Automation**

Although everything was working perfectly, it was tiresome to enter the manga's address and find the pattern each time in my script before downloading the manga. I needed a simpler way to access the manga I wanted, as well as the chapter I wanted! Hence the need to retrieve data about all chapter numbers and all available manga names from the site. This step was painstaking but useful for the future.

5. **Graphic Interface**

To allow others to use this tool, I needed to put my design and development skills to the test. I thank "" for developing the amazing tool [tkinter-designer](), which significantly sped up the development process for me! I discovered the fantastic tool called Figma, and the application was finally taking shape...

6. **The Drama**

At that time, my script was based on just one website, and what I feared happened: CloudFlare! The arch-nemesis of web scrapers, the barrier to task automation, had arrived on Japscan. I spent a lot of time searching for ways to bypass this restriction: using proxies, changing User Agents, Undetected-chromedriver... All without success. The simplest solution was to change the website and start the process again.

7. **Survivor**

In my research, I found websites with a good structure, a fairly wide range of manga, and accessibility through simple requests! The scraper's holy grail. After spending a few sleepless nights developing scraping scripts for the relevant sites, I finally integrated them into my application!

8. **Develop and Improve**

As any self-respecting perfectionist would do, I couldn't stop at this task. I absolutely had to make the script available, understandable, and organized. I'll spare you the details; I'm still racking my brains... Nevertheless, the test version is available [here]().

9. **A Luxury Feature**

To achieve ultimate automation, I needed a way to keep the data up to date and prevent the user from manually running the script to update available manga or chapters. So, I managed the execution of these scripts by creating a JSON configuration file that allowed users to choose between manual or automatic updates when launching the application. I also set up a system to track every change in the site's data: added or removed manga and chapters, update date and time.

## Lessons Learned ✍️

While developing PandaScan 🐼, I learned a lot from GitHub. I even managed to make my first pull request on the [MISST project](https://github.com/Frikallo/MISST).

I also learned a lot about application development and graphical interface design with Python! The mistakes I encountered, the development process—I learned a lot, and now I know how to approach and carry out a project like this independently. Nevertheless, I would have liked to work in a team, even though the feedback from those around me was very helpful. Alone, we go faster, but together, we go further. That's why, if you're interested in improving the project, I invite you to check out the [CONTRIBUTION section]() to learn how to contribute to PandaScan 🐼!

## Acknowledgments

I would like to express my gratitude to all those who played a role, whether close or distant, in making this project a reality! This project would never have come to fruition without Open Source, which is why this project will remain freely accessible to anyone who wants to use it, within the limits of its use, of course!

Thank you again for reading, and I hope to see you in even more exciting stories in the future 😋.

_Charles_

---

*This document aims to provide an in-depth account of the creation of PandaScan 🐼, capturing the dedication and passion invested in bringing this project to life.*
