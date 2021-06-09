# NFL Spread Gambling App
## Ben Hakimi (QA: Stephen Gill)

<!-- toc -->

- [Project charter](#project-charter)
  * [Vision](#vision)
  * [Mission](#mission)
  * [Success criteria ](#success-criteria)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [Create RDS Database and upload raw data to S3](#step1)
  * [Cleaning the Data and creating a reproducable model](#step2)
  * [Building the web app](#step3)
  * [Run Tests](#run-tests)
  * [Run entire pipeline at once](#pipeline)

<!-- tocstop -->

## Project charter
### Vision
Over the past few decades, football has overtaken baseball as the number one sport in the United States and over that same time, sports gambling has increased in popularity. With the ease of online gambling, along with many states relaxing their gambling policies, gambling on NFL games is on pace to be the highests it's ever been and is showing no signs of slowing down. Many gamblers will bet on an NFL game's money line (simply betting which team will win), but another popular form of gambling is betting against the spread. When betting against the spread, betters not only have to factor in who will win a game but what the margin of victory will be. This extra is designed to make betting against the spread essentially a 50/50 proposition. This application hopes to turn that 50/50 proposition into something slightly more predictable and give users extra information when making gambling decisions.

### Mission
This application will have users input the home team, visiting team, and points spread for a game they wish to bet on. The application will then use use team information such as defensive and offensive efficiency, as well as current trends in the past few games to detrmine which team will cover the spread in the selected game. Spread data is provided by www.sportsbookreviewsonline.com and team data will be taken from www.pro-football-reference.com.

### Success criteria 
In the training/testing phase of app development, correct classification rate will be the metric used to test the model's performance. In this situation, the correct classification rate will be the proportion of the time the application corectly predicts which team will cover the spread. Because "the house always wins" in gambling, having a correct classification rate above 50% will not be enough to make money for a user. Typically, a bet against the spread has odds of -105, meaning you must risk $105 in order to win $100. This means that to make money betting against the spread, a gambler will need to be right at least 51.2% of the time. To account for this gap, the metric used to determine the app's business value will be observed money earned for every $100 risked in cross-validation.


## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Running the app

### Create RDS Database and upload raw data to S3

#### Make sure all S3 and RDS environment variables have been sorced 

```bash
export AWS_ACCESS_KEY_ID="MY_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="MY_SECRET_ACCESS_KEY"
export MYSQL_USER="MY_USERNAME"
export MYSQL_PASSWORD="MY_PASSWORD"
export MYSQL_HOST="MY_HOST"
export MYSQL_PORT="MY_PORT"
export MYSQL_DATABASE="MY_DATABASE"
```
Either of the following commands will build the Docker Image for this first step

```bash
docker build -f app/Dockerfile_getData -t getdata_bjh6390 .
```
or
```bash
make dataimage
```

The next commands can be used to run the Docker commands which have just been built

```bash
docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source=$(pwd),target=/app/ getdata_bjh6390 run.py createDB
```
and 
```bash
docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source=$(pwd),target=/app/ getdata_bjh6390 run.py loadData
```
or
```bash
make getdata
```

These commands will download the raw data from the online source and push that raw data to the s3 bucket at `s3://2021-msia423-hakimi-ben/rawCSVUpload/raw.csv` as well as create a mysql by default at the location `sqlite:///data/msia423_db.db`.

To set your own locations for the database, source your `SQLALCHEMY_DATABASE_URI` before running the commands.

### Cleaning the Data and creating a reproducable model

#### Again, make sure the same environmental variables are sourced as the first section

Either of the following commands will build the Docker Image for this step

```bash
docker build -f app/Dockerfile_getModel -t getmodel_bjh6390 .
```
or
```bash
make modelimage
```
The next commands can be used to run the Docker commands which have just been built

```bash
docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source=$(pwd),target=/app/ getmodel_bjh6390 run.py cleanData
```
and 
```bash
docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source=$(pwd),target=/app/ getmodel_bjh6390 run.py model
```
or
```bash
make getmodel
```

This step downloads the raw data locally from S3, cleans that data, and then builds a Random Forest Model to predict which team will cover the spread. Variables in the cleaning steps as well as model parameters can be changed using the config.yaml file found in the the config folder of this repository.

The model built in this step will be used 

### Building the web app

For this section, please export your own `SQLALCHEMY_DATABASE_URI` engine string to connect to the RDS instance used in the app. If not, the output of the app will be saved to the `sqlite:///data/msia423_db.db` mysql database created in the first step.


Either of the following commands will build the Docker Image for this step

```bash
ocker build -f app/Dockerfile -t runapp_bjh6390 .
```
or
```bash
make appimage
```
The next commands can be used to run the Docker commands which have just been built

```bash
	docker run -e SQLALCHEMY_DATABASE_URI --mount type=bind,source=$(pwd),target=/app/ -p 5000:5000 runapp_bjh6390 app.py
```
or
```bash
make runapp
```

This step will create a web app which can be used to precict who will cover in a user selected matchup. After running this step, you can access the web app locally at the folowing web address: `http://localhost:5000/`.


CONGRATS! You just created a web app!

### Run Tests
Make sure the Docker image for the `Cleaning the Data and creating a reproducable model` has been built before running these tests

The next commands can be used to run unit tests for the data cleaning phase

```bash
docker run getmodel_bjh6390 -m pytest
```
or
```bash
make test
```

### Run entire pipeline at once

This step is optional and can be used to run the entire pipeline from downloading the raw data from the source to creating the web app.
(All Makefile commands) 

First, we have to remove artifacts created in earlier steps using the following command:
(This command can be run at any time to remove data and models created by the first two steps)

```bash
make clean
```

Next build all the docker images needed:
```bash
make allimages
```

Finally, run the entire pipeline:
```bash
make fullpipeline
```








