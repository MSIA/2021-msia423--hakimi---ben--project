import sys
import logging

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String

import logging
import logging.config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Float


logger = logging.getLogger(__name__)
logger.setLevel("INFO")


## Table with induvidual game information
Base = declarative_base()

class Games(Base):
	"""Create a data model for the database to be set up for saving web app inputs """

	__tablename__ = 'Games'
	gameID = Column(String(100), primary_key=True)
	homeTeam = Column(String(100), unique=False, nullable=False)
	awayTeam = Column(String(100), unique=False, nullable=False)
	line = Column(Float, unique=False, nullable=False)
	homeCover = Column(Integer, unique=False, nullable=False)
	
	def __repr__(self):
		return '<Games %r>' % self.id

def createDB(engine_string):
	"""
    Create mysql database on either RDS or local

    Args:
        engine_string: (String), Required

    Returns:
        None

    """
	try:
		# set up mysql connection
		engine = sql.create_engine(engine_string)

		# create the Games table
		Base.metadata.create_all(engine)

		logger.info("Database successfully created using ENGINE_STRING = %s", engine_string)

	except:
		logger.error("Failed to create database using ENGINE_STRING = %s, please check inputs and credentials", engine_string)


class inputGames():
	def __init__(self, app=None, engine_string=None):
		"""
		Args:
			app: Flask - Flask app
			engine_string: str - Engine string
		"""
		if app:
			self.db = SQLAlchemy(app)
			self.session = self.db.session
		elif engine_string:
			try:
				engine = sql.create_engine(engine_string)
				Session = sessionmaker(bind=engine)
				self.session = Session()
				logger.debug("Session created")
			except sql.exc.ArgumentError:
				logging.error("ArgumentError: Check --engine_string and try again")
			except:
				logging.error("Unexpected error creating engine in ingest: %s", sys.exc_info())
		else:
			raise ValueError("Need either an engine string or a Flask app to initialize")

	def close(self) -> None:
		"""Closes session
		Returns: None
		"""
		try:
			self.session.close()
			logger.debug("Session closed")
		except AttributeError:
			logger.debug("AttributeError occurred trying to close a session that wasn't opened")
		except:
			logger.error("Unexpected error closing database session: %s", sys.exc_info())

	def add_game(self,
					game_id: str,
					home_team: str,
					away_team: str,
					spread: float,
					home_cover: int) -> None:
		"""Adds game predictions to database.

		Args:
			game_id (str): Randomly generated key
			home_team (str): Full Home Team Name
			away_team (str): Full Away Team Name
			spread (float): Spread input for matchup
			home_cover (int): Prediction from model
		
		Returns:None
		"""


		try:
			# Initiate the sesion, add the game, commit the session, then close
			session = self.session
			game = Games(gameID=game_id,
									homeTeam=home_team,
									awayTeam=away_team,
									line=spread,
									homeCover=home_cover)
			session.add(game)
			session.commit()
			logger.info("%s at %s, %s, added to database", home_team, away_team, spread)
		except AttributeError:
			logger.debug("AttributeError occurred trying to add entry using a session that wasn't opened")
		except:
			logging.error("Unexpected error adding game in ingest: %s", sys.exc_info())

