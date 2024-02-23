
# Django REST framework Project
### About the project

### `1` Project structure

![][image-feat-privoder]

### `2` List Models

- Users
- Merchants
- Carts
- Cart Items
- Categories
- Products(Services)
- ProductImages
- Promotions
- Tags
- Blacklisted tokens
- Outstanding tokens


### `3` Relationships

- One User: One Merchant
- One Merchant: Multiple Products(Services)
- One Category: Multiple Cart Items
- One Cart Item: Multiple Products(Services)
- One Product(Service): Multiple Promotions
- One Product(Service): Multiple Tags

### `4` Introduce

- Use [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/readme.html) to automatically generate API documentation for Django Rest Framework:
+ [Swagger](http://localhost/swagger/)
+ [Redoc](http://localhost/redoc/)

- Dev environments: use Docker Compose file: **docker-compose-dev.yml**
- Production environments: use Docker Compose file: **docker-compose-dev.yml** (added Gunicorn and Nginx to handle static and media files)


### `5` Clone Project

`
git clone https://github.com/nhathong1204/drf_app.git
`

### `6` Deploy project to local

`
cd app/
`
>
`
python -m venv env
`
>
`
pip install -r requirements.txt
`
>
`
python manage.py makemigrations 
`
>
`
python manage.py migrate 
`
>
`
python manage.py createsuperuser
`
>
`
python manage.py runserver
`

Open Chrome Browser and go to the link http://localhost:8000/


### `7` Deploy project using Docker

- In the drf_app/ directory type the command:

`
docker-compose -f docker-compose-deploy.yml up -d --build 
`
>

- Create superuser:
`
docker-compose -f docker-compose-deploy.yml exec web python manage.py createsuperuser
`

Open Chrome Browser and go to the link http://localhost/

> \[!NOTE]
>
> Stop all applications on your computer that are using port 80


### `8` Another way to deploy the project

Unzip the **run_project.zip** file
Open the **run_project/** folder and click the **run.bat** file

> \[!NOTE]
>
> Stop all applications on your computer that are using port 80


### `9` Install dependencies

- [Django==5.0.2](https://pypi.org/project/Django/)
- [pillow==10.2.0](https://pypi.org/project/pillow/)
- [django-taggit==5.0.1](https://pypi.org/project/django-taggit/)
- [djangorestframework==3.14.0](https://pypi.org/project/djangorestframework/)
- [djangorestframework-simplejwt==5.3.1](https://pypi.org/project/djangorestframework-simplejwt/)
- [drf-nested-routers==0.93.5](https://pypi.org/project/drf-nested-routers/)
- [drf-yasg==1.21.7](https://pypi.org/project/drf-yasg/)
- [gunicorn==21.2.0](https://pypi.org/project/gunicorn/)
- [psycopg2-binary==2.9.9](https://pypi.org/project/psycopg2-binary/)
- [psycopg2-binary==2.9.9](https://pypi.org/project/psycopg2-binary/)

### `10` Video test

- Test create User, Login and using token to CRUD merchant: https://somup.com/cZn3o0pyBw
- Test CRUD Category: https://somup.com/cZn3owpygY
- Test CRUD Product and Promotions: https://somup.com/cZn0ijp4CO
- Test CRUD Cart, Cart Items: https://somup.com/cZn0j3p4H9
- Run in Window: https://somup.com/cZn0QZp4MP
- Create superuser: https://somup.com/cZn06ip49Y

[image-feat-privoder]: https://imgtr.ee/images/2024/02/23/8826b604a9af32213c7f3d0fde134cf2.png