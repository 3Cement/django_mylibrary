# django_mylibrary

My private library project created with Django

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
1. Create your virtual environment
2. Clone this repository
3. Install requirements
4. Initialize database
5. Run mylibrary app
```

### Installing

A step by step series of examples that tell you how to get a development env running

1. Create new virtual environment, for example with virtualenvwrapper:

```
$ pip install virtualenvwrapper
$ mkvirtualenv example_venv
```

2. Clone this repository:

```
$ git clone https://github.com/3Cement/django_mylibrary
```
2.1. Change you time zone in settings.py if you are in different one than Europe/London

```
TIME_ZONE = 'Europe/London'
```

3. Install requirements:

```
$ pip install -r requirements.txt
```

4. Initialize database

```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

5. Run mylibrary app (in folder with manage.py file):

```
$ python manage.py runserver
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Run tests from folder with manage.py file:

```
$ python manage.py test
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
