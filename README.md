# bbquda_web
Website for visualizing mission logs obtained from the EcoMapper and Heron drones.

#### 1. git clone https://github.com/cange017/bbquda_web.git

#### 2. With anaconda prompt, install gdal (conda install -c conda-forge gdal)

#### 3. pip install -r requirements.txt

#### 4. python manage.py migrate

#### 5. python manage.py createsuperuser

#### 6. python manage.py runserver

#### 7. Log in at http://127.0.0.1:8000/

#### 7. Switch to your team's branch:

##### (a) git branch -r (to see all remote branches)

##### (b) git checkout branch-name (for example, if you want to pull UI, do "git checkout UI" and do not include remotes/origin part)

##### (c) git checkout -b new-branch-name (if you want to make a new local branch to work on your own changes)
