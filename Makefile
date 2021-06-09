.PHONY: test dataimage modelimage appimage all clean

dataimage:
	docker build -f app/Dockerfile_getData -t getdata_bjh6390 .

data/rawdata.csv: config/config.yaml
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getdata_bjh6390 run.py createDB
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getdata_bjh6390 run.py loadData

getdata: data/rawdata.csv

modelimage:
	docker build -f app/Dockerfile_getModel -t getmodel_bjh6390 .

data/datafroms3.csv: config/config.yaml
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py cleanData
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py model

data/target.csv: config/config.yaml
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py cleanData
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py model

data/features.csv: config/config.yaml
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py cleanData
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py model
	
models/model.pkl: config/config.yaml
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py cleanData
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py model
	
models/testAccuracy.txt: config/config.yaml
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py cleanData
	docker run -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_DATABASE -e SQLALCHEMY_DATABASE_URI -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(shell pwd)",target=/app/ getmodel_bjh6390 run.py model
	
getmodel: models/model.pkl

appimage: 
	docker build -f app/Dockerfile -t runapp_bjh6390 .

runapp:
	docker run -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(shell pwd)",target=/app/ -p 5000:5000 runapp_bjh6390 app.py

test:
	docker run getmodel_bjh6390 -m pytest

clean:
	rm data/*
	rm models/*

allimages: dataimage modelimage appimage
fullpipeline: getdata getmodel runapp
