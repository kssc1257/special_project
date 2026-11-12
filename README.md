# Voice-Based ERP Assistant

## Project Overview

The Voice-Based ERP Assistant is a voice-controlled system designed to help faculty interact with a college ERP system using natural language commands.

Instead of manually navigating through different ERP modules, faculty can use voice commands to perform operations such as entering marks, managing attendance and retrieving student information.

The system uses Speech-to-Text technology to convert voice commands into text and Natural Language Processing (NLP) to understand the user's intent and extract relevant information.

## Problem Statement

Traditional ERP systems require faculty to manually navigate through multiple pages and enter or retrieve information. This can be time-consuming and repetitive.

This project aims to simplify these operations by introducing a voice-based interface.

## Objectives

- Enable faculty to interact with ERP using voice commands.
- Convert speech into text using Whisper.
- Identify user intent using NLP.
- Extract important information from voice commands.
- Support data entry and data retrieval.
- Validate information before modifying database records.

## Main Features

- Voice command input.
- Speech-to-Text conversion.
- Intent classification.
- Entity extraction.
- Student information management.
- Marks and attendance operations.
- Database connectivity.
- Voice-based ERP interaction.

## System Architecture

Faculty Voice Command  
↓  
Speech-to-Text (Whisper)  
↓  
Text Command  
↓  
NLP Pipeline  
↓  
Intent Classification and Entity Extraction  
↓  
Structured JSON  
↓  
Backend Processing  
↓  
Validation and Authorization  
↓  
Data Entry / Data Fetch  
↓  
ERP Database  
↓  
Response to Faculty

## Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python |
| Speech-to-Text | Whisper |
| NLP | Python, scikit-learn / spaCy |
| Database | MySQL |
| Model Storage | Joblib |

## Project Structure

- `sp/` – Frontend files and database SQL backup.
- `sp1/` – Python backend, NLP and voice-processing modules.
- `sp/database.sql` – Database backup used to recreate the project database.

## How to Run the Project

### Prerequisites

Install the following software:

- Python 3.10 or above
- MySQL Server
- MySQL Workbench
- Git
- A code editor such as VS Code

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```bash
cd special_project
```

### Step 2: Set Up the Database

1. Open MySQL Workbench.
2. Connect to your local MySQL server.
3. Create the project database.
4. Import the `sp/database.sql` file.
5. Update the database credentials in `sp1/db.py` to match your local MySQL configuration.

### Step 3: Set Up Python Environment

Navigate to the backend directory:

```bash
cd sp1
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Backend

Start the Python application:

```bash
python app1.py
```

### Step 5: Open the Frontend

Open the frontend login page:

```text
sp/login.html
```

Alternatively, use the local frontend server if the application requires one.

### Step 6: Use the Application

1. Open the login page.
2. Log in using the configured credentials.
3. Navigate through the ERP modules.
4. Open the voice module.
5. Give a voice command and test the supported operations.

### Important Notes

- The database runs locally using MySQL.
- Import the SQL backup before starting the backend.
- Configure your own database credentials.
- Do not upload database passwords or API keys to GitHub.
- Make sure the backend is running before using features that require it.

credentials- user-zaheer
                               password- zaheer1
