# Site Cloner - Advanced Website Cloning Tool

## 🚀 About
Site Cloner is a Python-based web page cloning tool that allows you to **download an entire website or specific pages**, including **HTML, CSS, JS, images**, and more. The tool maintains the **original directory structure** of the website and provides an easy way to create an offline version of any site.

## ✨ Features
- ✅ **Clone single pages or entire websites** (`--full` option)
- ✅ **Download assets (CSS, JS, images) while keeping directory structure**
- ✅ **Follow internal links to fetch subpages**
- ✅ **Support for authentication via cookies**
- ✅ **Real-time progress tracking with percentage updates**
- ✅ **User-friendly output with colored status messages**

## 🛠️ Installation
Make sure you have **Python 3.6+** installed. Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

## 📌 Usage

### Clone a Single Page
```bash
python site_cloner.py "https://example.com"
```
This will **only download the main page** and its assets (CSS, JS, images).

### Clone an Entire Website (`--full`)
```bash
python site_cloner.py "https://example.com" --full
```
This will **recursively follow all internal links** and download the entire site.

### Clone with Authentication (Cookies)
```bash
python site_cloner.py "https://example.com" --cookies "sessionid=abc123; userid=456"
```
Use this option for sites that require authentication.

### Save to a Specific Folder
```bash
python site_cloner.py "https://example.com" --output "my_cloned_site"
```
This saves all downloaded files inside the `my_cloned_site/` folder.

## 🏗️ Directory Structure
The cloned website maintains a **structured format**:
```
my_cloned_site/
│── index.html
│── about.html
│── contact.html
│── assets/
│   ├── css/
│   ├── js/
│   ├── images/
```

## ⚡ Example Output
```bash
✅ Cloning started: https://example.com
🔄 Downloading page: https://example.com
🖼️ Downloading assets (CSS, JS, img)...
✅ Page saved: my_cloned_site/index.html
✅ Cloning completed!
```

## 📜 License
This project is **open-source** and distributed under the **MIT License**.

🚀 **Try it out and easily create offline versions of any website!**

