import sys
import logging
import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import logging
from flask_sqlalchemy import SQLAlchemy


## Configure and name logger
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

## Table with induvidual game information
Base = declarative_base()

class Games(Base):
	"""Create a data model for the database to be set up for capturing songs """

	__tablename__ = 'Games' ## Chose name of table
	homeTeam = Column(String(100), unique=False, nullable=False)
	awayTeam = Column(String(100), unique=False, nullable=False)
	line = Column(Integer, unique=False, nullable=False)
	
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


class inputGames(Base):
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
					home_team: str,
					away_team: str,
					spread: int,) -> None:
		"""Seeds an existing database with additional games.
		Args:
			home_full (str): Full name of the home team in the game in question
			home_abv (str): Abbreviated name of the home team
			home_wins (str): Number of wins on the season for the home team
			home_losses (str): Number of losses on the season for the home team
			away_full (str): Full name of the away team in the game in question
			away_abv (str): Abbreviated name of the away team
			away_wins (str): Number of wins on the season for the away team
			away_losses (str): Number of losses on the season for the away team
			game_date (str): Date on which the game is to be played
			game_location (str): Location in which the game is to be played (ex: city, stadium)
		Returns:None
		"""


		try:
			# Initiate the sesion, add the game, commit the session, then close
			session = self.session
			game = Games(homeTeam=home_team,
									awayTeam=away_team,
									line=spread)
			session.add(game)
			session.commit()
			logger.info("%s at %s, %s, added to database", home_team, away_team, spread)
		except AttributeError:
			logger.debug("AttributeError occurred trying to add entry using a session that wasn't opened")
		except:
			logging.error("Unexpected error adding game in ingest: %s", sys.exc_info())