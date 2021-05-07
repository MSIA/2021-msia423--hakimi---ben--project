import os
import logging
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)

# conn_type = "mysql+pymysql"
# user = os.environ.get("MYSQL_USER")
# password = os.environ.get("MYSQL_PASSWORD")
# host = os.environ.get("MYSQL_HOST")
# port = os.environ.get("MYSQL_PORT")
# database = os.environ.get("DATABASE_NAME")
# engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database)

def createDB(engine_string):
	Base = declarative_base()

	"""
    Create mysql database on either RDS or local

    Args:
        engine_string: (String), Required

    Returns:
        None

    """

	try:
		class Games(Base):
			"""Create a data model for the database to be set up for capturing songs """
			__tablename__ = 'Games'
			id = Column(Integer, primary_key=True)
			index = Column(Integer, unique=False, nullable=False)
			date = Column(Integer, unique=False, nullable=False)
			rot = Column(Integer, unique=False, nullable=False)
			VH = Column(String(100), unique=False, nullable=False)
			Team = Column(String(100), unique=False, nullable=False)
			First = Column(Integer, unique=False, nullable=False)
			Second = Column(Integer, unique=False, nullable=False)
			Third = Column(Integer, unique=False, nullable=False)
			Fourth = Column(Integer, unique=False, nullable=False)
			Final = Column(Integer, unique=False, nullable=False)
			Open = Column(String(100), unique=False, nullable=False)
			Close = Column(String(100), unique=False, nullable=False)
			ML = Column(Integer, unique=False, nullable=False)
			H2 = Column(String(100), unique=False, nullable=False)
			yr = Column(Integer, unique=False, nullable=False)
			
			def __repr__(self):
				return '<Games %r>' % self.id


		# set up mysql connection
		engine = sql.create_engine(engine_string)

		# create the tracks table
		Base.metadata.create_all(engine)

		logger.info("Database successfully created using ENGINE_STRING = %s", engine_string)

	except:
		logger.error("Failed to create database using ENGINE_STRING = %s, please check inputs and credentials", engine_string)


