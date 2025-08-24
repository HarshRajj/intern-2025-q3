# Q3: Basic Logging & Retries

This repository contains the solution for Question 3 of the assignment.

## Description

A minimal Python script that generates tweets using a prompt template and the Google Gemini LLM. It logs every request and response using structlog and implements exponential back-off on 5xx errors.

## Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/HarshRajj/intern-2025-q3.git
    cd intern-2025-q3
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file** and add your Google API key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

4.  **Run the script:**
    ```bash
    python main.py
    ```

## Demo

[**▶️ Run on Google Colab**](https://colab.research.google.com/drive/1jQ2d44NQM7ZS1q6DSb8lrnipzdu3T5Gx?usp=sharing)