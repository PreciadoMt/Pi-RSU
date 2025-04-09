import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

dbName = 'MentalBalance.db'
base_dir= os.path.dirname(os.path.realpath(__file__))
dbUrl= f"sqlite:///{os.path.join(base_dir,dbName)}"

engine=create_engine(dbUrl,echo=True)
Session=sessionmaker(bind=engine)
Base=declarative_base()

