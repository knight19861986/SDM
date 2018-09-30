## Getting started

### Mac OS X/Linux

These instructions assume you use Python 3.

1. Install Python (google it and you will find instructions).
2. Setup virtualenv and install dependencies:
  ```
  python3 -m venv venv_thesis  # The executable might also be called just `python`.
  source venv_thesis/bin/activate
  pip install -r requirements.txt
  ```
After finished the installation:
1. Run `python manage.py migrate` to apply the data migration
2. Run the API server using `python manage.py runserver`
3. Visit http://localhost:8000/gameassistant/ to verify it is working.

### Windows

These instructions assume you use Python 3, but the code runs on Python 2 as well. It also assumes your OS is Windows 10 - equivalent instructions for other Windows versions can be found by googling.

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
9. `python -m venv venv_thesis`
10. `.\venv_thesis\Scripts\activate`
11. `pip install -r requirements.txt`

After finished the installation:
1. Run `python manage.py migrate` to apply the data migration
2. Run the API server using `python manage.py runserver`
3. Visit http://localhost:8000/gameassistant/ to verify it is working.
