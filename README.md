# <p align=center> <a name="top">ImageUploader---DRF-project </a></p>

## Short overview

This is application for uploading images. It provides the user upload image and according to the account tier the user belongs to, API creates resized thumbnails of that image and return urls to those thumbnails (image and thumbnails are saved using AWS storage). Urls have an expiration time and once the timeout expires, the specific url is no longer active. Some users (depending on account tier) can renew an expired url. 
By default, there is a command to create three basic account tiers (at the first sturtup of the application) with some permissions for sizes of the thumbnails, permission if the user can renew expired url or if the user can access the url of the orignial uploded image.
User can also list their original uploded images.
User with admin status can create new account tiers and add to it permisions.

The project uses Docker, AWS for store files, PostgreSQL database and linters such as Black, Flake8 and Mypy. The application has also been tested by unit tests (using pytest).

If you want to check out my other projects [click here.](https://github.com/krzysztofgrabczynski)

## Tool used in project

<p align=center><a href="https://www.python.org"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="60" height="60"/></a> 
<a href="https://www.djangoproject.com/"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="60" height="60"/> </a>
<a href="https://git-scm.com/"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" alt="git" width="60" height="60"/> </a> 
<a href="https://aws.amazon.com/"> <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" alt="aws" width="60" height="60"/> </a>
<a href="https://www.postgresql.org.pl/"> <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/postgresql/postgresql-original-wordmark.svg" alt="psql" width="60" height="60"/> </a>
<a href="https://www.docker.com/"> <img src="https://raw.githubusercontent.com/devicons/devicon/55609aa5bd817ff167afce0d965585c92040787a/icons/docker/docker-original-wordmark.svg" alt="docker" width="60" height="60"/> </a></p>

## Directory tree

```
|───src                            # Main directory of the project
    │   manage.py
    │
    ├───api                        # Directory with app named 'api'
    │   │   admin.py
    │   │   apps.py
    │   │   mixins.py              # .py file with 
    │   │   models.py
    │   │   permissions.py         # .py file with custom permissions
    │   │   s3.py                  # .py file with helper functioanlities to use AWS 
    │   │   serializers.py         # .py file with serialziers
    │   │   tiers.py               # .py file with functionalities for image operations (resize, save) and account tier helper functionalities
    │   │   urls.py
    │   │   views.py
    │   │   __init__.py
    │   │
    │   ├───management            # Directory with custom commands.
    │   └───migrations
    │
    ├───core                      # Main direcory of the project with files such as 'settings.py', etc.
    │
    └───tests                     # Directory with unit tests. Divided per each functionalities.
│   .gitignore
│   Dockerfile
│   README.md
│   docker-compose.yml
│   pytest.ini
│   requirements.txt
```

## Install for local use (using Docker)
- Clone the repository
- Create .env file and add requirement variables such as 'SECRET_KEY' or database parameters
- Build the Docker image using ``` docker-compose build ```
- Run containers using ``` docker-compose up ```
- Enter the ``` python manage.py migrate ``` to create migrations
- Everything done! 


## Install for local use (using local virtual environment)
- Clone the repository
- Create virtual environment using ``` python -m venv venv ``` in project directory
- Use ``` . venv/Scripts/activate ``` to activate the virtual environment
- Install required packages by ``` pip install -r requirements.txt ```
- Create .env file and add requirement variables such as 'SECRET_KEY' or database parameters
- Enter the ``` python manage.py migrate --run-syncdb ``` to update migrations
- Now, you can run the application with this: ``` python manage.py runserver ```
- Everything done! You can open Instagram app in your browser by ctrl + left click on http link in your console

 ## How to use that app after installing
 - create superuser using ``` python manage.py createsuperuser ```
 - run custom command to create basic tier accounts ``` python manage.py user_group_management ```
 - create some users on admin site and add them to speficic tier account
 - Enjoy using this app :)



