from enum import unique
from peewee import *
import os
db_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database=db_proxy

class Kullanici(BaseModel):
    kullaniciadi=CharField(unique=True)
    adsoyad=CharField(max_length=255)
    sifre=CharField(max_length=20)

class Notlar(BaseModel):
    baslik=CharField(max_length=1000)
    icerik=TextField()
    yayintarihi = CharField()
    kullaniciadi = CharField()

class PaylasilanNotlar(BaseModel):
    paylasimid=CharField()
    icid=CharField()

if 'HEROKU' in os.environ:
    import urlparse, psycopg2
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    db_proxy.initialize(db)
else:
    db = SqliteDatabase('notlar.db')
    db_proxy.initialize(db)

if __name__ == '__main__':
    db_proxy.connect()
    db_proxy.create_tables([Kullanici,Notlar,PaylasilanNotlar], safe=True)