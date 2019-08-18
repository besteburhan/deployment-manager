# Deployment Manager

Deployment Manager is a website where users can create or join teams, create projects, share deployment notes with teammates, comment on deployment notes and see teammates' comments immediately. This website also allows you to connect to GitHub and track your selected GitHub projects.

## Run

1. Create and activate a virtual environment with Python 3.7
```bash
virtualenv -p python3.7 my_env
source my_env/bin/activate
```

2. There is a channel layer  that uses Redis. To start a Redis server on port 6379:
```bash
docker run -p 6379:6379 -d --name redis_container redis:2.8
```

3. Install requirements
```bash
pip install -r requirements.txt
```

* if you are in trouble with installing mysqlclient  
  + For Ubuntu:

    ```bash
     sudo apt-get install python3.7-dev default-libmysqlclient-dev
    ```  
  + For Windows:

      Install wheel with specific windows and python version from [https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)
    then;

    ```bash
     pip install (installed wheel file)
    ```  
   Repeat the command:
  ```bash
   pip install -r requirements.txt
  ```

 4. Create a MySql database schema
```MYSQL
CREATE SCHEMA deploymentdb;
```

5. Set your database information on deployment_manager/settings.py file

```PYTHON
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'deploymentdb',
        'USER': '', # fill with your user name
        'PASSWORD': '', # fill with your password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

6. Initialize database
```bash
./manage.py migrate
```

7. Populate Database


   * K means clustering algorithm, which is an unsupervised machine learning algorithm, and the k-nearest neighbors algorithm, which is a supervised machine learning algorithm, has been implemented on the website. To view the relationship between the number of users' projects and the number of users' deployments, and the relationship between the number of users 'teams and the number of users' projects, we will populate the database:
     ```bash
      manage.py populate_database
     ```
     You can display statistics which is served using `CanvasJS` on index page.

8. Run development server
```bash
./manage.py runserver
```

## Structure
```bash
├── deployment_app
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── forms.py
│   ├── __init__.py
│   ├── management
│   │   └── commands
│   │       └── populate_database.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── routing.py
│   ├── statistics
│   │   ├── __init__.py
│   │   ├── k_means_clustering.py
│   │   └── k_nearest_neighbors.py
│   ├── templates
│   │   └── deployment_app
│   │       ├── base.html
│   │       ├── deployment_notes
│   │       │   └── deployment_detail.html
│   │       ├── github
│   │       │   ├── connect_github_projects.html
│   │       │   └── github_connection.html
│   │       ├── index.html
│   │       ├── profile
│   │       │   ├── edit_profile.html
│   │       │   └── profile.html
│   │       ├── projects
│   │       │   ├── main_projects.html
│   │       │   └── project_detail.html
│   │       ├── registration
│   │       │   ├── login.html
│   │       │   └── registration.html
│   │       └── team
│   │           ├── team_creation.html
│   │           ├── team_detail.html
│   │           └── teams.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── deployment_manager
│   ├── __init__.py
│   ├── routing.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media
│   ├── deployment_notes
│   ├── profile_photos
│   └── project_files
├── static
│   ├── css
│   │   ├── base.css
│   │   ├── deployment_detail.css
│   │   ├── edit_profile.css
│   │   ├── form.css
│   │   ├── github_connection.css
│   │   ├── index.css
│   │   ├── team_creation.css
│   │   └── teams.css
│   ├── images
│   │   └── download.png
│   └── javascript
│       └── index_script.js
├── manage.py
├── README.md
└── requirements.txt
```
