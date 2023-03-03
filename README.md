# ARCHAEOLOGICAL DATABASE AND GIS
### Video Demo:  https://youtu.be/ZFHER4My-js
### Description: This project was made during my work in an archaeological project of Historical museum in Moscow, Russia and i prepared it as Final Project for CS50 course

#### My project consists of two main parts:
1. Creating database for storing numerical data related to strontium isotope analysis.
Strontium isotope ratios (87Sr/86Sr) are a popular tool in provenance applications in 
archeology, forensics, paleoecology, and environmental sciences.
Using bioavailable 87Sr/86Sr in provenance studies requires comparing the 87Sr/86Sr of a sample of interest
to that of 87Sr/86Sr baselines. The archaeologists use this method to distinguish local-non local organisms or organic
tissues were found during excavations.
See more: 
https://www.sciencedirect.com/science/article/pii/S0031018220302947
https://doi.org/10.1016/j.palaeo.2020.109849

2. Database to store information about settlements with geographical coordinates in case of further usage for
geospatial analysis.

3. All data can be rendered as table or visualized on the map.


Archaeologists in Eastern Europe are mostly humanitarian, so they often stuck dealing with random excel tables,
the data is messy etc. My project's scope is to simplify
the process to store and visualize those data for my project team.

Application has the following features:

* Registration
* Basic authentication
* Submitting data in form of web forms and file uploads (with general validations)
* To test file uploads please use ONLY provided templates or generated data in /static/generated_data folder.
* /static/samples folder stores templates for uploading data and favicon for my project
* Data output in form of tables and maps


I used Flask, JS, HTML and CSS to build this project. Database uses simple SQlite local db.
I also made another ('production') version of the app for my scientific team, which uses PostgresSQL 
and runs as Docker container.

models.py has 3 SQLalchemy classes for transmitting data to database.

forms.py stores a registration form using wtform library. I wasn't able to manage all required forms as wtform classes
because I stack with some issues - csrf token bug with login form, which i cannot solve for now, and my submit forms
has 3 types of coordinates and I also don't know how to manage that at this timepoint, so i've made it using pure html.

helpers.py stores @login_required function taken from the last problem set and functions for calculating the coordinates.

routes.py is the main heart - it stores all logic of my app.

all needed packages are listed in requirements.txt


General layout based on the Bootstrap library
https://getbootstrap.com/

Map is created on base of Leaflet JS library
https://leafletjs.com

Basically I used most features, created during Finance problem set and 
some more advanced features of Flask based on the course of Jim Shaped coding
https://www.youtube.com/watch?v=Qr4QMBUPxWo&t=12451s

You can run the app from any IDE with virtual python environment (I use Pycharm Community Edition)
Another way is to isolate the app in Docker container (see Dockerfile included).
Please follow those instructions:

1. Install docker https://www.docker.com and Git https://github.com/git-guides/install-git
2. from the Command Line interface execute following commands
```
git clone https://github.com/Strokman/CS50_final_project.git
```
3. Navigate to the created folder
```
cd CS50_final_project
```
```
docker image build -t gis-image .
```
```
docker run -d -p 5000:5000 gis-image
```

4. You can specify any ports you like to run the app. Don't forget in that case to explicitly specify port number 
as an argument in run.py file (see below)
```
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=${PORT_NUMBER})
```

5. After that you should be able to access the app at localhost:5000 or curl localhost:5000

PS. In the future, I would like to add some functionality like CSV export of data, expanding databases,
more advanced filters and search, map functionality (like heatmaps)

