from enum import unique
from peewee import *

db = SqliteDatabase("notlar.db")

class BaseModel(Model):
    class Meta:
        database=db

class Kullanici(BaseModel):
    kullaniciadi=CharField(unique=True)
    adsoyad=CharField(max_length=255)
    sifre=CharField(max_length=20)

class Notlar(BaseModel):
    baslik=CharField(max_length=1000)
    icerik=TextField()
    yayintarihi = CharField()

db.connect()
db.create_tables([Kullanici,Notlar])