# bbquda_web
Website for visualizing mission logs obtained from the EcoMapper and Heron drones.

#### 1. git clone https://github.com/cange017/bbquda_web.git

#### 2. With anaconda prompt, install gdal (conda install -c conda-forge gdal)

#### 3. pip install -r requirements.txt

#### 4. python manage.py migrate

#### NOTE FOR WINDOWS USERS: If you encounter the error Directory does not exist: C:\OSGeo4W64, you're going to have to manually create the folder C:\OSGeo4W64, install the 64bit OSGeo4W network installer from https://trac.osgeo.org/osgeo4w/ and be sure to select the Desktop install option from the wizard. After this you should be good to go! For some reason gdal did not make the folder for you from step 2.

#### 5. python manage.py createsuperuser

#### 6. python manage.py runserver

#### 7. Log in at http://127.0.0.1:8000/

