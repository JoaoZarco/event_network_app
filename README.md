# Event Network

## Setup

clone the repository:

```sh
$ git clone https://github.com/JoaoZarco/event_network_app.git
$ cd project
```


Create a virtual environment at your will and install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies, migrations for the database need to be created and deployed:
```sh
(env)$ cd project
(env)$ python manage.py makemigrations user
(env)$ python manage.py makemigrations event
(env)$ python manage.py migrations
```
After that is sorted the project is ready to be run:
```sh
(env)$ cd project
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/` in order to access the home page.
Navigating throw the website should be intuitive 

## Tests

To run all tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test
```