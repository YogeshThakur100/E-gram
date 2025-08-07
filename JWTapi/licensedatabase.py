from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE="postgresql://postgres:root@localhost:5432/license"
# URL_DATABASE="postgresql://postgres:Gunadhya%40%23987@localhost:5432/jobdescription"


engine=create_engine(URL_DATABASE)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        # db._warn_on_events={}
        yield db
    except KeyboardInterrupt:
        # print("Key Borad Interrupt")
        pass
    finally:
        db.close()