# Django Taffy Web

| Topic              	| Taffy web Application for Dating                |
|---------------------	|----------------------------------------------	|
| Author              	| Mr. Kriengkrai Yothee                        	|
| Advisor             	| Wichit sombat, Ph.D.                         	|
| Degree              	| Bachelor of Science (Computer Science)       	|
| Academic Year       	| 2020                                         	|
---



## Abstract

Taffy is a dating web application designed to generate connections between members who are interested in love and friendship. Without limits on distance and time, using factors of belief in Thai society on the pair according to the relationship of the horoscope by using the score of the relationship according to the day of birth, zodiac, blood group, zodiac year from many astrological sources. The score of the will help the system to rank and present the members who received the high. Members can also select a partner to chat. You can reject the chosen pair. And also have space to share the experience about love. This system is developed by Django Framework technology using Python language. And connect to the SQLite database. It can be used on the Pythonanywhere web server.

Keywords: web application, web server, match, dating , Horoscope, Factors of belief in Thai society

[![](https://img.shields.io/pypi/pyversions/Django.svg)](https://python.org/downloads/)
[![](https://img.shields.io/badge/django-2.0%20%7C%202.1%20%7C%202.2-success.svg)](https://djangoproject.com/)


Full-Featured Blog with Django web framework. 


Features 
=
- User Registration
- User Login & Logout
- User Profile
- Create, Update, Edit & Delete Profiles
- Comments
- Search
- User Change Password
- Password Reset
- Customized admin panel

How To Use
=
## Clone project & Install Requirements
> Make sure you have already installed python3 and git.
```
$ git clone https://github.com/taffy63/taffy.git && cd web
$ pipenv install 
```
## Migrate & Collect Static
```
$ pipenv run m
$ python manage.py collectstatic
```
## Create Admin User
```
$ python manage.py createsuperuser
```
## Run Server
```
$ python manage.py runserver
```
> Enter your browser http://localhost:8000/. You can login via admin in http://localhost:8000/admin/.





