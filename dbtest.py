import sqlalchemy

engine = sqlalchemy.create_engine("mysql+mysqldb://root:test@localhost/")

engine.connect()
engine.disconnect()

