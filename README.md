## Getting started

### Mac OS X

These instructions assume you use Python 3.

Step 1: Intallation and configuration of python
1. Install Python (Please find instructions from google).
2. Setup virtualenv and install dependencies:
  ```
  python3 -m venv <name of venv>  # The executable might also be called just `python`
  source <name of venv>/bin/activate
  pip install -r requirements.txt
  ```
Step 2: Intallation and initiation of MongoDB
1. Install MongoDB (See https://docs.mongodb.com/guides/server/install/).
2. Run `<mongodb installation dir>/bin/mongod` to start MongoDB
3. Open another terminal and run `<mongodb installation dir>/bin/mongo`
(See https://docs.mongodb.com/manual/mongo/#start-the-mongo-shell-and-connect-to-mongodb)
4. Run `use testdb` to create the database we are going to use

Step 3: Intallation and initiation of Redis
1. Install Redis:
  ```
  mkdir redis
  cd redis
  curl -O http://download.redis.io/redis-stable.tar.gz
  tar xzvf redis-stable.tar.gz
  cd redis-stable
  make
  ```
2. Open a new terminal and run `redis-server`

Step 4: Initiation and running of the application
1. Open a new terminal and run `python manage.py migrate` to apply the data migration
2. Run the application server using `python manage.py runserver`
3. Visit http://localhost:8000/gameassistant/ to verify if it is working.

### Ubuntu

These instructions assume you use Python 3.

Step 1: Intallation and configuration of python
1. Install Python3 (Please find instructions from google).
2. Setup virtualenv and install dependencies:
  ```
  apt-get install python3-venv
  python3 -m venv <name of venv>  # The executable might also be called just `python`
  source <name of venv>/bin/activate
  pip3 install wheel
  pip3 install -r requirements.txt
  ```
Step 2: Intallation and initiation of MongoDB
1. Install MongoDB (See https://docs.mongodb.com/guides/server/install/).
2. Run `<mongodb installation dir>/bin/mongod` to start MongoDB
3. Open another terminal and run `<mongodb installation dir>/bin/mongo`
(See https://docs.mongodb.com/manual/mongo/#start-the-mongo-shell-and-connect-to-mongodb)
4. Run `use testdb` to create the database we are going to use

Step 3: Intallation and running of Redis
1. Install Redis:
  ```
  mkdir redis
  cd redis
  curl -O http://download.redis.io/redis-stable.tar.gz
  tar xzvf redis-stable.tar.gz
  cd redis-stable
  make
  ```
2. Open a new terminal and run `redis-server`

Step 4: Initiation and running of the application
1. Open a new terminal and run `python3 manage.py migrate` to apply the data migration
2. Run the application server using `python3 manage.py runserver`
3. Visit http://localhost:8000/gameassistant/ to verify if it is working.

### Windows

Will be updated later
