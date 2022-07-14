# Foodgram app / Django / React
![foodgram_workflow](https://github.com/timurgain/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Description 
 
Foodgram is a grocery assistant. 

On this service, users will be able to publish recipes, subscribe to publications of other users, add favorite recipes to the Favorites list, and before going to the store, download a summary list of products needed to prepare one or more selected dishes..

## Technologies

- Python 3;
- Django 2.2;
- Django REST framework;
- Postgres;
- Gunicorn;
- NGINX;
- Docker;
- GitHub Actions;
- React (prepared for me).

## Site
[The main Foodgram page](http://84.201.179.139/) 

[A ReDoc page](http://84.201.179.139/api/docs/)
```
Admin (tm / super1super1)
User One (one@e.ru / one1one1)
```

## .env example

```
# django
DJANGO_SECRET_KEY=
ALLOWED_HOSTS=

# postgresql
DB_ENGINE=
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
```

## Clone repository and navigate to the folder on the command line:

```
git clone ...
```

## Plan A. Launch the application in docker containers

Be sure that docker-compose.yaml, nginx.conf, docs and frontend folder is uploaded on your server in right ways.
Check your volumes routes in the docker-compose.yaml
Install Docker with compose on your server.

Start containers from the infra folder
```
docker-compose up -d --build 
```
Now set up the django app in backend container
```
sudo docker compose exec backend python manage.py makemigrations
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py write_ingredients
sudo docker compose exec backend python manage.py write_tags
sudo docker compose exec backend python manage.py collectstatic --no-input
```

## Plan B. Launch only the django application localy

Check your local database setting. If necessary, make changes to backend/settings.py
Create and activate virtual environment:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Install dependencies from requirements.txt file:

```
pip install -r requirements.txt
```

Set up the django app:

```
python manage.py makemigrations
python manage.py migrate
python manage.py write_ingredients
python manage.py write_tags

```

Launch the project:

```
python3 manage.py runserver
```

## The autors
The app made by - [Timur Gainutdinov](https://github.com/timurgain)
as part of training at Yandex.Practicum
