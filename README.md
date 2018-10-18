## Getting started

### Mac OS X/Linux

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

Step 3: Initiation and running of the application
1. Open a new terminal and run `python manage.py migrate` to apply the data migration
2. Run the application server using `python manage.py runserver`
3. Visit http://localhost:8000/gameassistant/ to verify if it is working.

### Windows

These instructions assume you use Python 3. It also assumes your OS is Windows 10 - equivalent instructions for other Windows versions can be found by googling.

Step 1: Intallation and configuration of python
1. Install Python (google it and you will find instructions).
2. Right-click the Start menu and choose **Settings**.
3. Search for `path` and choose **Edit the system environment variables**.
4. Click **Environment variables** in the window that opens.
5. In the **User variables for User**, **Edit** `path`.
6. Add two paths (the exact path differs depending on where you installed Python):
  * `C:\Users\User\AppData\Local\Programs\Python\Python36-32\` (for `python`)
  * `C:\Users\User\AppData\Local\Programs\Python\Python36-32\Scripts` (for `pip`)
7. Open PowerShell.
8. Navigate to the task directory (the directory this file is in).
9. `python -m venv <name of venv>`
10. `.\<name of venv>\Scripts\activate`
11. `pip install -r requirements.txt`

Step 2: Intallation and initiation of MongoDB

Will be updated later

Step 3: Initiation and running the application

Will be updated later
