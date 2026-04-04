# advanced-data-tools-lab1
# GPT Social Media Data Collection & Analysis System

## 📌 Project Overview
This project is a data collection and analysis system that gathers GPT-related content from multiple social media platforms:

- 🔵 YouTube — using YouTube Data API  
- 🔴 Reddit — using Selenium web scraping  

The collected data is stored in a **MongoDB database (Docker container)** and presented through a **GUI dashboard** that allows users to:

- Collect data from different sources
- Store data in MongoDB
- Analyze the dataset using built-in queries
- View insights such as:
  - Posts per month
  - Distribution by source
  - Collection methods (API vs Scraping)
  - Top topics
  - Top authors / channels

---

## 🧱 Project Architecture

The system follows a layered architecture:
# 📊 GPT Social Media Data Collection & Analysis System

## 📌 Project Overview
This project is a data collection and analysis system that gathers GPT-related content from multiple social media platforms:

- 🔵 YouTube — using YouTube Data API  
- 🔴 Reddit — using Selenium web scraping  

The collected data is stored in a **MongoDB database (Docker container)** and presented through a **GUI dashboard** that allows users to:

- Collect data from different sources
- Store data in MongoDB
- Analyze the dataset using built-in queries
- View insights such as:
  - Posts per month
  - Distribution by source
  - Collection methods (API vs Scraping)
  - Top topics
  - Top authors / channels

---

## 🧱 Project Architecture

The system follows a layered architecture:
app/
│
├── controllers/ # Application logic
├── db/
│ ├── mongo_client.py
│ └── repositories/ # Database queries
├── services/ # API + Selenium scraping
├── ui/ # GUI (Tkinter)
└── main.py # Entry point



## ⚙️ Technologies Used

- Python 3.x
- MongoDB (Docker)
- Selenium
- YouTube Data API
- Tkinter (GUI)
- PyMongo

---

## 🐳 Step 1 — Run MongoDB (Docker)

Make sure Docker is installed and running.

Run MongoDB container:

```bash
docker run -d -p 27017:27017 --name mongo-gpt mongo


---

## ⚙️ Technologies Used

- Python 3.x
- MongoDB (Docker)
- Selenium
- YouTube Data API
- Tkinter (GUI)
- PyMongo

---

## 🐳 Step 1 — Run MongoDB (Docker)

Make sure Docker is installed and running.

Run MongoDB container: 

```bash
docker run -d -p 27017:27017 --name mongo-gpt mongo

## 📦 Step 2 — Install Dependencies

Create virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

Install requirements:

pip install -r requirements.txt

If no requirements file exists:

pip install pymongo selenium webdriver-manager google-api-python-client


## 🔑 Step 3 — YouTube API Key

In the file:youtube_api_service.py
Insert your API key: API_KEY = "YOUR_API_KEY"


## 🚀 Step 4 — Run the Application
Run the GUI: python -m app.main



