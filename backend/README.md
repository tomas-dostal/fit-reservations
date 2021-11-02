# BACKEND


# Docker stuff

The app is dockerised so we will be able to work on it without bigger problems with dependiences. 

To spin up the app, type 
```bash
$ docker-compose up
```

```bash
$ docker ps 
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS         PORTS                    NAMES
e2b5d78be02d   backend_app          "sh -c 'python manag…"   6 seconds ago    Up 4 seconds   0.0.0.0:8000->8000/tcp   backend_app_1
396aa851f220   postgres:13-alpine   "docker-entrypoint.s…"   32 minutes ago   Up 6 seconds   0.0.0.0:5432->5432/tcp   backend_db_1
```
now get inside the running container (`e2b5d78be02d`) by running `docker exec -it e2b5d78be02d sh`. You should be inside the running instance of the app. 

## Django management 

Most of the stuff with django is done throught the command line by `manage.py` script. 
- `manage.py shell` to go to the Django's shell 
- `manage.py makemigrations` to perpare changes form models.py
- `manage.py migrate` to propagate the changes to the database

In the shell you can e.g. modify/add database content. 

### Django shell 
```python
from reservations.models import *
u = User(name="Tomas", surname="Dostal", is_admin=False)
u.save()
User.objects.all()
>> <QuerySet [<User: Dostal, Tomas>]>
```
# Old good local development 

```bash
pip install -r ./requirements.txt
```
if it fails, it might be needed to install openssl and run again. 
```bash 
brew install openssl
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
```

To use dummy sqlite database change `DATABASES` in `backend/settings.py` to

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```