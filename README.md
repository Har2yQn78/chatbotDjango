# ChatbotDjango

A Django-based chatbot application with text-to-SQL capabilities.

## Overview

This project implements a chatbot interface that can convert natural language queries into SQL commands. It provides both a web interface and a notebook-based demonstration.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Django
- Required Python packages (listed in requirements.txt)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chatbotDjango
   ```

2. Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Environment Configuration:
   
   - Create a .env file in the root directory
   - Use the .env.copy file as a template and fill in the required values:
     ```bash
     cp .env.copy .env
     # Edit the .env file with your configuration values
     ```

4. Run migrations:
   
   ```bash
   cd src
   python manage.py migrate
   ```

5. Create a superuser (optional):
   
   ```bash
   python manage.py createsuperuser
   ```

## Usage

### Web Interface
1. Start the Django development server:
   
   ```bash
   cd src
   python manage.py runserver
   ```

2. Access the application:
   
   - Main interface: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

3. In the admin panel, you can:
   
   - Add and manage data
   - Configure application settings

4. On the main page, you can:
   
   - Use the text-to-SQL feature to convert natural language to SQL queries
   - Interact with the chatbot interface

### Demo Version
For a demonstration version with additional features, you can use the Jupyter notebook:

```bash
jupyter notebook notebook/XX-Testversion.ipynb
```

This notebook contains examples and demonstrations of the text-to-SQL functionality in an interactive environment.

## Features
- Natural language to SQL conversion
- Web-based chat interface
- Admin panel for data management
- Jupyter notebook demo version


## Contact
hamidreza.amiri800@gmail.com
