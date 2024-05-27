# Dailies
Complete your daily tasks for long term goals



setup:

docker-compose up -d to create and start the db

To start the application, .env needs to be created with the following data:
CONDA_DEFAULT_ENV = /mambaforge/envs/dailies/bin/python
DATABASE_URI = mysql+pymysql://root:mysql@localhost:3306/dailies
user and password pulled from the docker-compose file


Server should be run with the following command:
python -m server.src.app