import os

from sqlalchemy import create_engine

from sqlalchemy.orm import Session

pg_creds = (
    os.getenv('POSTGRES_USER'),
    os.getenv('POSTGRES_PASSWORD'),
    os.getenv('POSTGRES_HOST'),
    os.getenv('POSTGRES_PORT'),
    os.getenv('POSTGRES_DB')
)

engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' % pg_creds, echo = os.getenv('DATABASE_VERBOSE') == 'true')

def session():
    return Session(engine)
