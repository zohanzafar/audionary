# Audionary

**Turn any PDF into an easy-to-understand audio narration.**  
Upload a file, get a smart summary, and listen to it like a podcast.

---

## Overview

Audionary transforms long and technical PDFs into digestible, spoken summaries. It's designed for anyone who wants to consume content more efficiently while commuting, multitasking, or just relaxing.

Upload a PDF → Get a natural language summary → Listen to it as audio.

---

## Features

- Upload any PDF
- Summarize complex content using AI
- Natural narration using text-to-speech
- Stream or download the audio summary
- Clean User Interface

---

## Live Demo

Watch the demo: [YouTube Demo Link](https://youtu.be/XN-Nw4oxqlI?si=ZmGH43JZRdWywUbd)

---

## Tech Stack

| Layer           | Tools Used                               |
|-----------------|------------------------------------------|
| Backend         | Python, Django REST Framework            |
| Frontend        | HTML, Tailwind CSS, JavaScript           |
| PDF Parsing     | PyMuPDF                                  |
| AI Summarization| OpenAI + LangGraph                       |
| Text to Speech  | Google Text-to-Speech (gTTS)             |
| Storage         | Local (easily extendable to cloud)       |

---

## How It Works

1. User uploads a PDF
2. Text is extracted using PyMuPDF
3. AI summarizes the content using OpenAI and LangGraph
4. A narration is generated using gTTS
5. Audio summary is played back or available for download

---

## Project Structure

```
audionary/
├── core/                 # Django API  
│   ├── views.py  
│   ├── serializers.py  
│   └── utils/            # Text extraction, summarization, audio   
├── media/                # Audio output files  
├── static/               # Static frontend assets  
├── templates/            # HTML templates  
├── .env                  # API keys and environment variables  
├── requirements.txt  
└── manage.py
```

---

## Local Setup Guide

### 1. Clone the Repository

```bash
git clone https://github.com/zohanzafar/audionary.git
cd audionary
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root directory with the following content:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Now open your browser and go to:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

1. Open the homepage.
2. Upload a PDF file.
3. The system will:
   - Extract the text
   - Generate a summary
   - Convert the summary to audio
4. Listen to or download the audio file.

---

## .env Example

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Requirements

All dependencies are listed in `requirements.txt`. Key packages include:

- Django  
- djangorestframework  
- PyMuPDF  
- gTTS  
- openai  
- langgraph  
- python-dotenv  

Install using:

```bash
pip install -r requirements.txt
```

---

## UI Screenshots

Place your screenshots in a `screenshots/` folder inside the project, and embed them here:

Example:

![Home Page](screenshots/homepage.png)  
![Upload Page](screenshots/upload.png)  
![Summary and Audio](screenshots/output.png)

---

## Coming Soon

- OCR support for scanned PDFs
- Higher-quality voices (e.g., ElevenLabs, Azure TTS)
- Language and voice selection
- User accounts to save previous files
- Background task support for large files

---

## Contributing

We welcome contributions and feedback.

Steps:

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Submit a pull request

---

## License

This project is licensed under the MIT License.
