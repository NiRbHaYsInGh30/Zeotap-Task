# Rule Engine Evaluation

## Overview

This project is a Flask-based web application designed to evaluate rules based on user input. The rules are stored in a SQLite database, and the evaluation results are saved for future reference. The application provides a user-friendly interface for inputting data and displays the evaluation results based on predefined rules.


```
## Prerequisites

Ensure you have Python 3.7 or higher installed on your system.

## Installation

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/rule-engine-evaluation.git
cd Task1
```
## Create a Virtual Environment

Create a virtual environment to manage dependencies:

```bash
python3 -m venv venv
venv\Scripts\activate
```
## Install Dependencies

Install the necessary dependencies using pip:
```bash
pip install flask
```

## Initialize the Database

Initialize the SQLite database by running the Flask application:
```bash
python app.py
```
This will create the SQLite database and necessary tables.

## Usage

To use the application:
- Run the Application
```bash
   python app.py
```
- Open your browser and navigate to http://127.0.0.1:5000/
- Fill in the form with the required information and click "Evaluate" to see the result.
