# Objective

To Learn devlopments with django.

# Materials

Main : Udemy course.
Others : django documentation


# Environments

MacOS: 10.15.7
Docker: 20.10.10

## Building devlopment environment

build containers

```
$ docker-compose build
$ docker-compose up -d
```

get into bash

```
$ docker-compose exec web bash
```

launch server and access from your device.

```
$ [project folder]python manage.py runserver 0.0.0.0:8000
```

if your device is already using port 8000, kill the process or edit docker-compose.yml at

```
port:
  - 8000:8000
```


# Memo

- test user

|user name|password|
|:-|:-|
|user1|kmqCaJ!i6NRDkYZd&38U|
|user2|kmqCaJ!i6NRDkYZd&38U|


