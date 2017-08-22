# HackerTV Server

Code written using python-flask which renders [HackerTV.io](http://www.hackertv.io/). 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need Python 2.6 or newer to get started, so be sure to have an up-to-date Python 2.x installation.

Most Macs come with Python 2.7 already installed, but it’s good to double-check the version. To determine whether you have Python 2.7, open the Terminal application, type the following, and press Return:
```
python -v
```

On Windows machines, open the Command Prompt window, type the following and press Enter
```
python
```

### Installing

Virtualenv can be used to set up a development environment on your machine. Virtualenv enables multiple side-by-side installations of Python, one for each project. It doesn’t actually install separate copies of Python, but it does provide a clever way to keep different project environments isolated.

To install it on Mac OS X or Linux, use the following command:
```
$ sudo pip install virtualenv
```

Use the following command to install it on Windows:
```
pip install virtualenv
```

Clone the repository to a folder and navigate to it using the terminal. To create a virtualenv, run the following command:
```
virtualenv venv
```

To activate the corresponding environment and install flask on OS X or Linux, use the following command:
```
$ . venv/bin/activate
$ pip install Flask
```

and on Windows:
```
venv\Scripts\activate
pip install Flask
```

## Running the server

To run the application you can either use the flask command or python’s -m switch with Flask. Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable.

This can be done on Mac OS X or Linux using:
```
$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/
```

and on Windows:
```
set FLASK_APP=hello.py
flask run
 * Running on http://127.0.0.1:5000/
```

To view the website in action, head over to [http://127.0.0.1:5000/]( http://127.0.0.1:5000/)