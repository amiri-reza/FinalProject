## Getting Started

These instructions will guide you to get a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
List all the software and versions you need to install before running your project.

For example:

- Python (3.8 or higher)
- Django (3.0 or higher)
- yfinance, numpy, pandas, spacy, plotly (latest versions)
- Git


### Installation
Provide a step by step series of instructions to set up the project. Here's a basic example:

#### 1- Clone the repository:

  Using HTTPS:

  $ git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

  Or using SSH:

  $ git clone git@github.com:YOUR_USERNAME/YOUR_REPOSITORY.git

#### 2- Navigate into the directory:

  $ cd YOUR_REPOSITORY

#### 3- Create a virtual environment and activate it:

On macOS and Linux:

$ python3 -m venv env

$ source env/bin/activate

On Windows:

$ py -m venv env

$ .\env\Scripts\activate

#### 4- Install the requirements:

$ pip install -r requirements.txt

#### 5- Apply migrations:

$ python manage.py migrate

#### 6- Run the server:

$ python manage.py runserver

Your project should now be running at http://127.0.0.1:8000/.
