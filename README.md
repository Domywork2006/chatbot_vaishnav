# AI Chatbot - Vaishnav

## Problem Statement

The goal of this project was to create a simple AI-powered question answering chatbot using the Groq API and Python.

The chatbot should:
- Accept user input
- Send the message to an AI model
- Display AI-generated responses
- Maintain conversation history for multi-turn chat

---

## Approach

The project was developed using Python and the Groq API.

Main steps followed:
1. Created a Python virtual environment
2. Installed the Groq Python library
3. Connected to the Groq API using an API key
4. Sent prompts to the AI model
5. Displayed responses in the terminal
6. Added conversation memory using a messages list
7. Implemented a multi-turn chatbot loop

---

## Steps Taken to Solve the Problem

### Environment Setup
- Installed Python 3.10+
- Created virtual environment using:
```bash
python -m venv venv
```

### Dependency Installation
Installed Groq library:
```bash
pip install groq
```

### Chatbot Development
- Created `chat.py`
- Imported Groq library
- Initialized Groq client
- Used `llama-3.1-8b-instant` model
- Added system prompt
- Added user and assistant message history

---

## Challenges Faced

### 1. Model Deprecation Error
The older model `llama3-8b-8192` was deprecated.

### Solution
Updated model to:
```python
llama-3.1-8b-instant
```

---

### 2. Invalid API Key Error

Initially received authentication errors due to incorrect API key formatting.

### Solution
Generated a new API key from Groq Console and updated the code correctly.

---

### 3. VS Code Import Warning

The Groq import appeared in yellow due to interpreter mismatch.

### Solution
Selected the correct virtual environment interpreter in VS Code.

---

## How to Run the Project

### Step 1 — Clone Repository

```bash
git clone <repository_link>
```

### Step 2 — Open Project Folder

```bash
cd ai-chatbot_vaishnav
```

### Step 3 — Create Virtual Environment

```bash
python -m venv venv
```

### Step 4 — Activate Virtual Environment

#### Windows
```bash
venv\Scripts\activate
```

### Step 5 — Install Dependencies

```bash
pip install groq
```

### Step 6 — Add Your Groq API Key

Inside `chat.py`, replace:

```python
YOUR_API_KEY
```

with your actual Groq API key.

---

### Step 7 — Run Application

```bash
python chat.py
```

---

## Technologies Used

- Python
- Groq API
- VS Code
- GitHub
