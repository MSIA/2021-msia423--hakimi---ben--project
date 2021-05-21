# NFL Spread Gambling App
## Ben Hakimi (QA: Stephen Gill)

<!-- toc -->

- [Project charter](#project-charter)
  * [Vision](#vision)
  * [Mission](#mission)
  * [Success criteria ](#success-criteria)
- [Directory structure](#directory-structure)
- [Running the app](#running-the-app)
  * [1. Initialize the database](#1-initialize-the-database)
    + [Create the database with a single song](#create-the-database-with-a-single-song)
    + [Adding additional songs](#adding-additional-songs)
    + [Defining your engine string](#defining-your-engine-string)
      - [Local SQLite database](#local-sqlite-database)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Run the Flask app](#3-run-the-flask-app)
- [Running the app in Docker](#running-the-app-in-docker)
  * [1. Build the image](#1-build-the-image)
  * [2. Run the container](#2-run-the-container)
  * [3. Kill the container](#3-kill-the-container)
  * [Workaround for potential Docker problem for Windows.](#workaround-for-potential-docker-problem-for-windows)

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

### 1. Load data into S3

#### Source S3 Credentials

Make sure the following AWS/S3 credentials have been loaded as environment variables:

```bash
export AWS_ACCESS_KEY_ID="MY_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="MY_SECRET_ACCESS_KEY"
```

#### Build Docker Image

Run the following command in the command line to build the Docker Image:

```bash
docker build -f app/Dockerfile -t nflgames .
```

#### Download raw data and upload to S3

To download the raw data using the previously built Docker Image, run the following in the command line:

```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY nflgames run.py loadData 2021-msia423-hakimi-ben rawCSVUpload/raw.csv
```

If no optional inputs are specified for the run.py function, the data will be pulled from the internet and placed in the local path `data/data.csv`. It will then be uploaded to the the S3 bucket `s3://2021-msia423-hakimi-ben/rawCSVUpload/raw.csv`. To change the S3 bucket (the 2021-msia423-hakimi-ben part of the previous path), input the desired name of your S3 bucket in the first argument after `loadData`. To change the name of the file when uploaded to S3 (the rawCSVUpload/raw.csv part of the previous path), input the desired file path in the second argument after `loadData`.

### 2. Initialize Database

#### Source RDS/mysql variables

Make sure the following RDS/mysql credentials have been loaded as environment variables:

```bash
export MYSQL_USER="MY_USERNAME"
export MYSQL_PASSWORD="MY_PASSWORD"
export MYSQL_HOST="MY_HOST"
export MYSQL_PORT="MY_PORT"
export MYSQL_DATABASE="MY_DATABASE"
```

#### Create Database

To create a database using the Docker Image, run the following in the command line:

```bash
docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABSE -e SQLALCHEMY_DATABASE_URI nflgames run.py createDB
```

To set your own locations for the database, source your `SQLALCHEMY_DATABASE_URI` and use it as an import to the above docker command. If no `SQLALCHEMY_DATABASE_URI` or `MYSQL_DATABASE` are input, the default will be `sqlite:///data/msia423_db.db`.

##### Local SQLite database

A local SQLite database can be created by not providing a `MYSQL_HOST` input and will create a database locally with the following engine string:

`engine_string = 'sqlite:///data/msia423_db.db'`


 
