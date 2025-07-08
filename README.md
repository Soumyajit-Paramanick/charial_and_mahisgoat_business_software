# Charial & Mahisgoat Business Management Software

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A comprehensive business management solution for Charial and Mahisgoat businesses, built with Django.

> **Important Note**: The code in this repository represents a demonstration version of the project. The final production code developed for the client is not publicly available due to confidentiality agreements. This repository serves as documentation of my work and as a basis for collaboration.

---

## Features

- **Dual Business Management**: Separate modules for Charial and Mahisgoat businesses
- **Core Modules**:
  - Bill management with party tracking
  - Daily expenses tracking
  - Trade management with seller accounts
  - Balance sheets
- **Advanced Functionality**:
  - Excel exports for all reports
  - Date-based filtering
  - Unique name validation
  - Pending amount calculations
  - Last record per seller view
- **User Authentication**:
  - Login/logout functionality
  - Dashboard with business selection

---

## Demo Video

[![Business Software Demo](https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)  
*(Click the image to watch the demo video)*

---

## Getting Started

### Prerequisites

- Python **3.9.13** (recommended)
- Git
- Virtualenv

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Soumyajit-Paramanick/charial_and_mahisgoat_business_software.git
cd charial_and_mahisgoat_business_software
### 2. Set up virtual environment

```bash
python -m venv venv
venv\Scripts\activate or source venv/bin/activate
pip install -r requirements.txt
python core/manage.py migrate
python core/manage.py createsuperuser