from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, create_engine, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship

import json


DeclarativeBase = declarative_base()


class Documents(DeclarativeBase):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column('title', String)

    authors = Column('authors', String, nullable=True)
    keywords = Column('keywords', String, nullable=True)
    summary = Column('summary', Text, nullable=True)
    url_view = Column('url_view', String, nullable=True)
    url_pdf = Column('url_pdf', String, nullable=True)
    journal = Column('journal', Integer)
    trash = Column('trash', Boolean, default=False)


class RawData(DeclarativeBase):

    __tablename__ = "rawdata"

    id = Column(Integer, primary_key=True)

    raw_data = Column('raw_data', Text, nullable=True)
    html_doc = Column('html_doc', Text, nullable=True)

    document_id = Column(Integer, ForeignKey('documents.id'))
    document = relationship('Documents', backref = 'documents')


class DB():

    def __init__(self):
        self.engine = self.__db_connect()
        self.__create_tables(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save(self, item, journal):
        session = self.Session()
        try:

            doc_data = {
                'title': item['title'],
                'authors': item['authors'],
                'keywords': item['keywords'],
                'summary': item['summary'],
                'url_view': item['url_view'],
                'url_pdf': item['url_pdf'],
                'journal': journal,
            }

            doc = Documents(**doc_data)
            session.add(doc)

            session.flush()
            session.refresh(doc)

            raw_data = {
                'raw_data': json.dumps(item['raw_data']),
                'html_doc': item['html_doc'],
                'document': doc,
            }
            raw = RawData(**raw_data)

            session.add(raw)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

    def __db_connect(self):

        engine = create_engine('postgres://yhkwgjpzocdvxp:b8e01ffe882c4042df1adb673fec46de6880b94c32c869b34feb4c800c5f2c52@ec2-50-19-218-160.compute-1.amazonaws.com:5432/dfquvos8et8l34', pool_recycle=1200)
        return engine

    def __create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine)


'''
Install postgre
> sudo apt-get update
> sudo apt-get install postgresql postgresql-contrib

Comandos do banco de dados
> sudo -i -u postgres
> psql
> \q

> sudo -u postgres createuser --interactivec -W
> createuser -P -s -e joe

> sudo -u postgres createdb ci
> createdb ci

> sudo -i -u joe

> psql -d ci -U joe 

Mac Start/Stop Postgres

pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
pg_ctl -D /usr/local/var/postgres stop -s -m fast
'''
