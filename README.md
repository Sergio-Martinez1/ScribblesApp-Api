# Scribbles Api

Scribbles Api is an Rest-Api developed for the Scribbles App, this api was developed in [FastApi](https://fastapi.tiangolo.com/).

* It provides data to the Front-End of the app.
* Can be used for retrieving data to other apps.
* It retrives the data in json format.

This is an api for a social network style app, so manages models like:

* Users.
* Posts.
* Comments.
* Reactions.
* Tags.

If want more information about the schemas and routes can check the OpenApi documentation generated when run the api.

## Getting started

1. [Run the app with docker compose](#run-the-app-with-docker)
2. [Manual installation](#manual-installation)

## Run the app with docker compose
Create a project folder and go inside:
```
mkdir scribblesapp && cd scribblesapp
```
Clone the repository:
```
git clone https://github.com/Sergio-Martinez1/ScribblesApp-Api.git
```
Create a .env file inside Scribbles-Api folder and open it with the editor:
```
touch ./ScribblesApp-Api/.env && nano ./ScribblesApp-Api/.env
```
Paste this inside and save it with **Ctrl-x**:
```
DATABASE_URL=postgresql://user:password@db:5432/scribbles_db
SECRET_KEY=randomSecretKey
ACCESS_TOKEN_EXPIRE_SECONDS=3600
BUCKET_URL=
BUCKET_NAME=
GOOGLE_APPLICATION_CREDENTIALS=
```
Create a db folder:
```
mkdir db
```
Create a .env inside db folder and open it with the editor:
```
touch ./db/.env && nano ./db/.env
```
Paste this inside and save it with **Ctrl-x**:
```
PGUSER=user
POSTGRES_DB=scribbles_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
```
Create a docker compose file and open it with the editor:
```
touch docker-compose.yml && nano ./docker-compose.yml
```
Put this data inside the docker-compose.yml and save it with **Ctrl-x**:
```
services:
  api:
    build: ./ScribblesApp-Api
    ports:
      - 8080:8080
    env_file:
      - ./ScribblesApp-Api/.env
  db:
    image: postgres:13
    env_file:
      - ./db/.env
    volumes:
      - scribbles_db:/var/lib/postgresql/data
volumes:
  scribbles_db:
```
Run the app:
```
docker compose up
```
Go to the api url in your browser:
```
http://127.0.0.1:8080/docs
```
## Manual installation
#### Setting the database
- **If already have a database go to ->** [Setting the api](#setting-the-api)

We need to create a container with a postgresql image:
```
docker run -d \
    --name postgres \
    -e PGUSER=user \
    -e POSTGRES_DB=scribbles_db \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=password \
    -p 5432:5432 \
    --mount source=scribbles,target=/var/lib/postgresql/data \
    postgres:13 
```
With the postgres_user, postgres_password, postgres_db and port you can build your database url.
#### Setting the api

Create a project folder and go inside:
```
mkdir scribblesapp && cd scribblesapp
```
Clone the repository:
```
git clone https://github.com/Sergio-Martinez1/ScribblesApp-Api.git
```

Go to the project:

```
cd ScribblesApp-Api
```

Create a .env file, here will be the all the configuration for database and other stuff:
```
touch .env
```
Copy and paste the following in the .env file:
```
DATABASE_URL=postgresql://user:password@0.0.0.0:5432/scribbles_db
SECRET_KEY=randomSecretKey
ACCESS_TOKEN_EXPIRE_SECONDS=3600
BUCKET_URL=
BUCKET_NAME=
GOOGLE_APPLICATION_CREDENTIALS=
```

You need to specify all the fields of the .env file:
|Field|Description|Example (Please don't use in real app)|
|-----|-----------|-------|
|DATABASE_URL|The postgresql database url.|postgresql://user:password@hostname:port/db_name|
|SECRET_KEY| An arbitrary unique key that will be used to create auth tokens for authorization.|jBDT1KgdYW|
|ACCESS_TOKEN_EXPIRE_SECONDS|This field determine the time that a user will be login until the api expire the user token and needed to login again.|3600|
|BUCKET_URL|This the Google Cloud Storage bucket url that is needed when a user upload images to the app. They will be stored here.|https://storage.googleapis.com/test_bucket|
|BUCKET_NAME|This is the Google Cloud Storage bucket name.|test_bucket|
|GOOGLE_APPLICATION_CREDENTIALS|This points to the ServiceKey Google Cloud json file that is generated for a service account, is needed to have permissions to upload files to a bucket. When request in Google Cloud a service account key you will get a ServiceKey.json file, you gonna save the file in ScribblesApp_Api folder and put the file name here.| ServiceKey_GoogleCloud.json|

*If not set the credential for google cloud storage the **Files** route won't work, so you can't upload files.

Create a python virtual env:
```
python3 -m venv ./venv
```
Activate the virtual env:
```
source ./venv/bin/activate
```
Install the dependencies of the api:
```
pip3 install -r dev.requirements.txt
```
Once installed run the app:
```
uvicorn main:app
```
Go to this url in your browser:
```
http://127.0.0.1:8000/docs
```
## Setting data to the database
- If you want to see the full functionality of the api, we recommend you to insert **[this](https://drive.google.com/drive/folders/12CaabgMaTivYgKy1cBmOEJYiBQiFskxM?usp=sharing)** dummy data into your database.

Create a directory in your scribblesapp folder:
```
mkdir data && cd data
```
 and copy the data there:
```
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1qdOko_DLOH4c9kCd4-wClNXdCTMKWpXe' -O users.sql &&\
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Foo6oz4Kt8qby1kcA_w_lxgEpb_mxZE5' -O posts.sql &&\
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1b1gwzDhL5MOgr4X6kVseQZOM89XGffOh' -O comments.sql &&\
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1M2RMqBbKF9TgnsuPLv3pxlgUe0ZcvxPP' -O reactions.sql &&\
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=19uQQz27UBfv7t14FA_lYbmRLSFx1J0NQ' -O tags.sql
```
Check the name of your running postgresql container:
```
docker ps
```
**With your database and api running** copy your data into your postgres container (*change "postgres" with your database container name*):
```
for f in ./*sql; do docker cp $f postgres:/usr/src/; done
```
Once your data is inside your container, the next step is to insert your data into your database (*change "postgres" with your database container name*):
```
docker exec -it postgres psql -U user -d scribbles_db -f /usr/src/users.sql -f /usr/src/posts.sql -f /usr/src/comments.sql -f /usr/src/reactions.sql -f /usr/src/tags.sql
```
*Important: your **user** and **database name** need to be the same that you set when create your database.
#### Make a request to the api
Go to the api url:
```
http://127.0.0.1:8000/docs
```
